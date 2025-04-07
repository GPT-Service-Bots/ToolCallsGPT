from typing import Callable, Dict

FUNCTION_REGISTRY: Dict[str, Callable] = {}


def register(func: Callable):
    """
    Декоратор для автоматической регистрации функции
    """
    FUNCTION_REGISTRY[func.__name__] = func
    return func
