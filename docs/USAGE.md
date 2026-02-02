# Usage Guide

Complete API reference and usage examples for the Yahoo Finance FOREX skill.

## Table of Contents

1. [Quick Start](#quick-start)
2. [YahooFinanceForexSkill API](#yahoofinanceforexskill-api)
3. [Utility Functions](#utility-functions)
4. [TradingAgent API](#tradingagent-api)
5. [Code Examples](#code-examples)
6. [Best Practices](#best-practices)

## Quick Start

### Basic Usage

```python
from skills.yahoo_finance_forex_majors import YahooFinanceForexSkill

# Initialize skill
skill = YahooFinanceForexSkill()

# Execute for EUR/USD
result = skill.execute("EURUSD", news_limit=10)

if result['success']:
    print("Market Data:", result['raw_data']['market_data'])
    print("News:", result['raw_data']['news'])
    print("LLM Context:", result['llm_context'])
else:
    print("Error:", result['error'])
```

## YahooFinanceForexSkill API

### Class: `YahooFinanceForexSkill`

Main class for Yahoo Finance FOREX integration.

#### Attributes

```python
# Class attributes
name: str = "yahoo_finance_forex"
description: str = "Fetches forex pair data, news, and market sentiment from Yahoo Finance"
FOREX_PAIRS: Dict[str, str]  # Mapping of pairs to Yahoo symbols
CURRENCY_INFO: Dict[str, Dict]  # Currency metadata
MAJOR_PAIRS: List[str]  # List of 7 major pairs

# Instance attributes
cache: Dict[str, Tuple[Any, float]]  # Response cache
cache_duration: int = 300  # Cache TTL in seconds
```

#### Methods

### `__init__()`

Initialize the skill.

```python
skill = YahooFinanceForexSkill()
```

---

### `parse_forex_pair(pair: str) -> Tuple[str, str]`

Parse and validate a FOREX pair string.

**Parameters:**
- `pair` (str): FOREX pair (e.g., "EURUSD", "EUR/USD", "EURUSD=X")

**Returns:**
- `Tuple[str, str]`: (base_currency, quote_currency)

**Raises:**
- `ValueError`: If pair is invalid or not a major pair

**Example:**
```python
base, quote = skill.parse_forex_pair("EURUSD")
# Returns: ("EUR", "USD")

base, quote = skill.parse_forex_pair("EUR/USD")
# Returns: ("EUR", "USD")

skill.parse_forex_pair("INVALID")
# Raises: ValueError
```

---

### `get_yahoo_symbol(pair: str) -> str`

Convert FOREX pair to Yahoo Finance symbol format.

**Parameters:**
- `pair` (str): FOREX pair string

**Returns:**
- `str`: Yahoo Finance symbol (e.g., "EURUSD=X")

**Raises:**
- `ValueError`: If pair is not supported

**Example:**
```python
symbol = skill.get_yahoo_symbol("EURUSD")
# Returns: "EURUSD=X"
```

---

### `fetch_news(pair: str, limit: int = 10) -> List[Dict]`

Fetch news articles for a FOREX pair.

**Parameters:**
- `pair` (str): FOREX pair
- `limit` (int): Maximum news articles (default: 10)

**Returns:**
- `List[Dict]`: List of news articles with keys:
  - `title` (str): Article headline
  - `publisher` (str): News source
  - `link` (str): Article URL
  - `published` (str): Publication timestamp

**Example:**
```python
news = skill.fetch_news("EURUSD", limit=5)
for article in news:
    print(f"{article['title']} - {article['publisher']}")
```

---

### `fetch_market_data(pair: str, period: str = "5d") -> Dict`

Fetch market data for a FOREX pair.

**Parameters:**
- `pair` (str): FOREX pair
- `period` (str): Time period (default: "5d")
  - Options: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"

**Returns:**
- `Dict`: Market data with keys:
  - `pair` (str): Pair name
  - `current_rate` (float): Current exchange rate
  - `prev_close` (float): Previous close
  - `change` (float): Absolute change
  - `change_pct` (float): Percentage change
  - `high` (float): Period high
  - `low` (float): Period low
  - `support` (float): Support level
  - `resistance` (float): Resistance level
  - `volatility` (float): ATR approximation
  - `position_in_range` (float): Position in range (0-100%)
  - `base_currency` (str): Base currency code
  - `quote_currency` (str): Quote currency code
  - `base_info` (Dict): Base currency metadata
  - `quote_info` (Dict): Quote currency metadata

**Example:**
```python
data = skill.fetch_market_data("EURUSD")
print(f"Current: {data['current_rate']:.5f}")
print(f"Change: {data['change_pct']:+.2f}%")
print(f"Support: {data['support']:.5f}")
print(f"Resistance: {data['resistance']:.5f}")
```

---

### `calculate_pip_value(pair: str, lot_size: float = 1.0) -> Dict`

Calculate pip value for a FOREX pair.

**Parameters:**
- `pair` (str): FOREX pair
- `lot_size` (float): Lot size (default: 1.0 standard lot)

**Returns:**
- `Dict`: Pip calculation with keys:
  - `pip_size` (float): Pip size (0.01 for JPY, 0.0001 for others)
  - `pip_value_usd` (float): Pip value in USD
  - `lot_size` (float): Lot size used
  - `units` (float): Number of units

**Example:**
```python
pip_info = skill.calculate_pip_value("EURUSD", lot_size=1.0)
print(f"Pip value: ${pip_info['pip_value_usd']:.2f}")

# For mini lot (0.1)
pip_info = skill.calculate_pip_value("EURUSD", lot_size=0.1)
print(f"Pip value (mini): ${pip_info['pip_value_usd']:.2f}")
```

---

### `format_for_llm(pair: str, news_limit: int = 10, include_technicals: bool = True) -> str`

Format FOREX data for LLM consumption.

**Parameters:**
- `pair` (str): FOREX pair
- `news_limit` (int): Number of news articles (default: 10)
- `include_technicals` (bool): Include technical context (default: True)

**Returns:**
- `str`: Formatted multiline string ready for LLM

**Example:**
```python
context = skill.format_for_llm("EURUSD", news_limit=5)
print(context)
```

Output:
```
======================================================================
📊 🇪🇺 EURUSD 🇺🇸 - Yahoo Finance Data
======================================================================

💹 MARKET DATA:
  Current Rate: 1.10250
  Change: +0.00150 (+0.14%)
  High: 1.10500
  Low: 1.09800
  ...
```

---

### `execute(pair: str, **kwargs) -> Dict`

Main execution method called by OpenClaw.

**Parameters:**
- `pair` (str): FOREX pair
- `**kwargs`: Optional parameters
  - `news_limit` (int): Number of news articles
  - `include_technicals` (bool): Include technical analysis

**Returns:**
- `Dict`: Result dictionary with keys:
  - `success` (bool): Success status
  - `llm_context` (str): Formatted context string
  - `raw_data` (Dict): Raw data with keys:
    - `news` (List[Dict]): News articles
    - `market_data` (Dict): Market data
    - `pip_info` (Dict): Pip calculation
  - `metadata` (Dict): Metadata with keys:
    - `skill_name` (str): Skill identifier
    - `timestamp` (str): ISO timestamp
    - `pair` (str): Pair analyzed
    - `news_count` (int): Number of news articles
  - `error` (str): Error message (if failed)

**Example:**
```python
result = skill.execute("EURUSD", news_limit=10, include_technicals=True)

if result['success']:
    # Use in LLM prompt
    llm_prompt = f"Analyze this data: {result['llm_context']}"
    
    # Access raw data
    rate = result['raw_data']['market_data']['current_rate']
    news_count = len(result['raw_data']['news'])
    
    print(f"Rate: {rate}, News: {news_count}")
else:
    print(f"Error: {result['error']}")
```

---

### `get_all_majors_overview() -> List[Dict]`

Get overview data for all major pairs.

**Returns:**
- `List[Dict]`: List of summary dicts with keys:
  - `pair` (str): Pair name
  - `rate` (float): Current rate
  - `change_pct` (float): Percentage change
  - `volatility` (float): Volatility measure
  - `position_in_range` (float): Position in range (%)

**Example:**
```python
overview = skill.get_all_majors_overview()
for data in overview:
    print(f"{data['pair']}: {data['rate']:.5f} ({data['change_pct']:+.2f}%)")
```

## Utility Functions

### `get_forex_sentiment(news: List[Dict], base_currency: str, quote_currency: str) -> Dict`

Analyze sentiment from news articles.

**Parameters:**
- `news` (List[Dict]): List of news articles
- `base_currency` (str): Base currency code (e.g., "EUR")
- `quote_currency` (str): Quote currency code (e.g., "USD")

**Returns:**
- `Dict`: Sentiment analysis with keys:
  - `base_bullish` (int): Bullish mentions for base
  - `base_bearish` (int): Bearish mentions for base
  - `quote_bullish` (int): Bullish mentions for quote
  - `quote_bearish` (int): Bearish mentions for quote
  - `pair_sentiment` (int): Overall pair sentiment score
  - `recommendation` (str): "BUY", "SELL", or "NEUTRAL"

**Example:**
```python
from skills.yahoo_finance_forex_majors import get_forex_sentiment

news = skill.fetch_news("EURUSD")
sentiment = get_forex_sentiment(news, "EUR", "USD")

print(f"Sentiment: {sentiment['pair_sentiment']:+d}")
print(f"Recommendation: {sentiment['recommendation']}")
```

**Sentiment Logic:**
- Base strengthens OR Quote weakens → Pair up (Bullish)
- Base weakens OR Quote strengthens → Pair down (Bearish)
- Score > 2 → BUY
- Score < -2 → SELL
- Otherwise → NEUTRAL

---

### `register_skill() -> YahooFinanceForexSkill`

Register and return skill instance.

**Returns:**
- `YahooFinanceForexSkill`: Skill instance

**Example:**
```python
from skills.yahoo_finance_forex_majors import register_skill

skill = register_skill()
```

## TradingAgent API

### Class: `TradingAgent`

Trading agent with LLM integration.

#### Methods

### `__init__()`

Initialize the trading agent.

```python
from src.backend.agent.decision_maker import TradingAgent

agent = TradingAgent()
```

---

### `async make_decision(assets: List[str], market_sections: List[Dict], dashboard: Dict) -> Dict`

Make trading decision using LLM.

**Parameters:**
- `assets` (List[str]): List of FOREX pairs
- `market_sections` (List[Dict]): Technical indicators per asset
- `dashboard` (Dict): Account and performance data

**Returns:**
- `Dict`: Decision with keys:
  - `reasoning` (str): LLM reasoning
  - `trade_decisions` (List[Dict]): List of trade decisions

**Example:**
```python
import asyncio

async def main():
    agent = TradingAgent()
    
    decision = await agent.make_decision(
        assets=['EURUSD', 'GBPUSD'],
        market_sections=[
            {
                'asset': 'EURUSD',
                'current_price': 1.1000,
                'indicators': {
                    'intraday': {'ema20': 1.0980, 'rsi14': 55},
                    'long_term': {'ema20': 1.0950}
                }
            }
        ],
        dashboard={
            'balance': 10000,
            'account_value': 10500,
            'positions': []
        }
    )
    
    print(decision['reasoning'])
    for trade in decision['trade_decisions']:
        print(f"{trade['asset']}: {trade['action']}")

asyncio.run(main())
```

## Code Examples

### Example 1: Basic Data Fetch

```python
from skills.yahoo_finance_forex_majors import YahooFinanceForexSkill

skill = YahooFinanceForexSkill()

# Fetch EUR/USD data
result = skill.execute("EURUSD")

if result['success']:
    data = result['raw_data']['market_data']
    print(f"EUR/USD: {data['current_rate']:.5f}")
    print(f"Change: {data['change_pct']:+.2f}%")
    print(f"Volatility: {data['volatility']:.5f}")
```

### Example 2: News Analysis

```python
from skills.yahoo_finance_forex_majors import YahooFinanceForexSkill, get_forex_sentiment

skill = YahooFinanceForexSkill()

# Fetch news
news = skill.fetch_news("GBPUSD", limit=10)

# Analyze sentiment
sentiment = get_forex_sentiment(news, "GBP", "USD")

print(f"News articles: {len(news)}")
print(f"Sentiment score: {sentiment['pair_sentiment']:+d}")
print(f"Recommendation: {sentiment['recommendation']}")
```

### Example 3: Multiple Pairs Comparison

```python
from skills.yahoo_finance_forex_majors import YahooFinanceForexSkill

skill = YahooFinanceForexSkill()

pairs = ['EURUSD', 'GBPUSD', 'USDJPY']

for pair in pairs:
    data = skill.fetch_market_data(pair)
    if data:
        print(f"{pair}: {data['current_rate']:.5f} ({data['change_pct']:+.2f}%)")
```

### Example 4: Custom Trading Logic

```python
from skills.yahoo_finance_forex_majors import YahooFinanceForexSkill, get_forex_sentiment

skill = YahooFinanceForexSkill()

def should_buy(pair):
    """Custom trading logic."""
    # Fetch data
    result = skill.execute(pair)
    if not result['success']:
        return False
    
    data = result['raw_data']['market_data']
    news = result['raw_data']['news']
    
    # Analyze sentiment
    base, quote = skill.parse_forex_pair(pair)
    sentiment = get_forex_sentiment(news, base, quote)
    
    # Decision logic
    if (data['position_in_range'] < 30 and  # Near support
        sentiment['recommendation'] == 'BUY' and
        data['volatility'] < 0.01):  # Low volatility
        return True
    
    return False

# Test
if should_buy('EURUSD'):
    print("🟢 BUY signal for EUR/USD")
else:
    print("🔴 No BUY signal")
```

### Example 5: Full Bot Integration

```python
import asyncio
from src.backend.agent.decision_maker import TradingAgent
from src.backend.config_loader import CONFIG

async def trading_cycle():
    """One trading cycle."""
    agent = TradingAgent()
    pairs = CONFIG['forex_pairs']
    
    # Build market sections (placeholder)
    market_sections = [
        {'asset': pair, 'current_price': 1.1, 'indicators': {}}
        for pair in pairs
    ]
    
    # Dashboard data
    dashboard = {
        'balance': 10000,
        'account_value': 10000,
        'positions': []
    }
    
    # Make decision
    decision = await agent.make_decision(pairs, market_sections, dashboard)
    
    # Process decisions
    for trade in decision['trade_decisions']:
        print(f"{trade['asset']}: {trade['action']}")
        # Execute trade here...

asyncio.run(trading_cycle())
```

## Best Practices

### 1. Caching

The skill caches responses for 5 minutes by default. Adjust if needed:

```python
skill = YahooFinanceForexSkill()
skill.cache_duration = 600  # 10 minutes
```

### 2. Error Handling

Always check for success:

```python
result = skill.execute("EURUSD")
if result['success']:
    # Process data
    pass
else:
    # Handle error
    print(f"Error: {result['error']}")
```

### 3. Rate Limiting

Yahoo Finance has rate limits. Use caching and avoid excessive calls:

```python
# Good: Fetch once, use multiple times
result = skill.execute("EURUSD")
data = result['raw_data']['market_data']
news = result['raw_data']['news']

# Bad: Fetching repeatedly
skill.fetch_market_data("EURUSD")
skill.fetch_news("EURUSD")
skill.fetch_market_data("EURUSD")  # Unnecessary
```

### 4. Pair Validation

Always validate pairs before use:

```python
try:
    base, quote = skill.parse_forex_pair(user_input)
    # Proceed with valid pair
except ValueError as e:
    print(f"Invalid pair: {e}")
```

### 5. Sentiment Analysis

Use sentiment as one signal among many:

```python
sentiment = get_forex_sentiment(news, "EUR", "USD")

# Don't rely solely on sentiment
if sentiment['recommendation'] == 'BUY' and other_conditions:
    # Execute trade
    pass
```

### 6. Async Usage

Always use async for the trading agent:

```python
# Good
decision = await agent.make_decision(...)

# Bad - will not work
decision = agent.make_decision(...)  # Missing await
```

### 7. Testing

Test with different pairs before going live:

```python
test_pairs = ['EURUSD', 'GBPUSD', 'USDJPY']

for pair in test_pairs:
    result = skill.execute(pair)
    assert result['success'], f"Failed for {pair}"
```

---

**Ready to integrate?** → Check [Integration Guide](INTEGRATION.md) for setup instructions
