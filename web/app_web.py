# web/app_web.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from tm.turing_machine import TuringMachine

app = FastAPI(title="Машина Тьюринга — Палиндром")

os.makedirs("web/templates", exist_ok=True)
os.makedirs("web/static", exist_ok=True)

templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # ожидается, что в web/templates/index.html есть фронтенд
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/check")
async def check_word(request: Request):
    data = await request.json()
    word = data.get("word", "").strip()

    if not word:
        return JSONResponse({"error": "Введите слово!"}, status_code=400)

    # ТuringMachine поддерживает конструктор с первым аргументом input_str (см. tm/turing_machine.py)
    machine = TuringMachine(word)
    machine.run()

    return JSONResponse({
        "result": machine.get_result(),
        "tape": str(machine.tape),
        "is_palindrome": machine.state == machine.accept_state
    })


@app.get("/status")
async def get_status():
    return JSONResponse({"status": "ok", "message": "Сервер работает"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web.app_web:app", host="0.0.0.0", port=8000, reload=True)
