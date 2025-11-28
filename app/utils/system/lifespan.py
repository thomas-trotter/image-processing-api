"""
Application lifespan management.

This module provides the lifespan context manager for FastAPI that handles
startup and shutdown operations, including cleanup of temporary files.

For detailed documentation, see the module's README.md file.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from pathlib import Path

from app.utils.system.clean_up import clean_up
from app.core.logging_config import get_logger

logger = get_logger("lifespan")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown lifecycle.

    This async context manager is used by FastAPI to manage the application
    lifecycle. It performs cleanup operations (removing __pycache__ directories)
    after the application shuts down.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Control is yielded to the application during its runtime.
    """
    logger.info("Starting lifespan context...")

    project_root = Path(__file__).parent.parent.parent
    
    yield

    logger.info("Removing __pycache__ after shutdown...")
    clean_up(project_root)
    logger.info("Lifespan context ended.")
