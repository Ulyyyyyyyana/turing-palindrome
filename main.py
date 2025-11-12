import sys
import sqlite3
from PyQt5.QtWidgets import QApplication
from tm.turing_machine import TuringMachine
from tm.transitions import TransitionTable
from gui.app_gui import TuringAppGUI, init_db


def main():
    """Точка входа в GUI-приложение 'Машина Тьюринга — Палиндром'."""
    # 1. Инициализируем базу данных (создаётся таблица history, если её нет)
    init_db()

    # 2. Создаём таблицу переходов и саму машину Тьюринга
    transitions = TransitionTable.strict_palindrome_table()
    machine = TuringMachine(
        transitions,
        start_state="q0",
        accept_state="q_accept",
        reject_state="q_reject"
    )

    # 3. Запускаем приложение PyQt5
    app = QApplication(sys.argv)
    gui = TuringAppGUI(machine)
    gui.show()

    # 4. Безопасный выход при закрытии
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
