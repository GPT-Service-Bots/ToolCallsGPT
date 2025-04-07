import logging
from typing import Any

logger = logging.getLogger("app_logger")


def mask_sensitive_data(data):
    """
    Маскирует чувствительные данные в словаре.
    """
    SENSITIVE_FIELDS = {"tg_token", "open_ai_key", "open_ai_assistant_key", "manager_tg_id"}

    if isinstance(data, dict):
        return {
            key: "****" if key in SENSITIVE_FIELDS else mask_sensitive_data(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [mask_sensitive_data(item) for item in data]
    return data


def _prepare_log_extra(action: str, **kwargs) -> dict[str, Any]:
    """
    Подготавливает структуру для передачи в параметр `extra` логгера.

    Основная логика:
    - Рекурсивно маскирует чувствительные данные в kwargs;
    - Возвращает словарь с двумя ключами:
        - `action`: краткое название действия (используется как категория события);
        - `context`: безопасный контекст с дополнительной информацией (kwargs после маскировки);

    Эта функция используется во всех шаблонах логирования и позволяет:
    - единообразно оформлять логи;
    - не повторять логику маскировки и структурирования в каждом вызове;
    - передавать данные в JSON-логгер без ручной сериализации.
    """
    masked_data = mask_sensitive_data(kwargs)
    return {
        "action": action,
        "context": masked_data
    }


def log_debug(action: str, message: str, **kwargs):
    extra = _prepare_log_extra(action, **kwargs)
    logger.debug(message, extra=extra)


def log_info(action: str, message: str, **kwargs):
    extra = _prepare_log_extra(action, **kwargs)
    logger.info(message, extra=extra)


def log_warning(action: str, message: str, **kwargs):
    extra = _prepare_log_extra(action, **kwargs)
    logger.warning(message, extra=extra)


def log_error(action: str, message: str, exc_info: bool = False, **kwargs):
    extra = _prepare_log_extra(action, **kwargs)
    logger.error(message, extra=extra, exc_info=exc_info)


def log_critical(action: str, message: str, exc_info: bool = False, **kwargs):
    extra = _prepare_log_extra(action, **kwargs)
    logger.critical(message, extra=extra, exc_info=exc_info)
