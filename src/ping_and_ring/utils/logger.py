"""Application logging configuration and logger factory."""

import logging
import logging.config
from datetime import datetime
from typing import Any

import yaml

from ping_and_ring.constants import LOGGING_CONFIG_FILE_PATH, PROJECT_ROOT

_LOGGING_CONFIGURED = False


class UTCOffsetFormatter(logging.Formatter):
    """Formats log timestamps with the local UTC offset."""

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        """Formats a log record timestamp with its UTC offset.

        Args:
            record: Log record containing the event creation timestamp.
            datefmt: Timestamp format string. Uses the default format when
                omitted.

        Returns:
            The formatted timestamp followed by the UTC offset.
        """
        timestamp = datetime.fromtimestamp(record.created).astimezone()
        offset = timestamp.strftime("%z")
        formatted_offset = f"{offset[:3]}:{offset[3:]}"
        return f"{timestamp.strftime(datefmt or '%Y-%m-%d %H:%M:%S')} UTC{formatted_offset}"


def get_date_time() -> tuple[str, str]:
    """Returns the current local date and time parts.

    Returns:
        A tuple containing the date in ``YYYY-MM-DD`` format and the time in
        ``HH_MM_SS`` format.
    """
    timestamp = datetime.now().astimezone()
    return timestamp.strftime("%Y-%m-%d"), timestamp.strftime("%H_%M_%S")


def _load_logging_config() -> dict[str, Any]:
    """Loads the logging configuration from the YAML file.

    Returns:
        The parsed logging configuration.
    """
    with LOGGING_CONFIG_FILE_PATH.open(encoding="utf-8") as yaml_file:
        return yaml.safe_load(yaml_file)


def _configure_file_handler(logging_config: dict[str, Any]) -> None:
    """Configures or removes the optional file handler.

    Args:
        logging_config: Parsed logging configuration to update.
    """
    file_handler_config = logging_config["handlers"]["file_handler"]
    file_logging_enabled = file_handler_config.pop("enable", True)

    if file_logging_enabled:
        log_root_dir = file_handler_config.pop("log_root_dir")
        log_date, log_time = get_date_time()
        log_file_path = PROJECT_ROOT / log_root_dir / log_date / f"folioflow_{log_time}.log"
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler_config["filename"] = str(log_file_path)
    else:
        del logging_config["handlers"]["file_handler"]
        logging_config["root"]["handlers"].remove("file_handler")


def setup_logging() -> None:
    """Loads and applies the logging configuration from YAML.

    Logging is configured only once. Subsequent calls return without changing
    the existing logging configuration.
    """
    global _LOGGING_CONFIGURED

    if _LOGGING_CONFIGURED:
        return

    logging_config = _load_logging_config()
    _configure_file_handler(logging_config)
    logging_config["formatters"]["default"]["()"] = UTCOffsetFormatter
    logging.config.dictConfig(logging_config)
    _LOGGING_CONFIGURED = True


def get_logger(name: str = "root") -> logging.Logger:
    """Returns a configured logger by name.

    Args:
        name: Name of the logger to return.

    Returns:
        A configured logger instance.
    """
    if not _LOGGING_CONFIGURED:
        setup_logging()

    return logging.getLogger(name)
