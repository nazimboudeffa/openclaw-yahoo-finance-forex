"""
Configuration loader for OpenClaw bot.

Loads configuration from environment variables with defaults.
"""

import os
from typing import Any, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def _get_bool(key: str, default: bool) -> bool:
    """
    Get boolean value from environment variable.
    
    Args:
        key: Environment variable name
        default: Default value if not set
        
    Returns:
        Boolean value
    """
    value = os.getenv(key, str(default)).lower()
    return value in ('true', '1', 'yes', 'on')


def _get_int(key: str, default: int) -> int:
    """
    Get integer value from environment variable.
    
    Args:
        key: Environment variable name
        default: Default value if not set
        
    Returns:
        Integer value
    """
    try:
        return int(os.getenv(key, default))
    except ValueError:
        return default


def _get_str(key: str, default: str) -> str:
    """
    Get string value from environment variable.
    
    Args:
        key: Environment variable name
        default: Default value if not set
        
    Returns:
        String value
    """
    return os.getenv(key, default)


def _get_list(key: str, default: List[str]) -> List[str]:
    """
    Get list value from environment variable.
    
    Args:
        key: Environment variable name
        default: Default list if not set
        
    Returns:
        List of strings
    """
    value = os.getenv(key)
    if value:
        return [item.strip() for item in value.split(',')]
    return default


# Configuration dictionary
CONFIG = {
    # Yahoo Finance FOREX settings
    "yahoo_forex_enabled": _get_bool("YAHOO_FOREX_ENABLED", True),
    "yahoo_news_limit": _get_int("YAHOO_NEWS_LIMIT", 10),
    "yahoo_cache_duration": _get_int("YAHOO_CACHE_DURATION", 300),
    "forex_pairs": _get_list("FOREX_PAIRS", ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "NZDUSD", "USDCHF"]),
    
    # OpenRouter LLM settings
    "openrouter_api_key": _get_str("OPENROUTER_API_KEY", ""),
    "openrouter_base_url": _get_str("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    "openrouter_referer": _get_str("OPENROUTER_REFERER", "https://github.com/nazimboudeffa/openclaw-yahoo-finance-forex"),
    "openrouter_app_title": _get_str("OPENROUTER_APP_TITLE", "OpenClaw FOREX Bot"),
    "llm_model": _get_str("LLM_MODEL", "anthropic/claude-3-5-sonnet"),
    
    # Optional settings
    "taapi_api_key": _get_str("TAAPI_API_KEY", ""),
    "sanitize_model": _get_str("SANITIZE_MODEL", "openai/gpt-4o"),
}
