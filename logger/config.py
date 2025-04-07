
import logging
import sys
from logging.handlers import RotatingFileHandler
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
LOG_FILE_PATH = "logs/app.log"
MAX_LOG_SIZE_MB = 5
BACKUP_COUNT = 3


class ExtraFormatter(logging.Formatter):
    def format(self, record):
        base_msg = super().format(record)
        extra_attrs = set(record.__dict__.keys()) - logging.LogRecord('', '', '', '', '', (), None).__dict__.keys()
        if extra_attrs:
            extra_data = ' | '.join(f'{key}={record.__dict__[key]}' for key in extra_attrs)
            return f"{base_msg} | {extra_data}"
        return base_msg


def configure_logger() -> logging.Logger:
    logger = logging.getLogger("app_logger")
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False  # не передаём логи выше (в корневой логгер)

    if not logger.handlers:
        # ==== Форматтер ====
        formatter = ExtraFormatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        # ==== Консоль ====
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        # Создаём папку для логов
        os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

        # ==== Файл с ротацией ====
        file_handler = RotatingFileHandler(
            LOG_FILE_PATH,
            maxBytes=MAX_LOG_SIZE_MB * 1024 * 1024,
            backupCount=BACKUP_COUNT,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
