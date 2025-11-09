# gui/app_gui.py
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, 
                             QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, 
                             QMessageBox, QGroupBox, QSplitter,
                             QFrame, QScrollArea)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

class CompactTuringAppGUI(QWidget):
    """
    Графический интерфейс с классической горизонтальной лентой.
    """
    def __init__(self, machine):
        super().__init__()
        self.machine = machine
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_step)
        self.steps_count = 0
        self.is_loaded = False
        self.last_action = ""

        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        self.setWindowTitle("Машина Тьюринга: Палиндром")
        self.setGeometry(100, 100, 900, 700)

        # Главный layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Строка ввода
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите слово для проверки")
        self.input_field.setMaximumHeight(30)
        
        self.load_btn = QPushButton("Загрузить")
        self.load_btn.setMaximumHeight(30)
        self.load_btn.setMaximumWidth(100)
        
        input_layout.addWidget(QLabel("Слово:"))
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.load_btn)
        main_layout.addLayout(input_layout)

        # Панель управления
        control_layout = QHBoxLayout()
        
        self.step_btn = QPushButton("Шаг")
        self.run_btn = QPushButton("Авто")
        self.stop_btn = QPushButton("Стоп")
        self.reset_btn = QPushButton("Сброс")
        
        self.step_btn.setEnabled(False)
        self.run_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        
        for btn in [self.step_btn, self.run_btn, self.stop_btn, self.reset_btn]:
            btn.setMinimumHeight(30)
            btn.setMaximumWidth(80)
            control_layout.addWidget(btn)
        
        control_layout.addStretch()
        self.steps_label = QLabel("Шагов: 0")
        self.steps_label.setStyleSheet("font-weight: bold; color: #34495e;")
        control_layout.addWidget(self.steps_label)
            
        main_layout.addLayout(control_layout)

        # Классическая горизонтальная лента
        tape_group = QGroupBox("ЛЕНТА МАШИНЫ ТЬЮРИНГА")
        tape_group.setStyleSheet("QGroupBox { font-weight: bold; color: #2c3e50; }")
        tape_layout = QVBoxLayout(tape_group)
        
        # Контейнер для ленты с прокруткой
        tape_scroll = QScrollArea()
        tape_scroll.setMinimumHeight(120)
        tape_scroll.setMaximumHeight(140)
        tape_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        tape_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tape_scroll.setWidgetResizable(True)
        
        self.tape_widget = QWidget()
        self.tape_layout = QHBoxLayout(self.tape_widget)
        self.tape_layout.setSpacing(0)
        self.tape_layout.setContentsMargins(10, 10, 10, 10)
        self.tape_layout.setAlignment(Qt.AlignLeft)
        
        tape_scroll.setWidget(self.tape_widget)
        tape_layout.addWidget(tape_scroll)
        
        main_layout.addWidget(tape_group)

        # Горизонтальная панель действий машины
        actions_frame = QFrame()
        actions_frame.setFrameStyle(QFrame.Box)
        actions_frame.setStyleSheet("QFrame { border: 2px solid #3498db; border-radius: 8px; background: #ebf5fb; }")
        actions_layout = QHBoxLayout(actions_frame)
        
        # Текущее действие
        self.action_label = QLabel("Действие: Ожидание загрузки...")
        self.action_label.setStyleSheet("padding: 8px; background: white; border-radius: 5px; font-weight: bold; color: #2c3e50;")
        self.action_label.setAlignment(Qt.AlignCenter)
        
        # Состояние и позиция
        state_pos_layout = QHBoxLayout()
        self.state_label = QLabel("Состояние: -")
        self.position_label = QLabel("Позиция: -")
        
        for label in [self.state_label, self.position_label]:
            label.setStyleSheet("padding: 6px; background: white; border-radius: 4px; font-size: 11px; margin: 2px;")
            label.setAlignment(Qt.AlignCenter)
            state_pos_layout.addWidget(label)
        
        actions_layout.addWidget(self.action_label, 2)
        actions_layout.addLayout(state_pos_layout, 1)
        
        main_layout.addWidget(actions_frame)

        # Информация о результате
        result_layout = QHBoxLayout()
        
        self.result_label = QLabel("Результат: Ожидание ввода...")
        self.result_label.setStyleSheet("padding: 10px; background: #fff3cd; color: #856404; border-radius: 6px; font-weight: bold; font-size: 12px;")
        self.result_label.setAlignment(Qt.AlignCenter)
        
        result_layout.addWidget(self.result_label)
        main_layout.addLayout(result_layout)

        # Splitter для лога
        splitter = QSplitter(Qt.Vertical)
        
        # Лог выполнения
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        log_layout.setContentsMargins(0, 0, 0, 0)
        
        log_header = QLabel("ЛОГ ВЫПОЛНЕНИЯ")
        log_header.setStyleSheet("font-weight: bold; color: #2c3e50; padding: 2px;")
        log_layout.addWidget(log_header)
        
        log_controls = QHBoxLayout()
        self.clear_log_btn = QPushButton("Очистить")
        self.clear_log_btn.setMaximumHeight(25)
        self.export_log_btn = QPushButton("Экспорт")
        self.export_log_btn.setMaximumHeight(25)
        log_controls.addStretch()
        log_controls.addWidget(self.clear_log_btn)
        log_controls.addWidget(self.export_log_btn)
        log_layout.addLayout(log_controls)
        
        self.log_display = QTextEdit()
        self.log_display.setFont(QFont("Consolas", 9))
        self.log_display.setPlaceholderText("Здесь отображается подробный лог выполнения...")
        log_layout.addWidget(self.log_display)
        
        splitter.addWidget(log_widget)
        splitter.setSizes([300])
        
        main_layout.addWidget(splitter, 1)

        self.setLayout(main_layout)

        # Подключение сигналов
        self.load_btn.clicked.connect(self.load_word)
        self.step_btn.clicked.connect(self.do_step)
        self.run_btn.clicked.connect(self.start_auto)
        self.stop_btn.clicked.connect(self.stop_auto)
        self.reset_btn.clicked.connect(self.reset_machine)
        self.clear_log_btn.clicked.connect(self.clear_log)
        self.export_log_btn.clicked.connect(self.export_log)
        self.input_field.returnPressed.connect(self.load_word)

    def create_tape_cell(self, symbol, index, is_current=False):
        """Создать ячейку ленты"""
        cell_widget = QWidget()
        cell_layout = QVBoxLayout(cell_widget)
        cell_layout.setSpacing(2)
        cell_layout.setContentsMargins(3, 3, 3, 3)
        
        # Индекс позиции
        index_label = QLabel(str(index))
        index_label.setAlignment(Qt.AlignCenter)
        index_label.setStyleSheet("""
            QLabel {
                font-size: 9px;
                color: #7f8c8d;
                padding: 1px;
            }
        """)
        
        # Символ ячейки
        symbol_label = QLabel(symbol)
        symbol_label.setAlignment(Qt.AlignCenter)
        symbol_label.setMinimumWidth(25)
        symbol_label.setMinimumHeight(25)
        
        if is_current:
            # Текущая позиция головки
            symbol_label.setStyleSheet("""
                QLabel {
                    border: 3px solid #e74c3c;
                    border-radius: 5px;
                    background: white;
                    color: #e74c3c;
                    font-weight: bold;
                    font-size: 14px;
                    padding: 5px;
                }
            """)
            index_label.setStyleSheet("""
                QLabel {
                    font-size: 9px;
                    color: #e74c3c;
                    font-weight: bold;
                    padding: 1px;
                }
            """)
        else:
            symbol_label.setStyleSheet("""
                QLabel {
                    border: 2px solid #bdc3c7;
                    border-radius: 4px;
                    background: white;
                    color: #2c3e50;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 5px;
                }
            """)
        
        cell_layout.addWidget(index_label)
        cell_layout.addWidget(symbol_label)
        
        # Стрелка головки для текущей позиции
        if is_current:
            head_label = QLabel("v")
            head_label.setAlignment(Qt.AlignCenter)
            head_label.setStyleSheet("""
                QLabel {
                    color: #e74c3c;
                    font-weight: bold;
                    font-size: 12px;
                }
            """)
            cell_layout.addWidget(head_label)
        else:
            # Пустой placeholder для выравнивания
            spacer = QLabel(" ")
            spacer.setFixedHeight(15)
            cell_layout.addWidget(spacer)
        
        return cell_widget

    def update_tape_display(self):
        """Обновить отображение ленты"""
        if not self.is_loaded or not self.machine.tape:
            return
            
        # Очищаем предыдущую ленту
        for i in reversed(range(self.tape_layout.count())): 
            widget = self.tape_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Создаем новые ячейки
        tape_str = str(self.machine.tape)
        for i, symbol in enumerate(tape_str):
            if symbol == "⊔":
                symbol_display = "_"  # Более читаемый символ пустоты
            else:
                symbol_display = symbol
                
            is_current = (i == self.machine.head)
            cell_widget = self.create_tape_cell(symbol_display, i, is_current)
            self.tape_layout.addWidget(cell_widget)
        
        # Добавляем растягивающий элемент в конец
        self.tape_layout.addStretch()

    def update_action_display(self, action):
        """Обновить отображение текущего действия"""
        # Обрабатываем новый многострочный формат
        lines = action.strip().split('\n')
        
        if len(lines) >= 4:
            # Новый формат: берем только основное действие (вторую строку)
            main_action = lines[1].strip()
            self.action_label.setText(f"Действие: {main_action}")
            self.last_action = action
        else:
            # Старый формат для обратной совместимости
            if "читаем" in action and "пишем" in action:
                parts = action.split("→")
                if len(parts) >= 1:
                    self.action_label.setText(f"Действие: {parts[0].strip()}")
            else:
                self.action_label.setText(f"Действие: {action}")
            
            self.last_action = action

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #f8f9fa;
                font-size: 11px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 6px 10px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background: white;
                font-size: 11px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background: #f8fffe;
            }
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 6px;
                background-color: white;
            }
            QGroupBox {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QScrollArea {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background: white;
            }
        """)

    def load_word(self):
        word = self.input_field.text().strip()
        if not word:
            self.show_message("Ошибка", "Введите слово для проверки!", QMessageBox.Warning)
            return
        
        try:
            self.machine.load_tape(word)
            self.steps_count = 0
            self.is_loaded = True
            self.update_steps_counter()
            
            self.step_btn.setEnabled(True)
            self.run_btn.setEnabled(True)
            self.stop_btn.setEnabled(True)
            
            self.update_tape_display()
            self.update_state_info()
            self.update_action_display("Машина готова к работе")
            self.update_display("Начало работы. Слово загружено.")
            
        except Exception as e:
            self.show_message("Ошибка", f"Ошибка при загрузке слова: {str(e)}", QMessageBox.Critical)

    def do_step(self):
        if not self.is_loaded:
            self.show_message("Информация", "Сначала загрузите слово!", QMessageBox.Information)
            return
        
        if self.machine.is_halted():
            self.show_completion_message()
            return
        
        try:
            action = self.machine.step()
            self.steps_count += 1
            self.update_steps_counter()
            self.update_tape_display()
            self.update_state_info()
            self.update_action_display(action)
            self.update_display(action)
            
            if self.machine.is_halted():
                self.show_completion_message()
                
        except Exception as e:
            self.show_message("Ошибка", f"Ошибка при выполнении шага: {str(e)}", QMessageBox.Critical)

    def start_auto(self):
        if not self.is_loaded:
            self.show_message("Информация", "Сначала загрузите слово!", QMessageBox.Information)
            return
        
        if self.machine.is_halted():
            self.show_completion_message()
            return
        
        self.timer.start(800)
        self.run_btn.setEnabled(False)
        self.step_btn.setEnabled(False)
        self.update_action_display("Автоматический режим запущен")
        self.update_display("Авторежим запущен")

    def stop_auto(self):
        self.timer.stop()
        self.run_btn.setEnabled(True)
        self.step_btn.setEnabled(True)
        self.update_action_display("Автоматический режим остановлен")
        self.update_display("Авторежим остановлен")

    def auto_step(self):
        if self.machine.is_halted():
            self.timer.stop()
            self.run_btn.setEnabled(True)
            self.step_btn.setEnabled(True)
            self.show_completion_message()
            return
        
        try:
            action = self.machine.step()
            self.steps_count += 1
            self.update_steps_counter()
            self.update_tape_display()
            self.update_state_info()
            self.update_action_display(action)
            self.update_display(action)
        except Exception as e:
            self.timer.stop()
            self.show_message("Ошибка", f"Ошибка в автоматическом режиме: {str(e)}", QMessageBox.Critical)

    def reset_machine(self):
        self.timer.stop()
        self.steps_count = 0
        self.is_loaded = False
        self.update_steps_counter()
        
        self.step_btn.setEnabled(False)
        self.run_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        
        # Очищаем ленту
        for i in reversed(range(self.tape_layout.count())): 
            widget = self.tape_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        self.log_display.clear()
        self.update_state_info(reset=True)
        self.update_action_display("Машина сброшена")
        
        current_word = self.input_field.text().strip()
        if current_word:
            try:
                self.machine.load_tape(current_word)
                self.is_loaded = True
                self.step_btn.setEnabled(True)
                self.run_btn.setEnabled(True)
                self.stop_btn.setEnabled(True)
                self.update_tape_display()
                self.update_display("Машина сброшена и перезагружена")
            except Exception as e:
                self.show_message("Ошибка", f"Ошибка при перезагрузке: {str(e)}", QMessageBox.Warning)
        else:
            self.update_display("Машина сброшена")

    def clear_log(self):
        self.log_display.clear()
        self.update_display("Лог очищен")

    def export_log(self):
        QMessageBox.information(self, "Экспорт", "Функция экспорта в разработке")

    def update_display(self, log_message):
        try:
            # Просто добавляем сообщение без времени и лишнего форматирования
            self.log_display.append(log_message)
            self.log_display.ensureCursorVisible()
        except Exception as e:
            print(f"Ошибка: {e}")

    def update_state_info(self, reset=False):
        try:
            if reset:
                self.state_label.setText("Состояние: -")
                self.position_label.setText("Позиция: -")
                self.result_label.setText("Результат: Ожидание ввода...")
                self.result_label.setStyleSheet("padding: 10px; background: #fff3cd; color: #856404; border-radius: 6px; font-weight: bold;")
                return
                
            current_state = self.machine.state
            head_position = self.machine.head
            
            self.state_label.setText(f"Состояние: {current_state}")
            self.position_label.setText(f"Позиция: {head_position}")
            
            if self.machine.is_halted():
                if current_state == self.machine.accept_state:
                    result_text = "Слово является палиндромом!"
                    style = "padding: 10px; background: #d4edda; color: #155724; border-radius: 6px; font-weight: bold;"
                elif current_state == self.machine.reject_state:
                    result_text = "Слово не является палиндромом"
                    style = "padding: 10px; background: #f8d7da; color: #721c24; border-radius: 6px; font-weight: bold;"
                else:
                    result_text = f"Завершено ({current_state})"
                    style = "padding: 10px; background: #fff3cd; color: #856404; border-radius: 6px; font-weight: bold;"
            else:
                result_text = "Выполняется проверка..."
                style = "padding: 10px; background: #d1ecf1; color: #0c5460; border-radius: 6px; font-weight: bold;"
            
            self.result_label.setText(f"Результат: {result_text}")
            self.result_label.setStyleSheet(style)
            
        except Exception as e:
            print(f"Ошибка при обновлении состояния: {e}")

    def update_steps_counter(self):
        self.steps_label.setText(f"Шагов: {self.steps_count}")

    def show_completion_message(self):
        try:
            current_state = self.machine.state
            
            if current_state == self.machine.accept_state:
                message = "Слово является палиндромом!"
                self.update_display("РЕЗУЛЬТАТ: Слово является палиндромом!")
            elif current_state == self.machine.reject_state:
                message = "Слово не является палиндромом"
                self.update_display("РЕЗУЛЬТАТ: Слово не является палиндромом")
            else:
                message = f"Завершено: {current_state}"
                self.update_display(f"Работа завершена: {current_state}")
            
            self.show_message("Готово", message, QMessageBox.Information)
            
        except Exception as e:
            self.show_message("Ошибка", f"Ошибка при завершении: {str(e)}", QMessageBox.Critical)

    def show_message(self, title, message, icon):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.exec_()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

# Для обратной совместимости
TuringAppGUI = CompactTuringAppGUI