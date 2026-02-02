# OpenClaw Yahoo Finance FOREX Skill 💱

A native OpenClaw skill that provides real-time FOREX news analysis and market data from Yahoo Finance for 7 major currency pairs.

## Overview

This skill enables OpenClaw (an AI assistant with a TypeScript/Node.js skill system) to fetch and analyze FOREX market data and news. It uses Yahoo Finance as the data source and provides sentiment analysis based on news headlines.

## Features

✅ **Real-time FOREX News** - Fetches latest news articles from Yahoo Finance  
✅ **7 Major Currency Pairs** - Supports EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD, NZD/USD  
✅ **Sentiment Analysis** - Keyword-based sentiment scoring (bullish/bearish)  
✅ **Market Data** - Current exchange rates and 24h price changes  
✅ **Trading Recommendations** - BUY/SELL/HOLD based on sentiment  
✅ **JSON Output** - Easy to parse programmatically  

## Supported Currency Pairs

| Pair | Name | Symbol | Nickname |
|------|------|--------|----------|
| EUR/USD 🇪🇺🇺🇸 | Euro Dollar | EURUSD=X | Fiber |
| GBP/USD 🇬🇧🇺🇸 | Pound Dollar | GBPUSD=X | Cable |
| USD/JPY 🇺🇸🇯🇵 | Dollar Yen | USDJPY=X | Gopher |
| USD/CHF 🇺🇸🇨🇭 | Dollar Franc | USDCHF=X | Swissy |
| AUD/USD 🇦🇺🇺🇸 | Aussie Dollar | AUDUSD=X | Aussie |
| USD/CAD 🇺🇸🇨🇦 | Dollar Loonie | USDCAD=X | Loonie |
| NZD/USD 🇳🇿🇺🇸 | Kiwi Dollar | NZDUSD=X | Kiwi |

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install yfinance>=0.2.40
```

### OpenClaw Integration

If using with OpenClaw, the skill will be automatically discovered when placed in the skills directory. OpenClaw will handle dependency installation based on the metadata in `SKILL.md`.

## Quick Start

### Basic Usage

Fetch EUR/USD news and sentiment:

```bash
python3 scripts/fetch_forex_news.py EURUSD --limit 10
```

### Example Output

```json
{
  "pair": "EURUSD",
  "symbol": "EURUSD=X",
  "current_rate": 1.10250,
  "change_pct": 0.136,
  "news_count": 5,
  "news": [
    {
      "title": "ECB maintains hawkish stance on rates",
      "publisher": "Reuters",
      "published": "2026-02-02 14:30:00",
      "link": "https://finance.yahoo.com/news/..."
    }
  ],
  "sentiment": {
    "pair_sentiment": 3,
    "recommendation": "BUY",
    "analysis": "Sentiment is bullish based on keyword analysis"
  },
  "timestamp": "2026-02-02 15:45:23"
}
```

### More Examples

```bash
# Get GBP/USD with pretty-printed output
python3 scripts/fetch_forex_news.py GBPUSD --limit 8 --pretty

# Check USD/JPY sentiment
python3 scripts/fetch_forex_news.py USDJPY --limit 5

# Analyze AUD/USD
python3 scripts/fetch_forex_news.py AUDUSD --limit 15
```

## Usage with OpenClaw

When a user asks OpenClaw about FOREX:

**User:** "What's happening with EUR/USD?"

**OpenClaw's Workflow:**
1. Recognizes FOREX query
2. Activates this skill
3. Runs: `python3 scripts/fetch_forex_news.py EURUSD --limit 8`
4. Parses JSON output
5. Provides analysis:

```
EUR/USD is currently at 1.10250, up 0.136% today.

Recent News:
• ECB maintains hawkish stance on rates (Reuters, 2h ago)
• Euro strengthens on strong PMI data (Bloomberg, 3h ago)

Sentiment: BULLISH (+3) - Recommendation: BUY

The euro is showing strength driven by hawkish ECB comments
and positive economic data. Bullish momentum is present.
```

## Documentation

- **[SKILL.md](SKILL.md)** - Main skill file for OpenClaw (LLM instructions)
- **[references/api-examples.md](references/api-examples.md)** - Detailed usage examples
- **[references/forex-pairs.md](references/forex-pairs.md)** - Complete pairs reference
- **[references/sentiment-guide.md](references/sentiment-guide.md)** - Sentiment methodology

## Sentiment Analysis

The skill uses keyword-based sentiment analysis:

**Bullish Keywords:** strengthens, rallies, hawkish, rate hike, growth  
**Bearish Keywords:** weakens, falls, dovish, rate cut, recession

**Scoring:**
- Score > +2: Bullish → BUY recommendation
- Score -2 to +2: Neutral → HOLD recommendation
- Score < -2: Bearish → SELL recommendation

See [sentiment-guide.md](references/sentiment-guide.md) for detailed methodology.

## Project Structure

```
openclaw-yahoo-finance-forex/
├── SKILL.md                      # OpenClaw skill definition (main file)
├── README.md                     # User documentation (this file)
├── package.json                  # NPM metadata
├── .gitignore                    # Git ignore patterns
├── scripts/
│   └── fetch_forex_news.py       # Data fetching script
└── references/
    ├── api-examples.md           # Usage examples
    ├── forex-pairs.md            # Pairs reference
    └── sentiment-guide.md        # Sentiment methodology
```

## Limitations

- News data may have 1-5 minute delays
- Sentiment is keyword-based, not deep NLP
- Historical data typically limited to last 7-14 days
- No real-time tick data (only periodic updates)
- Depends on Yahoo Finance API availability

## Troubleshooting

### Script fails to run
- Ensure Python 3.7+ is installed: `python3 --version`
- Install yfinance: `pip install yfinance>=0.2.40`

### No news returned
- Check internet connection
- Verify pair symbol is correct
- Try a different pair
- Reduce the limit parameter

### Rate data is null
- Yahoo Finance API may be temporarily unavailable
- Market may be closed (weekends, holidays)
- Try again in a few minutes

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Development

1. Clone the repository
2. Install dependencies: `pip install yfinance>=0.2.40`
3. Make your changes
4. Test with: `python3 scripts/fetch_forex_news.py EURUSD --limit 5`
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Author

Nazim Boudeffa

## Links

- **GitHub:** https://github.com/nazimboudeffa/openclaw-yahoo-finance-forex
- **Issues:** https://github.com/nazimboudeffa/openclaw-yahoo-finance-forex/issues
- **OpenClaw:** https://github.com/openclaw (hypothetical link)

## Acknowledgments

- Yahoo Finance for providing free FOREX data
- yfinance library for Python API
- OpenClaw framework for the skill system
