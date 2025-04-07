import logging
import sys


class ExtraFormatter(logging.Formatter):
    def format(self, record):
        base_msg = super().format(record)
        extra_attrs = set(record.__dict__.keys()) - logging.LogRecord('', '', '', '', '', (), None).__dict__.keys()
        if extra_attrs:
            extra_data = ' | '.join(f'{key}={record.__dict__[key]}' for key in extra_attrs)
            return f"{base_msg} | {extra_data}"
        return base_msg


def setup_logger(name: str = "whatsapp_logger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = ExtraFormatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


