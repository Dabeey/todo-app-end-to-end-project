import logging
import os
from enum import Enum

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOG_FORMAT_DEBUG = "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | line:%(lineno)d | %(message)s"

class LogLevels(str, Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


def configure_logging(log_level: str = LogLevels.ERROR.value):
    """Configures global logging for the app."""
    log_level = str(log_level).upper()

    if log_level not in LogLevels._value2member_map_:
        log_level = LogLevels.ERROR.value

    # Prevent duplicate handlers if reloaded
    if logging.getLogger().hasHandlers():
        logging.getLogger().handlers.clear()

    # Choose format
    log_format = LOG_FORMAT_DEBUG if log_level == LogLevels.DEBUG.value else LOG_FORMAT

    # Configure logging
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(),  # Console
            logging.FileHandler(LOG_FILE)  # File
        ]
    )

    logging.info(f"Logging configured at level: {log_level}")
    return logging.getLogger(__name__)
