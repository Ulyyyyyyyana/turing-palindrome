from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from tm.turing_machine import TuringMachine, TransitionTable
import traceback

app = FastAPI(title="Машина Тьюринга — Палиндром")
templates = Jinja2Templates(directory="web/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Главная страница с визуализацией работы машины Тьюринга.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/check")
async def check_word(request: Request):
    """
    Проверка слова на палиндром.
    Принимает JSON {"word": "..."} и возвращает пошаговую симуляцию.
    """
    data = await request.json()
    word = data.get("word", "").strip()

    if not word:
        return JSONResponse({"error": "Введите слово для проверки!"}, status_code=400)

    try:
        # Создаём таблицу переходов и машину Тьюринга
        table = TransitionTable.strict_palindrome_table()
        machine = TuringMachine(table)
        machine.load_tape(word)

        steps = []
        max_steps = 500
        step_count = 0

        while not machine.is_halted() and step_count < max_steps:
            tape_str = "".join(machine.tape.cells)
            current_symbol = machine.read_symbol()

            # Выполняем один шаг
            action_text = machine.step()

            # Формируем понятное описание шага
            human_action = f"Машина считывает символ «{current_symbol}». {action_text}."
            if "влево" in action_text:
                human_action += " Головка движется влево."
            elif "вправо" in action_text:
                human_action += " Головка движется вправо."
            elif "остались" in action_text:
                human_action += " Головка остаётся на месте."

            steps.append({
                "tape": tape_str,
                "head": machine.head,
                "state": machine.state,
                "action": human_action
            })
            step_count += 1

        result = machine.get_result()
        is_palindrome = machine.state == machine.accept_state

        return JSONResponse({
            "is_palindrome": is_palindrome,
            "result": result,
            "steps": steps
        })

    except Exception:
        traceback.print_exc()
        return JSONResponse({
            "error": "Произошла внутренняя ошибка при обработке слова. Попробуйте снова."
        }, status_code=500)
