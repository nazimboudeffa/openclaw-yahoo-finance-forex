# OpenClaw Yahoo Finance FOREX Skill

🚀 **Professional FOREX Trading Bot with Yahoo Finance Integration**

A complete trading system that combines real-time Yahoo Finance data with LLM-powered decision-making for automated FOREX trading.

## ✨ Features

- 📊 **Real-time FOREX Data**: Fetches live market data from Yahoo Finance
- 📰 **News Analysis**: Aggregates and analyzes financial news for sentiment
- 🤖 **LLM Decision Making**: Uses advanced AI models for trading decisions
- 🎯 **7 Major Pairs**: Supports the most liquid FOREX pairs
- ⚡ **Smart Caching**: 5-minute cache to optimize API usage
- 🔒 **Risk Management**: Built-in position sizing and stop-loss logic
- 📈 **Technical Analysis**: Integration-ready for indicators (EMA, RSI, MACD)

## 🌍 Supported Major Currency Pairs

| Pair | Symbol | Description |
|------|--------|-------------|
| 🇪🇺🇺🇸 EUR/USD | EURUSD=X | Euro / US Dollar |
| 🇬🇧🇺🇸 GBP/USD | GBPUSD=X | British Pound / US Dollar |
| 🇺🇸🇯🇵 USD/JPY | USDJPY=X | US Dollar / Japanese Yen |
| 🇺🇸🇨🇭 USD/CHF | USDCHF=X | US Dollar / Swiss Franc |
| 🇦🇺🇺🇸 AUD/USD | AUDUSD=X | Australian Dollar / US Dollar |
| 🇺🇸🇨🇦 USD/CAD | USDCAD=X | US Dollar / Canadian Dollar |
| 🇳🇿🇺🇸 NZD/USD | NZDUSD=X | New Zealand Dollar / US Dollar |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenRouter API key (for LLM access)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/nazimboudeffa/openclaw-yahoo-finance-forex.git
cd openclaw-yahoo-finance-forex
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

4. **Run the bot:**
```bash
python src/main.py
```

### Basic Usage Example

```python
from skills.yahoo_finance_forex_majors import YahooFinanceForexSkill

# Initialize skill
skill = YahooFinanceForexSkill()

# Fetch data for EUR/USD
result = skill.execute("EURUSD", news_limit=10)

if result['success']:
    print(result['llm_context'])  # Formatted for LLM
    print(f"Current rate: {result['raw_data']['market_data']['current_rate']}")
    print(f"News count: {len(result['raw_data']['news'])}")
```

## ⚙️ Configuration

Edit `.env` file to customize:

```bash
# Yahoo Finance Settings
YAHOO_FOREX_ENABLED=true          # Enable/disable Yahoo Finance skill
YAHOO_NEWS_LIMIT=10               # Number of news articles to fetch
YAHOO_CACHE_DURATION=300          # Cache duration in seconds (5 min)
FOREX_PAIRS=EURUSD,GBPUSD,USDJPY  # Pairs to trade

# LLM Settings
OPENROUTER_API_KEY=your-key       # Your OpenRouter API key
LLM_MODEL=anthropic/claude-3-5-sonnet  # Model to use
```

## 📚 Documentation

- **[Integration Guide](docs/INTEGRATION.md)** - Step-by-step integration instructions
- **[Usage Guide](docs/USAGE.md)** - API reference and code examples

## 🧪 Testing

Run the integration test to verify setup:

```bash
python tests/test_integration.py
```

Expected output:
```
✅ FOREX skill loaded successfully
✅ Data fetched successfully
✅ Decision received from LLM
✅ Integration test complete!
```

## 🏗️ Architecture

```
openclaw-yahoo-finance-forex/
├── skills/                          # Skills modules
│   ├── __init__.py                 # Skill registry
│   └── yahoo_finance_forex_majors.py  # Yahoo Finance skill
├── src/
│   ├── backend/
│   │   ├── config_loader.py        # Configuration management
│   │   └── agent/
│   │       └── decision_maker.py   # LLM trading agent
│   └── main.py                     # Main bot entry point
├── tests/
│   └── test_integration.py         # Integration tests
└── docs/                           # Documentation
```

## 🔧 Key Components

### 1. Yahoo Finance FOREX Skill
- Fetches real-time data from Yahoo Finance
- Analyzes news sentiment
- Calculates technical indicators
- Formats data for LLM consumption

### 2. Trading Agent
- Integrates Yahoo Finance data with technical indicators
- Makes LLM-powered trading decisions
- Implements risk management rules
- Provides detailed reasoning for each trade

### 3. Main Bot Loop
- Runs continuous trading cycles
- Logs all decisions and actions
- Handles errors gracefully
- Supports multiple currency pairs

## 🛡️ Risk Management

The bot implements several safety features:

- **Position Sizing**: Max 2% risk per trade
- **Stop Loss**: Always set at key levels
- **Take Profit**: Minimum 2:1 reward-to-risk
- **Max Positions**: 3-4 simultaneous positions
- **Diversification**: Max 30% in single currency

## 📊 Data Sources

- **Yahoo Finance**: Market data and news (via yfinance)
- **OpenRouter**: LLM models for decision-making
- **TAAPI** (optional): Additional technical indicators

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Yahoo Finance for providing free market data
- OpenRouter for LLM API access
- The OpenClaw community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/nazimboudeffa/openclaw-yahoo-finance-forex/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nazimboudeffa/openclaw-yahoo-finance-forex/discussions)

## ⚠️ Disclaimer

**This software is for educational purposes only. Trading FOREX carries significant risk. Never trade with money you cannot afford to lose. Always do your own research and consider consulting with a financial advisor.**

---

Made with ❤️ for the OpenClaw community
