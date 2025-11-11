# gui/app_gui.py
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, 
                             QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, 
                             QMessageBox, QGroupBox, QScrollArea)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPalette

class CompactTuringAppGUI(QWidget):
    """
    Минималистичный графический интерфейс для машины Тьюринга.
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
        self.apply_clean_styles()

    def init_ui(self):
        self.setWindowTitle("Машина Тьюринга: Палиндром")
        self.setGeometry(100, 100, 900, 700)

        # Главный layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Строка ввода
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите слово для проверки на палиндром")
        self.input_field.setMinimumHeight(40)
        
        self.load_btn = QPushButton("Загрузить слово")
        self.load_btn.setMinimumHeight(40)
        self.load_btn.setMinimumWidth(120)
        
        input_layout.addWidget(QLabel("Слово:"))
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.load_btn)
        main_layout.addLayout(input_layout)

        # Панель управления
        control_layout = QHBoxLayout()
        
        self.step_btn = QPushButton("Выполнить шаг")
        self.run_btn = QPushButton("Автоматический режим")
        self.stop_btn = QPushButton("Остановить")
        self.reset_btn = QPushButton("Сброс")
        
        self.step_btn.setEnabled(False)
        self.run_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        
        for btn in [self.step_btn, self.run_btn, self.stop_btn, self.reset_btn]:
            btn.setMinimumHeight(35)
            btn.setMinimumWidth(140)
            control_layout.addWidget(btn)
        
        control_layout.addStretch()
        self.steps_label = QLabel("Шагов выполнено: 0")
        self.steps_label.setStyleSheet("font-weight: 500; color: #2c3e50; font-size: 13px;")
        control_layout.addWidget(self.steps_label)
            
        main_layout.addLayout(control_layout)

        # Лента машины Тьюринга
        tape_group = QGroupBox("Лента машины Тьюринга")
        tape_layout = QVBoxLayout(tape_group)
        
        tape_scroll = QScrollArea()
        tape_scroll.setMinimumHeight(130)
        tape_scroll.setMaximumHeight(150)
        tape_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        tape_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tape_scroll.setWidgetResizable(True)
        
        self.tape_widget = QWidget()
        self.tape_layout = QHBoxLayout(self.tape_widget)
        self.tape_layout.setSpacing(3)
        self.tape_layout.setContentsMargins(15, 15, 15, 15)
        self.tape_layout.setAlignment(Qt.AlignLeft)
        
        tape_scroll.setWidget(self.tape_widget)
        tape_layout.addWidget(tape_scroll)
        
        main_layout.addWidget(tape_group)

        # Информация о результате
        self.result_label = QLabel("Результат: Введите слово и нажмите 'Загрузить слово'")
        self.result_label.setStyleSheet("padding: 15px; background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 6px; font-weight: 500; font-size: 14px;")
        self.result_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.result_label)

        # Журнал выполнения
        log_group = QGroupBox("Журнал выполнения")
        log_layout = QVBoxLayout(log_group)
        
        self.log_display = QTextEdit()
        self.log_display.setFont(QFont("Segoe UI", 10))
        self.log_display.setPlaceholderText("Здесь будет отображаться процесс выполнения шагов машины...")
        log_layout.addWidget(self.log_display)
        
        # Кнопка очистки лога
        self.clear_log_btn = QPushButton("Очистить журнал")
        self.clear_log_btn.setMaximumHeight(35)
        log_layout.addWidget(self.clear_log_btn)
        
        main_layout.addWidget(log_group, 1)

        self.setLayout(main_layout)

        # Подключение сигналов
        self.load_btn.clicked.connect(self.load_word)
        self.step_btn.clicked.connect(self.do_step)
        self.run_btn.clicked.connect(self.start_auto)
        self.stop_btn.clicked.connect(self.stop_auto)
        self.reset_btn.clicked.connect(self.reset_machine)
        self.clear_log_btn.clicked.connect(self.clear_log)
        self.input_field.returnPressed.connect(self.load_word)

    def create_tape_cell(self, symbol, index, is_current=False):
        """Создать ячейку ленты"""
        cell_widget = QWidget()
        cell_layout = QVBoxLayout(cell_widget)
        cell_layout.setSpacing(2)
        cell_layout.setContentsMargins(4, 4, 4, 4)
        
        # Индекс позиции
        index_label = QLabel(str(index))
        index_label.setAlignment(Qt.AlignCenter)
        index_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #6c757d;
                padding: 2px;
                font-weight: 500;
            }
        """)
        
        # Символ ячейки
        symbol_label = QLabel(symbol)
        symbol_label.setAlignment(Qt.AlignCenter)
        symbol_label.setMinimumWidth(35)
        symbol_label.setMinimumHeight(35)
        
        if is_current:
            # Текущая позиция головки
            symbol_label.setStyleSheet("""
                QLabel {
                    border: 2px solid #e74c3c;
                    border-radius: 6px;
                    background: white;
                    color: #e74c3c;
                    font-weight: 600;
                    font-size: 16px;
                    padding: 8px;
                }
            """)
            index_label.setStyleSheet("""
                QLabel {
                    font-size: 10px;
                    color: #e74c3c;
                    font-weight: 600;
                    padding: 2px;
                }
            """)
        else:
            symbol_label.setStyleSheet("""
                QLabel {
                    border: 1px solid #bdc3c7;
                    border-radius: 5px;
                    background: white;
                    color: #2c3e50;
                    font-weight: 500;
                    font-size: 14px;
                    padding: 8px;
                }
            """)
        
        cell_layout.addWidget(index_label)
        cell_layout.addWidget(symbol_label)
        
        # Стрелка головки для текущей позиции
        if is_current:
            head_label = QLabel("▼")
            head_label.setAlignment(Qt.AlignCenter)
            head_label.setStyleSheet("""
                QLabel {
                    color: #e74c3c;
                    font-weight: 600;
                    font-size: 12px;
                    margin-top: 2px;
                }
            """)
            cell_layout.addWidget(head_label)
        
        return cell_widget

    def update_tape_display(self):
        """Обновить отображение ленты"""
        if not self.is_loaded or not self.machine.tape:
            # Показываем сообщение о загрузке
            for i in reversed(range(self.tape_layout.count())): 
                widget = self.tape_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()
            
            message_label = QLabel("Загрузите слово для отображения ленты")
            message_label.setAlignment(Qt.AlignCenter)
            message_label.setStyleSheet("color: #6c757d; font-style: italic; font-size: 14px;")
            self.tape_layout.addWidget(message_label)
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
                symbol_display = "_"
            else:
                symbol_display = symbol
                
            is_current = (i == self.machine.head)
            cell_widget = self.create_tape_cell(symbol_display, i, is_current)
            self.tape_layout.addWidget(cell_widget)
        
        # Добавляем растягивающий элемент в конец
        self.tape_layout.addStretch()

    def apply_clean_styles(self):
        """Применить чистые современные стили"""
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                background-color: #ffffff;
                font-size: 13px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 12px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
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
                padding: 8px 12px;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                background: white;
                font-size: 13px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-weight: 400;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background: #f8fffe;
            }
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                padding: 12px;
                background-color: white;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 12px;
                font-weight: 400;
            }
            QGroupBox {
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 12px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-weight: 600;
                font-size: 14px;
                color: #2c3e50;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-weight: 600;
            }
            QScrollArea {
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                background: white;
            }
            QLabel {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-weight: 400;
            }
        """)

    def load_word(self):
        word = self.input_field.text().strip()
        if not word:
            self.show_message("Внимание", "Пожалуйста, введите слово для проверки!", QMessageBox.Warning)
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
            
            self.log_display.clear()
            self.update_display(f"Начало проверки слова: '{word}'")
            self.update_display("Машина готова к выполнению.")
            
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
            # Выполняем один шаг и сразу обновляем интерфейс
            action = self.machine.step()
            self.steps_count += 1
            self.update_steps_counter()
            self.update_tape_display()
            self.update_state_info()
            self.update_display(f"Шаг {self.steps_count}: {self.extract_main_action(action)}")
            
            if self.machine.is_halted():
                self.show_completion_message()
                
        except Exception as e:
            self.show_message("Ошибка", f"Ошибка при выполнении шага: {str(e)}", QMessageBox.Critical)

    def extract_main_action(self, action):
        """Извлечь основное действие из многострочного описания"""
        lines = action.strip().split('\n')
        if len(lines) >= 4:
            return lines[1].strip()
        return action

    def start_auto(self):
        if not self.is_loaded:
            self.show_message("Информация", "Сначала загрузите слово!", QMessageBox.Information)
            return
        
        if self.machine.is_halted():
            self.show_completion_message()
            return
        
        self.timer.start(800)  # 0.8 секунды между шагами
        self.run_btn.setEnabled(False)
        self.step_btn.setEnabled(False)
        self.update_display("Запущен автоматический режим")

    def stop_auto(self):
        self.timer.stop()
        self.run_btn.setEnabled(True)
        self.step_btn.setEnabled(True)
        self.update_display("Автоматический режим остановлен")

    def auto_step(self):
        if self.machine.is_halted():
            self.timer.stop()
            self.run_btn.setEnabled(True)
            self.step_btn.setEnabled(True)
            self.show_completion_message()
            return
        
        try:
            # Выполняем один шаг и сразу обновляем интерфейс
            action = self.machine.step()
            self.steps_count += 1
            self.update_steps_counter()
            self.update_tape_display()
            self.update_state_info()
            self.update_display(f"Шаг {self.steps_count}: {self.extract_main_action(action)}")
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
        
        current_word = self.input_field.text().strip()
        if current_word:
            try:
                self.machine.load_tape(current_word)
                self.is_loaded = True
                self.step_btn.setEnabled(True)
                self.run_btn.setEnabled(True)
                self.stop_btn.setEnabled(True)
                self.update_tape_display()
                self.update_display("Машина перезагружена")
            except Exception as e:
                self.show_message("Ошибка", f"Ошибка при перезагрузке: {str(e)}", QMessageBox.Warning)
        else:
            self.update_display("Машина сброшена")
            self.update_tape_display()

    def clear_log(self):
        self.log_display.clear()
        self.update_display("Журнал очищен")

    def update_display(self, log_message):
        """Обновить журнал выполнения"""
        try:
            self.log_display.append(log_message)
            self.log_display.ensureCursorVisible()
        except Exception as e:
            print(f"Ошибка при обновлении лога: {e}")

    def update_state_info(self, reset=False):
        try:
            if reset:
                self.result_label.setText("Результат: Введите слово и нажмите 'Загрузить слово'")
                self.result_label.setStyleSheet("padding: 15px; background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 6px; font-weight: 500; font-size: 14px;")
                return
                
            current_state = self.machine.state
            
            if self.machine.is_halted():
                if current_state == self.machine.accept_state:
                    result_text = "Слово является палиндромом!"
                    style = "padding: 15px; background: #d4edda; border: 1px solid #c3e6cb; border-radius: 6px; font-weight: 500; font-size: 14px;"
                elif current_state == self.machine.reject_state:
                    result_text = "Слово не является палиндромом"
                    style = "padding: 15px; background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 6px; font-weight: 500; font-size: 14px;"
                else:
                    result_text = f"Завершено ({current_state})"
                    style = "padding: 15px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 6px; font-weight: 500; font-size: 14px;"
            else:
                result_text = "Выполняется проверка..."
                style = "padding: 15px; background: #d1ecf1; border: 1px solid #bee5eb; border-radius: 6px; font-weight: 500; font-size: 14px;"
            
            self.result_label.setText(f"Результат: {result_text}")
            self.result_label.setStyleSheet(style)
            
        except Exception as e:
            print(f"Ошибка при обновлении состояния: {e}")

    def update_steps_counter(self):
        self.steps_label.setText(f"Шагов выполнено: {self.steps_count}")

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
                self.update_display(f"РАБОТА ЗАВЕРШЕНА: {current_state}")
            
            self.show_message("Завершено", message, QMessageBox.Information)
            
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