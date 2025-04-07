from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from functions.registry import FUNCTION_REGISTRY
from logger.templates import log_critical

app = FastAPI()


# Pydantic-модель запроса
class FunctionCallRequest(BaseModel):
    function_name: str
    args: Dict[str, Any]


# Эндпоинт для выполнения функции
@app.post("/execute_tool")
async def execute_tool(request: FunctionCallRequest):
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
            exc_info=True,
            error=str(e),
        )
        return {"result": "Внутренняя ошибка при вызове функции"}
    except Exception as e:
        log_critical(
            action="Вызов функции",
            message='Ошибка при вызове функции Exception',
            exc_info=True,
            error=str(e),
        )
        return {"result": "Внутренняя ошибка при вызове функции"}
