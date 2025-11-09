# demo_palindrome.py
from tm.turing_machine import TuringMachine
from tm.transitions import TransitionTable

def demonstrate_palindrome(word, use_universal=False):
    """Демонстрирует работу машины Тьюринга на конкретном слове"""
    print(f"\n{'='*60}")
    print(f"Проверка слова: '{word}'")
    print(f"Ожидаемый результат: {'палиндром' if word == word[::-1] else 'не палиндром'}")
    print('='*60)
    
    # Выбираем таблицу переходов
    if use_universal:
        table = TransitionTable.universal_palindrome_table()
        print("Используется УНИВЕРСАЛЬНАЯ машина (любые символы)")
    else:
        table = TransitionTable.default_palindrome_table()
        print("Используется ОСНОВНАЯ машина (только a/b)")
    
    machine = TuringMachine(transitions=table)
    machine.load_tape(word)
    
    step = 0
    print(f"\nНачальное состояние:")
    print(f"  Лента: {machine._get_tape_with_head()}")
    print(f"  Состояние: {machine.state}")
    
    while not machine.is_halted() and step < 100:
        step += 1
        action = machine.step()
        
        # Показываем только основную информацию о шаге
        lines = action.strip().split('\n')
        if len(lines) >= 2:
            main_action = lines[1]  # Берем вторую строку с действием
            print(f"\nШаг {step}: {main_action}")
            print(f"  Лента: {machine._get_tape_with_head()}")
            print(f"  Состояние: {machine.state}")
    
    print(f"\n{'='*60}")
    result = "ПРИНЯТО" if machine.state == "q_accept" else "ОТВЕРГНУТО"
    print(f"РЕЗУЛЬТАТ: {result}")
    print(f"Финальное состояние: {machine.state}")
    print(f"Всего шагов: {step}")
    print(f"Совпало с ожиданием: {'✓' if (machine.state == 'q_accept') == (word == word[::-1]) else '✗'}")
    print('='*60)

if __name__ == "__main__":
    # Тестируем основную машину (только a/b)
    print("ДЕМОНСТРАЦИЯ ОСНОВНОЙ МАШИНЫ (символы a/b):")
    test_words = ["", "a", "b", "aa", "ab", "aba", "abb", "abba", "abab"]
    
    for word in test_words:
        demonstrate_palindrome(word, use_universal=False)
    
    # Тестируем универсальную машину (любые символы)
    print("\n\nДЕМОНСТРАЦИЯ УНИВЕРСАЛЬНОЙ МАШИНЫ (любые символы):")
    universal_words = ["", "x", "xy", "xx", "xyz", "xyx", "radar", "level"]
    
    for word in universal_words:
        demonstrate_palindrome(word, use_universal=True)