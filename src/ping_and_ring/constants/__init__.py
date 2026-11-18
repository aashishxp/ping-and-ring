"""Application-wide constants and configuration paths."""

from pathlib import Path

# Root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
APP_ROOT = PROJECT_ROOT / "src" / "ping_and_ring"

# Filesystem paths
ENV_FILE_PATH = PROJECT_ROOT / ".env"
APP_CONFIG_FILE_PATH = APP_ROOT / "configs" / "config.yaml"
LOGGING_CONFIG_FILE_PATH = APP_ROOT / "configs" / "logging.yaml"
