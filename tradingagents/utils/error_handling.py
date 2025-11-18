"""
Error handling utilities for TradingAgents.

Provides custom exceptions and error handling helpers.
"""

from typing import Optional, Any
from functools import wraps
import traceback


class TradingAgentsError(Exception):
    """Base exception for TradingAgents errors."""
    pass


class ConfigurationError(TradingAgentsError):
    """Raised when configuration is invalid or missing."""
    pass


class APIError(TradingAgentsError):
    """Raised when external API calls fail."""

    def __init__(self, message: str, provider: Optional[str] = None, details: Optional[Any] = None):
        self.provider = provider
        self.details = details
        super().__init__(message)


class DataFetchError(TradingAgentsError):
    """Raised when data fetching fails."""

    def __init__(self, message: str, ticker: Optional[str] = None, source: Optional[str] = None):
        self.ticker = ticker
        self.source = source
        super().__init__(message)


class ModelError(TradingAgentsError):
    """Raised when LLM model operations fail."""

    def __init__(self, message: str, model: Optional[str] = None, provider: Optional[str] = None):
        self.model = model
        self.provider = provider
        super().__init__(message)


def safe_execute(default_return=None, raise_on_error=False, log_errors=True):
    """
    Decorator for safe function execution with error handling.

    Args:
        default_return: Value to return if function fails (when raise_on_error=False)
        raise_on_error: If True, re-raise exceptions; if False, return default_return
        log_errors: If True, log errors when they occur

    Example:
        @safe_execute(default_return=[], log_errors=True)
        def fetch_data():
            # May raise exceptions
            return api.get_data()
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    from tradingagents.utils.logging_utils import logger
                    logger.error(f"Error in {func.__name__}: {str(e)}")
                    logger.debug(traceback.format_exc())

                if raise_on_error:
                    raise
                return default_return

        return wrapper
    return decorator


def validate_api_key(key: Optional[str], name: str = "API key") -> None:
    """
    Validate that an API key is present and not a placeholder.

    Args:
        key: API key to validate
        name: Name of the key for error messages

    Raises:
        ConfigurationError: If key is missing or appears to be a placeholder
    """
    if not key:
        raise ConfigurationError(f"{name} is missing. Please check your .env file.")

    if any(word in key.upper() for word in ["REPLACE", "PLACEHOLDER", "YOUR_KEY", "XXX"]):
        raise ConfigurationError(
            f"{name} appears to be a placeholder. "
            "Please replace it with your actual API key in the .env file."
        )


def format_error_message(error: Exception, context: Optional[str] = None) -> str:
    """
    Format an error message with context.

    Args:
        error: Exception object
        context: Optional context string

    Returns:
        Formatted error message
    """
    error_type = type(error).__name__
    error_msg = str(error)

    if context:
        return f"{context}: {error_type}: {error_msg}"
    return f"{error_type}: {error_msg}"


def retry_on_error(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator to retry a function on failure with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry

    Example:
        @retry_on_error(max_retries=3, delay=1.0)
        def fetch_data():
            return api.get_data()
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            from tradingagents.utils.logging_utils import logger

            retries = 0
            current_delay = delay

            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(
                            f"{func.__name__} failed after {max_retries} retries: {str(e)}"
                        )
                        raise

                    logger.warning(
                        f"{func.__name__} failed (attempt {retries}/{max_retries}), "
                        f"retrying in {current_delay:.1f}s: {str(e)}"
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator
