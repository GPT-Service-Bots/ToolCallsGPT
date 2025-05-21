from typing import Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel

from functions.registry import FUNCTION_REGISTRY
from logger.config import configure_logger
from logger.templates import log_critical, log_info
import functions

app = FastAPI()

configure_logger()


# Pydantic-модель запроса
class FunctionCallRequest(BaseModel):
    function_name: str
    args: Dict[str, Any]
    request_id: str


# Эндпоинт для выполнения функции
@app.post("/execute_tool")
async def execute_tool(request: FunctionCallRequest):
    log_info(
        action='Запрос выполнения функции',
        message='Пришёл запрос',
        function_name=request.function_name,
        args=request.args,
        request_id=request.request_id
    )
    func = FUNCTION_REGISTRY.get(request.function_name)

    if not func:
        return {"result": f"Функция '{request.function_name}' не найдена."}

    try:
        result = func(**request.args)
        return {"result": result}
    except TypeError as e:
        log_critical(
            action="Вызов функции",
            message='Ошибка при вызове функции TypeError',
            request_id=request.request_id,
            exc_info=True,
            error=str(e),
        )
        return {"result": "Внутренняя ошибка при вызове функции"}
    except Exception as e:
        log_critical(
            action="Вызов функции",
            message='Ошибка при вызове функции Exception',
            request_id=request.request_id,
            exc_info=True,
            error=str(e),
        )
        return {"result": "Внутренняя ошибка при вызове функции"}


@app.on_event("startup")
async def on_startup():
    log_info("startup", "FastAPI приложение инициализировано")