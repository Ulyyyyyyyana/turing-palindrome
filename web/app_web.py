# web/app_web.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from tm.turing_machine import TuringMachine, TransitionTable
import traceback

app = FastAPI()

templates = Jinja2Templates(directory="web/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/check")
async def check_word(request: Request):
    data = await request.json()
    word = data.get("word", "").strip()

    if not word:
        return JSONResponse({"error": "Введите слово"}, status_code=400)

    try:
        # создаём таблицу переходов и машину
        table = TransitionTable.universal_palindrome_table()
        machine = TuringMachine(table)
        machine.load_tape(word)

        steps = []
        max_steps = 500
        step_count = 0

        while not machine.is_halted() and step_count < max_steps:
            tape_str = "".join(machine.tape.cells)
            steps.append({
                "tape": tape_str,
                "head": machine.head,
                "state": machine.state,
                "action": f"Шаг {step_count + 1}: {machine.step()}"
            })
            step_count += 1

        result = machine.get_result()
        return JSONResponse({
            "is_palindrome": machine.state == machine.accept_state,
            "result": result,
            "steps": steps
        })

    except Exception as e:
        print("Ошибка:", traceback.format_exc())
        return JSONResponse({"error": str(e)}, status_code=500)
