# Integration Guide

This guide walks you through integrating the Yahoo Finance FOREX skill into OpenClaw bot.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [File-by-File Setup](#file-by-file-setup)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software
- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### API Keys
- **OpenRouter API Key** - Get one at [openrouter.ai](https://openrouter.ai)
  - Required for LLM-powered trading decisions
  - Supports multiple LLM providers (Anthropic, OpenAI, etc.)
  
- **TAAPI API Key** (Optional) - Get one at [taapi.io](https://taapi.io)
  - For advanced technical indicators
  - Not required for basic functionality

### System Requirements
- **Memory**: 512MB minimum (1GB recommended)
- **Disk Space**: 100MB for code + dependencies
- **Network**: Stable internet connection for API calls

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/nazimboudeffa/openclaw-yahoo-finance-forex.git
cd openclaw-yahoo-finance-forex
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `yfinance` - Yahoo Finance API wrapper
- `python-dotenv` - Environment variable management
- `requests` - HTTP library for API calls
- `asyncio` - Async programming support

### Step 4: Verify Installation

```bash
python -c "import yfinance; print('✅ yfinance installed')"
python -c "import dotenv; print('✅ python-dotenv installed')"
python -c "import requests; print('✅ requests installed')"
```

## Configuration

### Step 1: Create Environment File

```bash
cp .env.example .env
```

### Step 2: Edit Configuration

Open `.env` in your favorite text editor and configure:

```bash
# Yahoo Finance FOREX Skill
YAHOO_FOREX_ENABLED=true           # Enable the skill
YAHOO_NEWS_LIMIT=10                # Number of news articles (5-20 recommended)
YAHOO_CACHE_DURATION=300           # Cache duration in seconds (5 min default)
FOREX_PAIRS=EURUSD,GBPUSD,USDJPY,AUDUSD  # Pairs to trade

# OpenRouter LLM
OPENROUTER_API_KEY=sk-or-v1-xxxxx  # ⚠️ REQUIRED: Add your API key here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_REFERER=https://github.com/nazimboudeffa/openclaw-yahoo-finance-forex
OPENROUTER_APP_TITLE=OpenClaw FOREX Bot
LLM_MODEL=anthropic/claude-3-5-sonnet  # Choose your model

# Optional
TAAPI_API_KEY=your-taapi-key       # Optional: For technical indicators
SANITIZE_MODEL=openai/gpt-4o       # Optional: For content sanitization
```

### Configuration Options Explained

#### FOREX_PAIRS
Comma-separated list of pairs to trade. Supported:
- `EURUSD` - Euro / US Dollar
- `GBPUSD` - British Pound / US Dollar
- `USDJPY` - US Dollar / Japanese Yen
- `USDCHF` - US Dollar / Swiss Franc
- `AUDUSD` - Australian Dollar / US Dollar
- `USDCAD` - US Dollar / Canadian Dollar
- `NZDUSD` - New Zealand Dollar / US Dollar

#### LLM_MODEL
Choose from available OpenRouter models:
- `anthropic/claude-3-5-sonnet` - Recommended for best reasoning
- `anthropic/claude-3-haiku` - Faster, more affordable
- `openai/gpt-4-turbo` - Alternative high-quality option
- `openai/gpt-3.5-turbo` - Budget-friendly option

## File-by-File Setup

### 1. Skills Module (`skills/`)

**`skills/yahoo_finance_forex_majors.py`**
- Core skill implementation
- Already created - no changes needed
- Contains `YahooFinanceForexSkill` class

**`skills/__init__.py`**
- Skill registry
- Already created - no changes needed
- Exports `get_skill()` and `get_available_skills()`

### 2. Backend Module (`src/backend/`)

**`src/backend/config_loader.py`**
- Configuration management
- Already created - no changes needed
- Loads settings from `.env` file

**`src/backend/agent/decision_maker.py`**
- Trading agent with LLM integration
- Already created - no changes needed
- Contains `TradingAgent` class

### 3. Main Application (`src/`)

**`src/main.py`**
- Main bot entry point
- Already created - no changes needed
- Runs the trading loop

### 4. Tests (`tests/`)

**`tests/test_integration.py`**
- Integration tests
- Already created - no changes needed
- Verifies all components work together

## Testing

### Test 1: Verify Skill Loading

```bash
python -c "from skills import get_skill; skill = get_skill('yahoo_finance_forex'); print('✅ Skill loaded' if skill else '❌ Skill not loaded')"
```

Expected output: `✅ Skill loaded`

### Test 2: Test Data Fetch

```bash
python -c "
from skills.yahoo_finance_forex_majors import YahooFinanceForexSkill
skill = YahooFinanceForexSkill()
result = skill.execute('EURUSD', news_limit=5)
print('✅ Success' if result['success'] else f'❌ Error: {result.get(\"error\")}')"
```

Expected output: `✅ Success`

### Test 3: Run Full Integration Test

```bash
python tests/test_integration.py
```

Expected output:
```
🧪 Testing FOREX Skill Integration
==================================================
✅ FOREX skill loaded successfully
✅ Data fetched successfully
✅ Retrieved data for 7 pairs
✅ Decision received
✅ Integration test complete!
```

### Test 4: Run Main Bot (Dry Run)

```bash
# This will run one cycle and then you can stop it with Ctrl+C
timeout 60 python src/main.py
```

Expected output:
```
🚀 Starting OpenClaw FOREX Bot
📊 Trading pairs: EURUSD, GBPUSD, USDJPY, AUDUSD
🤖 LLM Model: anthropic/claude-3-5-sonnet
🔄 Starting trading cycle #1
💭 REASONING: [LLM reasoning here]
🎯 TRADE DECISIONS: [Trade decisions here]
```

## Troubleshooting

### Issue: "yfinance not available"

**Solution:**
```bash
pip install yfinance>=0.2.40
```

### Issue: "No module named 'dotenv'"

**Solution:**
```bash
pip install python-dotenv>=1.0.0
```

### Issue: "OpenRouter API key not configured"

**Solution:**
1. Check that `.env` file exists
2. Verify `OPENROUTER_API_KEY` is set
3. Key should start with `sk-or-v1-`
4. No quotes around the key value

### Issue: "No historical data available for pair"

**Possible Causes:**
- Market is closed (try during trading hours)
- Yahoo Finance API is down
- Pair name is incorrect

**Solution:**
```bash
# Test with a different pair
python -c "
from skills.yahoo_finance_forex_majors import YahooFinanceForexSkill
skill = YahooFinanceForexSkill()
result = skill.execute('GBPUSD', news_limit=5)
print(result)"
```

### Issue: "Rate limit exceeded"

**Solution:**
- The skill includes 5-minute caching by default
- Increase `YAHOO_CACHE_DURATION` in `.env`
- Reduce `YAHOO_NEWS_LIMIT` to fetch less data

### Issue: "LLM returns invalid JSON"

**Solution:**
1. Check your OpenRouter API key is valid
2. Try a different model (e.g., `anthropic/claude-3-haiku`)
3. Check OpenRouter credits/balance
4. The bot has fallback logic to HOLD on errors

## Next Steps

1. ✅ Complete installation and configuration
2. ✅ Run all tests successfully
3. 📖 Read [Usage Guide](USAGE.md) for API reference
4. 🚀 Start the bot: `python src/main.py`
5. 📊 Monitor performance and adjust configuration
6. 🔧 Integrate with your trading platform (e.g., MetaTrader)

## Additional Resources

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [Yahoo Finance API](https://finance.yahoo.com/)

## Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review logs for error messages
3. Open an issue on GitHub with:
   - Python version (`python --version`)
   - Error message and full traceback
   - Steps to reproduce

---

**Ready to trade?** → Continue to [Usage Guide](USAGE.md)
