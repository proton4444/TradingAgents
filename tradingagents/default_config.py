"""
Default configuration for TradingAgents.

This module provides default configuration values that can be overridden
via environment variables or by passing a custom config dictionary.

Environment Variables:
    TRADINGAGENTS_RESULTS_DIR: Directory for saving analysis results
    TRADINGAGENTS_DATA_DIR: Directory for local data storage
    TRADINGAGENTS_CACHE_DIR: Directory for caching data
    LLM_PROVIDER: LLM provider (openai, anthropic, google, openrouter, ollama)
    BACKEND_URL: LLM API endpoint URL
    DEEP_THINK_MODEL: Model for complex reasoning
    QUICK_THINK_MODEL: Model for quick analysis
"""

import os
from pathlib import Path


def _get_project_dir() -> str:
    """Get the project directory (tradingagents package root)."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "."))


def _get_data_dir() -> str:
    """
    Get data directory, checking environment variable first.

    Falls back to a 'data' folder in the project root if not set.
    This replaces the hardcoded developer-specific path.
    """
    env_data_dir = os.getenv("TRADINGAGENTS_DATA_DIR")
    if env_data_dir:
        return env_data_dir

    # Default to a 'data' directory in the project root
    project_root = Path(_get_project_dir()).parent
    default_data_dir = project_root / "data"

    # Create it if it doesn't exist
    default_data_dir.mkdir(exist_ok=True)

    return str(default_data_dir)


def _get_cache_dir() -> str:
    """Get cache directory for downloaded data."""
    env_cache_dir = os.getenv("TRADINGAGENTS_CACHE_DIR")
    if env_cache_dir:
        return env_cache_dir

    return os.path.join(_get_project_dir(), "dataflows/data_cache")


def _get_results_dir() -> str:
    """Get results directory for analysis outputs."""
    return os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results")


# Default configuration dictionary
# Values can be overridden via environment variables or custom config
DEFAULT_CONFIG = {
    # Directory configuration
    "project_dir": _get_project_dir(),
    "results_dir": _get_results_dir(),
    "data_dir": _get_data_dir(),
    "data_cache_dir": _get_cache_dir(),

    # LLM settings - can be overridden by environment variables
    "llm_provider": os.getenv("LLM_PROVIDER", "openrouter"),
    "deep_think_llm": os.getenv("DEEP_THINK_MODEL", "openai/gpt-4o-mini"),
    "quick_think_llm": os.getenv("QUICK_THINK_MODEL", "openai/gpt-4o-mini"),
    "backend_url": os.getenv("BACKEND_URL", "https://openrouter.ai/api/v1"),

    # Debate and discussion settings
    "max_debate_rounds": int(os.getenv("MAX_DEBATE_ROUNDS", "1")),
    "max_risk_discuss_rounds": int(os.getenv("MAX_RISK_DISCUSS_ROUNDS", "1")),
    "max_recur_limit": int(os.getenv("MAX_RECUR_LIMIT", "100")),

    # Data vendor configuration
    # Category-level configuration (default for all tools in category)
    "data_vendors": {
        "core_stock_apis": os.getenv("CORE_STOCK_VENDOR", "yfinance"),
        "technical_indicators": os.getenv("TECHNICAL_INDICATORS_VENDOR", "yfinance"),
        "fundamental_data": os.getenv("FUNDAMENTAL_DATA_VENDOR", "alpha_vantage"),
        "news_data": os.getenv("NEWS_DATA_VENDOR", "openai"),
    },

    # Tool-level configuration (takes precedence over category-level)
    "tool_vendors": {
        # Example: "get_stock_data": "alpha_vantage",  # Override category default
        # Example: "get_news": "openai",               # Override category default
    },
}


def get_config_value(key: str, default=None):
    """
    Get a configuration value by key.

    Args:
        key: Configuration key
        default: Default value if key not found

    Returns:
        Configuration value
    """
    return DEFAULT_CONFIG.get(key, default)


def validate_config(config: dict) -> tuple[bool, list[str]]:
    """
    Validate a configuration dictionary.

    Args:
        config: Configuration dictionary to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Check required keys
    required_keys = ["llm_provider", "deep_think_llm", "quick_think_llm", "backend_url"]
    for key in required_keys:
        if key not in config or not config[key]:
            errors.append(f"Missing required configuration: {key}")

    # Validate LLM provider
    valid_providers = ["openai", "anthropic", "google", "openrouter", "ollama"]
    if config.get("llm_provider") and config["llm_provider"].lower() not in valid_providers:
        errors.append(
            f"Invalid llm_provider: {config['llm_provider']}. "
            f"Must be one of: {', '.join(valid_providers)}"
        )

    # Validate directories exist or can be created
    for dir_key in ["results_dir", "data_dir", "data_cache_dir"]:
        if dir_key in config:
            dir_path = Path(config[dir_key])
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create directory {dir_key}='{dir_path}': {e}")

    return len(errors) == 0, errors
