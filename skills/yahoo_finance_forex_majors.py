"""
Yahoo Finance FOREX Skill for OpenClaw

Fetches real-time FOREX news and market data from Yahoo Finance,
analyzes sentiment for major currency pairs, and integrates with
OpenClaw's decision-making system.
"""

import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("⚠️ yfinance not available. Install with: pip install yfinance")


class YahooFinanceForexSkill:
    """Yahoo Finance FOREX skill for major currency pairs."""
    
    name = "yahoo_finance_forex"
    description = "Fetches forex pair data, news, and market sentiment from Yahoo Finance"
    
    # Yahoo Finance symbols for major FOREX pairs
    FOREX_PAIRS = {
        "EURUSD": "EURUSD=X",
        "GBPUSD": "GBPUSD=X",
        "USDJPY": "USDJPY=X",
        "USDCHF": "USDCHF=X",
        "AUDUSD": "AUDUSD=X",
        "USDCAD": "USDCAD=X",
        "NZDUSD": "NZDUSD=X",
    }
    
    # Currency information
    CURRENCY_INFO = {
        "EUR": {"name": "Euro", "flag": "🇪🇺", "central_bank": "European Central Bank"},
        "GBP": {"name": "British Pound", "flag": "🇬🇧", "central_bank": "Bank of England"},
        "USD": {"name": "US Dollar", "flag": "🇺🇸", "central_bank": "Federal Reserve"},
        "JPY": {"name": "Japanese Yen", "flag": "🇯🇵", "central_bank": "Bank of Japan"},
        "CHF": {"name": "Swiss Franc", "flag": "🇨🇭", "central_bank": "Swiss National Bank"},
        "AUD": {"name": "Australian Dollar", "flag": "🇦🇺", "central_bank": "Reserve Bank of Australia"},
        "CAD": {"name": "Canadian Dollar", "flag": "🇨🇦", "central_bank": "Bank of Canada"},
        "NZD": {"name": "New Zealand Dollar", "flag": "🇳🇿", "central_bank": "Reserve Bank of New Zealand"},
    }
    
    # List of major pairs
    MAJOR_PAIRS = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD"]
    
    def __init__(self):
        """Initialize the Yahoo Finance FOREX skill."""
        self.cache: Dict[str, Tuple[Any, float]] = {}
        self.cache_duration: int = 300  # 5 minutes in seconds
        
    def parse_forex_pair(self, pair: str) -> Tuple[str, str]:
        """
        Parse and validate a FOREX pair string.
        
        Args:
            pair: FOREX pair string (e.g., "EURUSD", "EUR/USD", "EURUSD=X")
            
        Returns:
            Tuple of (base_currency, quote_currency)
            
        Raises:
            ValueError: If pair is invalid or not a major pair
        """
        # Clean the pair string
        pair = pair.upper().replace("/", "").replace("=X", "").strip()
        
        # Validate length (should be 6 characters)
        if len(pair) != 6:
            raise ValueError(f"Invalid pair format: {pair}. Expected 6 characters (e.g., EURUSD)")
        
        # Extract base and quote currencies
        base = pair[:3]
        quote = pair[3:]
        
        # Validate it's a major pair
        if pair not in self.MAJOR_PAIRS:
            raise ValueError(
                f"Pair {pair} is not a supported major pair. "
                f"Supported pairs: {', '.join(self.MAJOR_PAIRS)}"
            )
        
        return base, quote
    
    def get_yahoo_symbol(self, pair: str) -> str:
        """
        Convert a FOREX pair to Yahoo Finance symbol format.
        
        Args:
            pair: FOREX pair string (e.g., "EURUSD", "EUR/USD")
            
        Returns:
            Yahoo Finance symbol (e.g., "EURUSD=X")
            
        Raises:
            ValueError: If pair is not supported
        """
        # Parse and validate the pair
        base, quote = self.parse_forex_pair(pair)
        pair_clean = f"{base}{quote}"
        
        # Get Yahoo symbol from mapping
        if pair_clean not in self.FOREX_PAIRS:
            raise ValueError(
                f"Pair {pair_clean} is not supported. "
                f"Supported pairs: {', '.join(self.MAJOR_PAIRS)}"
            )
        
        return self.FOREX_PAIRS[pair_clean]
    
    def fetch_news(self, pair: str, limit: int = 10) -> List[Dict]:
        """
        Fetch news articles for a FOREX pair.
        
        Args:
            pair: FOREX pair string
            limit: Maximum number of news articles to return
            
        Returns:
            List of news article dictionaries with title, publisher, link, published
        """
        if not YFINANCE_AVAILABLE:
            print("⚠️ yfinance not available, returning empty news list")
            return []
        
        # Check cache first
        cache_key = f"news_{pair}_{limit}"
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if (time.time() - cached_time) < self.cache_duration:
                return cached_data
        
        try:
            # Get Yahoo symbol
            symbol = self.get_yahoo_symbol(pair)
            
            # Fetch ticker data
            ticker = yf.Ticker(symbol)
            news_data = ticker.news if hasattr(ticker, 'news') else []
            
            # If no direct news, try fetching for base and quote currencies
            if not news_data:
                base, quote = self.parse_forex_pair(pair)
                # Try base currency
                try:
                    base_ticker = yf.Ticker(f"{base}=X")
                    news_data.extend(base_ticker.news if hasattr(base_ticker, 'news') else [])
                except Exception as e:
                    print(f"⚠️ Could not fetch news for {base}: {e}")
                # Try quote currency if it's not USD (USD news is usually abundant)
                if quote != "USD":
                    try:
                        quote_ticker = yf.Ticker(f"{quote}=X")
                        news_data.extend(quote_ticker.news if hasattr(quote_ticker, 'news') else [])
                    except Exception as e:
                        print(f"⚠️ Could not fetch news for {quote}: {e}")
            
            # Format news articles
            formatted_news = []
            for article in news_data[:limit]:
                try:
                    formatted_article = {
                        'title': article.get('title', 'N/A'),
                        'publisher': article.get('publisher', 'Unknown'),
                        'link': article.get('link', ''),
                        'published': datetime.fromtimestamp(
                            article.get('providerPublishTime', time.time())
                        ).strftime('%Y-%m-%d %H:%M:%S')
                    }
                    formatted_news.append(formatted_article)
                except Exception as e:
                    print(f"⚠️ Error formatting article: {e}")
                    continue
            
            # Cache results
            self.cache[cache_key] = (formatted_news, time.time())
            
            return formatted_news
            
        except Exception as e:
            print(f"❌ Error fetching news for {pair}: {e}")
            return []
    
    def fetch_market_data(self, pair: str, period: str = "5d") -> Dict:
        """
        Fetch market data for a FOREX pair.
        
        Args:
            pair: FOREX pair string
            period: Time period for historical data (default: "5d")
            
        Returns:
            Dictionary with comprehensive market data
        """
        if not YFINANCE_AVAILABLE:
            print("⚠️ yfinance not available, returning empty market data")
            return {}
        
        # Check cache first
        cache_key = f"market_{pair}_{period}"
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if (time.time() - cached_time) < self.cache_duration:
                return cached_data
        
        try:
            # Get Yahoo symbol
            symbol = self.get_yahoo_symbol(pair)
            
            # Fetch ticker data
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                print(f"⚠️ No historical data available for {pair}")
                return {}
            
            # Calculate market metrics
            current_rate = float(hist['Close'].iloc[-1])
            prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_rate
            change = current_rate - prev_close
            change_pct = (change / prev_close * 100) if prev_close != 0 else 0
            
            # Calculate volatility (ATR approximation)
            high_low_range = hist['High'] - hist['Low']
            volatility = float(high_low_range.mean())
            
            # Support and resistance levels
            support = float(hist['Low'].min())
            resistance = float(hist['High'].max())
            
            # Position in range
            range_size = resistance - support
            position_in_range = ((current_rate - support) / range_size * 100) if range_size != 0 else 50
            
            # Parse currencies
            base, quote = self.parse_forex_pair(pair)
            
            # Build market data dict
            market_data = {
                'pair': pair,
                'current_rate': current_rate,
                'prev_close': prev_close,
                'change': change,
                'change_pct': change_pct,
                'high': float(hist['High'].max()),
                'low': float(hist['Low'].min()),
                'support': support,
                'resistance': resistance,
                'volatility': volatility,
                'position_in_range': position_in_range,
                'base_currency': base,
                'quote_currency': quote,
                'base_info': self.CURRENCY_INFO.get(base, {}),
                'quote_info': self.CURRENCY_INFO.get(quote, {}),
            }
            
            # Cache results
            self.cache[cache_key] = (market_data, time.time())
            
            return market_data
            
        except Exception as e:
            print(f"❌ Error fetching market data for {pair}: {e}")
            return {}
    
    def calculate_pip_value(self, pair: str, lot_size: float = 1.0) -> Dict:
        """
        Calculate pip value for a FOREX pair.
        
        Args:
            pair: FOREX pair string
            lot_size: Lot size (default: 1.0 standard lot = 100,000 units)
            
        Returns:
            Dictionary with pip calculation details
        """
        try:
            # Fetch current market data
            market_data = self.fetch_market_data(pair)
            if not market_data:
                return {}
            
            current_rate = market_data['current_rate']
            base, quote = self.parse_forex_pair(pair)
            
            # Determine pip size
            # JPY pairs have pip size of 0.01, others 0.0001
            pip_size = 0.01 if quote == "JPY" else 0.0001
            
            # Calculate pip value in USD
            # Standard lot = 100,000 units
            units = 100000 * lot_size
            
            if quote == "USD":
                # Quote currency is USD, pip value is straightforward
                pip_value_usd = pip_size * units
            else:
                # Need to convert pip value to USD
                # pip_value = (pip_size / exchange_rate) * units
                pip_value_usd = (pip_size / current_rate) * units
            
            return {
                'pip_size': pip_size,
                'pip_value_usd': pip_value_usd,
                'lot_size': lot_size,
                'units': units,
            }
            
        except Exception as e:
            print(f"❌ Error calculating pip value for {pair}: {e}")
            return {}
    
    def format_for_llm(self, pair: str, news_limit: int = 10, 
                       include_technicals: bool = True) -> str:
        """
        Format FOREX data for LLM consumption.
        
        Args:
            pair: FOREX pair string
            news_limit: Maximum number of news articles
            include_technicals: Whether to include technical analysis
            
        Returns:
            Formatted string ready for LLM
        """
        try:
            # Fetch all data
            news = self.fetch_news(pair, limit=news_limit)
            market_data = self.fetch_market_data(pair)
            pip_info = self.calculate_pip_value(pair)
            
            if not market_data:
                return f"❌ Unable to fetch data for {pair}"
            
            # Parse currencies
            base = market_data['base_currency']
            quote = market_data['quote_currency']
            base_info = market_data['base_info']
            quote_info = market_data['quote_info']
            
            # Build formatted output
            output = []
            output.append("=" * 70)
            output.append(f"📊 {base_info.get('flag', '')} {pair} {quote_info.get('flag', '')} - Yahoo Finance Data")
            output.append("=" * 70)
            output.append("")
            
            # Market data section
            output.append("💹 MARKET DATA:")
            output.append(f"  Current Rate: {market_data['current_rate']:.5f}")
            output.append(f"  Change: {market_data['change']:+.5f} ({market_data['change_pct']:+.2f}%)")
            output.append(f"  High: {market_data['high']:.5f}")
            output.append(f"  Low: {market_data['low']:.5f}")
            output.append(f"  Support: {market_data['support']:.5f}")
            output.append(f"  Resistance: {market_data['resistance']:.5f}")
            output.append(f"  Volatility (ATR): {market_data['volatility']:.5f}")
            output.append("")
            
            # Currency info
            output.append("🏛️ CURRENCY INFO:")
            output.append(f"  Base: {base_info.get('name', base)} - {base_info.get('central_bank', 'N/A')}")
            output.append(f"  Quote: {quote_info.get('name', quote)} - {quote_info.get('central_bank', 'N/A')}")
            output.append("")
            
            # Pip value
            if pip_info:
                output.append("📐 PIP VALUE:")
                output.append(f"  Pip Size: {pip_info['pip_size']}")
                output.append(f"  Pip Value (USD): ${pip_info['pip_value_usd']:.2f}")
                output.append(f"  Lot Size: {pip_info['lot_size']} (Units: {pip_info['units']:,.0f})")
                output.append("")
            
            # News section
            if news:
                output.append(f"📰 LATEST NEWS ({len(news)} articles):")
                for i, article in enumerate(news, 1):
                    output.append(f"  {i}. [{article['published']}] {article['title']}")
                    output.append(f"     Source: {article['publisher']}")
                output.append("")
            else:
                output.append("📰 LATEST NEWS: No recent news available")
                output.append("")
            
            # Technical context
            if include_technicals:
                output.append("📈 TECHNICAL CONTEXT:")
                output.append(f"  Position in Range: {market_data['position_in_range']:.1f}%")
                if market_data['position_in_range'] > 70:
                    output.append("  → Near resistance (overbought territory)")
                elif market_data['position_in_range'] < 30:
                    output.append("  → Near support (oversold territory)")
                else:
                    output.append("  → Mid-range (neutral territory)")
                
                if market_data['volatility'] > 0.01:
                    output.append("  Volatility: HIGH - Caution advised")
                else:
                    output.append("  Volatility: NORMAL")
                output.append("")
            
            return "\n".join(output)
            
        except Exception as e:
            print(f"❌ Error formatting data for LLM: {e}")
            return f"❌ Error formatting data for {pair}: {str(e)}"
    
    def execute(self, pair: str, **kwargs) -> Dict:
        """
        Main execution method called by OpenClaw.
        
        Args:
            pair: FOREX pair string
            **kwargs: Optional parameters (news_limit, include_technicals)
            
        Returns:
            Dictionary with success status, LLM context, raw data, and metadata
        """
        try:
            # Validate it's a major pair
            try:
                self.parse_forex_pair(pair)
            except ValueError as e:
                return {
                    'success': False,
                    'error': str(e),
                    'llm_context': '',
                    'raw_data': {},
                    'metadata': {
                        'skill_name': self.name,
                        'timestamp': datetime.now().isoformat(),
                        'pair': pair,
                    }
                }
            
            # Get parameters from kwargs
            news_limit = kwargs.get('news_limit', 10)
            include_technicals = kwargs.get('include_technicals', True)
            
            # Fetch all data
            news = self.fetch_news(pair, limit=news_limit)
            market_data = self.fetch_market_data(pair)
            pip_info = self.calculate_pip_value(pair)
            
            # Format for LLM
            llm_context = self.format_for_llm(pair, news_limit, include_technicals)
            
            # Build result dictionary
            result = {
                'success': True,
                'llm_context': llm_context,
                'raw_data': {
                    'news': news,
                    'market_data': market_data,
                    'pip_info': pip_info,
                },
                'metadata': {
                    'skill_name': self.name,
                    'timestamp': datetime.now().isoformat(),
                    'pair': pair,
                    'news_count': len(news),
                }
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Error executing skill for {pair}: {e}")
            return {
                'success': False,
                'error': str(e),
                'llm_context': '',
                'raw_data': {},
                'metadata': {
                    'skill_name': self.name,
                    'timestamp': datetime.now().isoformat(),
                    'pair': pair,
                }
            }
    
    def get_all_majors_overview(self) -> List[Dict]:
        """
        Get overview data for all major pairs.
        
        Returns:
            List of summary dictionaries for each major pair
        """
        overview = []
        
        for pair in self.MAJOR_PAIRS:
            try:
                market_data = self.fetch_market_data(pair)
                if market_data:
                    overview.append({
                        'pair': pair,
                        'rate': market_data['current_rate'],
                        'change_pct': market_data['change_pct'],
                        'volatility': market_data['volatility'],
                        'position_in_range': market_data['position_in_range'],
                    })
            except Exception as e:
                print(f"⚠️ Skipping {pair}: {e}")
                continue
        
        return overview


def get_forex_sentiment(news: List[Dict], base_currency: str, quote_currency: str) -> Dict:
    """
    Analyze sentiment from news articles for a FOREX pair.
    
    Args:
        news: List of news article dictionaries
        base_currency: Base currency code (e.g., "EUR")
        quote_currency: Quote currency code (e.g., "USD")
        
    Returns:
        Dictionary with sentiment scores and recommendation
    """
    # Define sentiment keywords
    bullish_keywords = [
        'strengthens', 'rallies', 'gains', 'rises', 'surges', 'climbs',
        'rate hike', 'hawkish', 'strong', 'growth', 'positive', 'bullish',
        'optimistic', 'improve', 'recovery', 'expansion'
    ]
    
    bearish_keywords = [
        'weakens', 'falls', 'declines', 'drops', 'plunges', 'slides',
        'rate cut', 'dovish', 'weak', 'recession', 'negative', 'bearish',
        'pessimistic', 'worsen', 'slowdown', 'contraction'
    ]
    
    # Initialize counters
    base_bullish = 0
    base_bearish = 0
    quote_bullish = 0
    quote_bearish = 0
    
    # Analyze each article
    for article in news:
        title_lower = article.get('title', '').lower()
        
        # Check for base currency mentions
        if base_currency.lower() in title_lower:
            for keyword in bullish_keywords:
                if keyword in title_lower:
                    base_bullish += 1
            for keyword in bearish_keywords:
                if keyword in title_lower:
                    base_bearish += 1
        
        # Check for quote currency mentions
        if quote_currency.lower() in title_lower:
            for keyword in bullish_keywords:
                if keyword in title_lower:
                    quote_bullish += 1
            for keyword in bearish_keywords:
                if keyword in title_lower:
                    quote_bearish += 1
    
    # Calculate pair sentiment
    # If base strengthens or quote weakens, pair goes up (bullish)
    # If base weakens or quote strengthens, pair goes down (bearish)
    pair_sentiment = (base_bullish + quote_bearish) - (base_bearish + quote_bullish)
    
    # Determine recommendation
    if pair_sentiment > 2:
        recommendation = "BUY"
    elif pair_sentiment < -2:
        recommendation = "SELL"
    else:
        recommendation = "NEUTRAL"
    
    return {
        'base_bullish': base_bullish,
        'base_bearish': base_bearish,
        'quote_bullish': quote_bullish,
        'quote_bearish': quote_bearish,
        'pair_sentiment': pair_sentiment,
        'recommendation': recommendation,
    }


def register_skill():
    """
    Register the Yahoo Finance FOREX skill.
    
    Returns:
        YahooFinanceForexSkill instance
    """
    return YahooFinanceForexSkill()
