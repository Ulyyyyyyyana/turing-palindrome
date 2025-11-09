# tm/transitions.py
class TransitionTable:
    """
    Хранит таблицу переходов δ для Машины Тьюринга.
    Формат transitions: { state: { symbol_or__any_: (write_symbol, move, new_state), ... }, ... }
    move: "L", "R" или "S"
    """
    def __init__(self, transitions: dict):
        self.transitions = transitions or {}

    def get(self, state: str, symbol: str):
        """
        Возвращает кортеж (что_записать, куда_двигаться, новое_состояние)
        Если перехода нет — возвращает None
        """
        if state in self.transitions:
            state_transitions = self.transitions[state]
            # точное совпадение
            if symbol in state_transitions:
                return state_transitions[symbol]
            # wildcard
            if '_any_' in state_transitions:
                return state_transitions['_any_']
        return None

    def __contains__(self, state: str):
        return state in self.transitions

    def __repr__(self):
        return f"<TransitionTable states={len(self.transitions)}>"

    @staticmethod
    def default_palindrome_table():
        """
        Пример таблицы для алфавита {'a','b'} (как в вашем оригинальном фрагменте).
        Возвращает TransitionTable.
        """
        transitions = {
            "q0": {
                "a": ("a", "R", "q0"),
                "b": ("b", "R", "q0"),
                "⊔": ("⊔", "L", "q1")
            },
            "q1": {
                "X": ("X", "L", "q1"),
                "a": ("X", "L", "q2"),
                "b": ("X", "L", "q3"),
                "⊔": ("⊔", "R", "q_accept")
            },
            "q2": {
                "a": ("a", "L", "q2"),
                "b": ("b", "L", "q2"),
                "X": ("X", "L", "q2"),
                "⊔": ("⊔", "R", "q4")
            },
            "q3": {
                "a": ("a", "L", "q3"),
                "b": ("b", "L", "q3"),
                "X": ("X", "L", "q3"),
                "⊔": ("⊔", "R", "q5")
            },
            "q4": {
                "X": ("X", "R", "q1"),
                "a": ("X", "R", "q1"),
                "b": ("b", "S", "q_reject"),
                "⊔": ("⊔", "S", "q_reject")
            },
            "q5": {
                "X": ("X", "R", "q1"),
                "b": ("X", "R", "q1"),
                "a": ("a", "S", "q_reject"),
                "⊔": ("⊔", "S", "q_reject")
            },
            "q_accept": {},
            "q_reject": {}
        }
        return TransitionTable(transitions)

    @staticmethod
    def universal_palindrome_table():
        """
        Более обобщённая таблица, использующая '_any_' для любых символов.
        (пример — сохраняет логику поиска пары)
        """
        transitions = {
            "q0": {
                "_any_": ("_any_", "R", "q0"),
                "⊔": ("⊔", "L", "q1")
            },
            "q1": {
                "X": ("X", "L", "q1"),
                "⊔": ("⊔", "R", "q_accept"),
                "_any_": ("X", "L", "q2")
            },
            "q2": {
                "_any_": ("_any_", "L", "q2"),
                "X": ("X", "L", "q2"),
                "⊔": ("⊔", "R", "q3")
            },
            "q3": {
                "X": ("X", "R", "q1"),
                "_any_": ("X", "R", "q1"),
                "⊔": ("⊔", "S", "q_reject")
            },
            "q_accept": {},
            "q_reject": {}
        }
        return TransitionTable(transitions)
