"""Logging utility for Jarvis."""

import logging
from datetime import datetime
from pathlib import Path


# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"jarvis_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Jarvis")


def log(emoji: str, message: str):
    """Log a message with an emoji prefix."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_message = f"{emoji} [{timestamp}] {message}"
    logger.info(log_message)
    print(log_message)


def debug(message: str):
    """Log a debug message."""
    logger.debug(message)


def error(message: str):
    """Log an error message."""
    logger.error(message)
    print(f"❌ ERROR: {message}")


def success(message: str):
    """Log a success message."""
    logger.info(f"✅ {message}")
    print(f"✅ {message}")
