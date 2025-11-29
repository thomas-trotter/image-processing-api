"""
Centralized logging configuration for the application.

This module sets up centralized logging with rotating file handlers
and optional console output. Log levels and handlers are configured
based on application settings.

For detailed documentation, see the module's README.md file.
"""

from app.core.config import settings
from typing import Optional

import logging
from logging.handlers import RotatingFileHandler
import os


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file_path = os.path.join(LOG_DIR, "app.log")

logger = logging.getLogger("logging_config")
logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]")


file_handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=5)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

if settings.DEBUG:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG) 
    logger.addHandler(console_handler)

if not logger.hasHandlers():
    logger.addHandler(file_handler)

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Retrieves a logger instance, either the main app logger or a child logger.

    Creates a child logger if a name is provided, otherwise returns the main
    application logger. Child loggers inherit the configuration from the main logger.

    Args:
        name (str, optional): Name for a child logger. If None, returns the main logger.
            Defaults to None.

    Returns:
        logging.Logger: The logger instance (either the main logger or a child logger).
    """
    return logger if not name else logger.getChild(name)
