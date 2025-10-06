import logging
from enum import Enum


# -------------------------------------------------------------------
# Log level definitions
# -------------------------------------------------------------------
class LogLevels(str, Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


# -------------------------------------------------------------------
# Default format for detailed debugging
# -------------------------------------------------------------------
LOG_FORMAT_DEBUG = "%(levelname)s: %(message)s [%(pathname)s:%(funcName)s:%(lineno)d]"


# -------------------------------------------------------------------
# Configure the logging system
# -------------------------------------------------------------------
def configure_logging(log_level: str | LogLevels = LogLevels.ERROR) -> None:
    """
    Configure application logging.

    Args:
        log_level (str | LogLevels): Desired logging level. Defaults to ERROR.
    """

    # Convert enum to string if necessary
    if isinstance(log_level, LogLevels):
        log_level = log_level.value

    # Normalize case
    log_level = str(log_level).upper()

    # Map string to actual logging constant
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARN,
        "ERROR": logging.ERROR,
    }

    level = log_level_map.get(log_level, logging.ERROR)

    # Apply configuration
    if level == logging.DEBUG:
        logging.basicConfig(level=level, format=LOG_FORMAT_DEBUG)
    else:
        logging.basicConfig(level=level)

    logging.getLogger("uvicorn").setLevel(level)
    logging.getLogger("uvicorn.error").setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(level)
    logging.info(f"Logging initialized with level: {log_level}")
