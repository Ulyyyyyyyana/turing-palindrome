# main.py
import sys
from PyQt5.QtWidgets import QApplication
from tm.turing_machine import TuringMachine
from tm.transitions import TransitionTable
from gui.app_gui import TuringAppGUI

# --- Построим универсальную таблицу переходов (пример, можно заменить вашей)
transitions = TransitionTable.universal_palindrome_table()

# Создаём машину: передаём таблицу и имена нач/принятия/отклонения
machine = TuringMachine(transitions, start_state="q0", accept_state="q_accept", reject_state="q_reject")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TuringAppGUI(machine)
    gui.show()
    sys.exit(app.exec_())
