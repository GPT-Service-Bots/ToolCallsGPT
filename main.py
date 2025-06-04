from typing import Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel

from functions.registry import FUNCTION_REGISTRY
import functions
from logger import log

app = FastAPI()


# Pydantic-модель запроса
class FunctionCallRequest(BaseModel):
    function_name: str
    args: Dict[str, Any]
    request_id: str


# Эндпоинт для выполнения функции
@app.post("/execute_tool")
async def execute_tool(request: FunctionCallRequest):
    log.info(
        "Пришёл запрос на выполнение функции",
        extra={
            "function_name": request.function_name,
            "args": request.args,
            "request_id": request.request_id,
        }
    )
    func = FUNCTION_REGISTRY.get(request.function_name)

    if not func:
        return {"result": f"Функция '{request.function_name}' не найдена."}

    try:
        result = await func(**request.args)
        return {"result": result}
    except TypeError as e:
        log.error(
            "Ошибка при вызове функции TypeError",
            exc_info=e,
            extra={
                "function_name": request.function_name,
                "args": request.args,
                "request_id": request.request_id,
            }
        )
        return {"result": "Внутренняя ошибка при вызове функции"}
    except Exception as e:
        log.error(
            "Ошибка при вызове функции Неизвестная ошибка",
            exc_info=e,
            extra={
                "function_name": request.function_name,
                "args": request.args,
                "request_id": request.request_id,
            }
        )
        return {"result": "Внутренняя ошибка при вызове функции"}


@app.on_event("startup")
async def on_startup():
    log.info(
        "FastAPI приложение инициализировано"
    )
