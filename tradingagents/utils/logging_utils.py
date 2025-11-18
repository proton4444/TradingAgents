"""
Logging utilities for TradingAgents.

Provides simple, configurable logging for the application.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


class TradingAgentsLogger:
    """Singleton logger for TradingAgents."""

    _instance: Optional[logging.Logger] = None

    @classmethod
    def get_logger(
        cls,
        name: str = "tradingagents",
        level: str = "INFO",
        log_file: Optional[str] = None,
    ) -> logging.Logger:
        """
        Get or create a logger instance.

        Args:
            name: Logger name
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file to write logs to

        Returns:
            Configured logger instance
        """
        if cls._instance is not None:
            return cls._instance

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))

        # Remove existing handlers to avoid duplicates
        logger.handlers.clear()

        # Console handler with formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        # Format: [2024-01-15 10:30:45] INFO: Message here
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler if specified
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        cls._instance = logger
        return logger


def get_logger(name: str = "tradingagents", **kwargs) -> logging.Logger:
    """
    Convenience function to get a logger.

    Args:
        name: Logger name
        **kwargs: Additional arguments for TradingAgentsLogger.get_logger()

    Returns:
        Logger instance
    """
    return TradingAgentsLogger.get_logger(name, **kwargs)


# Default logger instance
logger = get_logger()
