"""
Trading Agent for OpenClaw FOREX bot.

Makes trading decisions using LLM with Yahoo Finance data and technical analysis.
"""

import json
import logging
import requests
from typing import Dict, List, Optional
from src.backend.config_loader import CONFIG

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import FOREX skill
try:
    from skills import get_skill
    from skills.yahoo_finance_forex_majors import get_forex_sentiment
    FOREX_SKILL_AVAILABLE = True
except ImportError:
    FOREX_SKILL_AVAILABLE = False
    logger.warning("⚠️ Yahoo Finance FOREX skill not available")


class TradingAgent:
    """Trading agent that makes decisions using LLM with market data."""
    
    def __init__(self):
        """Initialize the trading agent."""
        # OpenRouter API configuration
        self.api_key = CONFIG.get('openrouter_api_key', '')
        self.base_url = CONFIG.get('openrouter_base_url', 'https://openrouter.ai/api/v1')
        self.model = CONFIG.get('llm_model', 'anthropic/claude-3-5-sonnet')
        self.referer = CONFIG.get('openrouter_referer', 'https://github.com/nazimboudeffa/openclaw-yahoo-finance-forex')
        self.app_title = CONFIG.get('openrouter_app_title', 'OpenClaw FOREX Bot')
        
        # Initialize FOREX skill
        self.forex_skill = None
        if FOREX_SKILL_AVAILABLE and CONFIG.get('yahoo_forex_enabled', True):
            try:
                self.forex_skill = get_skill('yahoo_finance_forex')
                if self.forex_skill:
                    logger.info(f"✅ Yahoo Finance FOREX skill loaded successfully")
                    logger.info(f"   Supported pairs: {self.forex_skill.MAJOR_PAIRS}")
                else:
                    logger.warning("⚠️ Failed to load Yahoo Finance FOREX skill")
            except Exception as e:
                logger.error(f"❌ Error loading FOREX skill: {e}")
                self.forex_skill = None
    
    def _build_context(self, assets: List[str], market_sections: List[Dict], dashboard: Dict) -> str:
        """
        Build comprehensive context string for LLM.
        
        Args:
            assets: List of FOREX pairs to analyze
            market_sections: Technical indicators for each asset
            dashboard: Account and performance dashboard data
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        # Header banner
        context_parts.append("=" * 80)
        context_parts.append("🤖 OPENCLAW FOREX TRADING ANALYSIS")
        context_parts.append("=" * 80)
        context_parts.append("")
        
        # Account overview
        context_parts.append("💰 ACCOUNT OVERVIEW:")
        context_parts.append(f"  Balance: ${dashboard.get('balance', 0):,.2f}")
        context_parts.append(f"  Account Value: ${dashboard.get('account_value', 0):,.2f}")
        context_parts.append(f"  Total Return: {dashboard.get('total_return_pct', 0):+.2f}%")
        context_parts.append(f"  Sharpe Ratio: {dashboard.get('sharpe_ratio', 0):.2f}")
        context_parts.append("")
        
        # Current positions
        positions = dashboard.get('positions', [])
        if positions:
            context_parts.append("📊 CURRENT POSITIONS:")
            for pos in positions:
                context_parts.append(f"  {pos.get('asset', 'N/A')}: {pos.get('size', 0)} units @ {pos.get('entry_price', 0):.5f}")
                pnl = pos.get('pnl', 0)
                pnl_sign = "📈" if pnl > 0 else "📉" if pnl < 0 else "➖"
                context_parts.append(f"    {pnl_sign} P&L: ${pnl:+,.2f}")
            context_parts.append("")
        else:
            context_parts.append("📊 CURRENT POSITIONS: None")
            context_parts.append("")
        
        # Asset analysis
        for asset in assets:
            context_parts.append("=" * 80)
            context_parts.append(f"📈 ANALYSIS: {asset}")
            context_parts.append("=" * 80)
            context_parts.append("")
            
            # Yahoo Finance data
            if self.forex_skill:
                try:
                    logger.info(f"📊 Fetching Yahoo Finance data for {asset}...")
                    result = self.forex_skill.execute(
                        asset, 
                        news_limit=CONFIG.get('yahoo_news_limit', 10)
                    )
                    
                    if result['success']:
                        # Add Yahoo Finance context
                        context_parts.append(result['llm_context'])
                        context_parts.append("")
                        
                        # Add sentiment analysis
                        news = result['raw_data'].get('news', [])
                        if news:
                            market_data = result['raw_data'].get('market_data', {})
                            base = market_data.get('base_currency', '')
                            quote = market_data.get('quote_currency', '')
                            
                            if base and quote:
                                sentiment = get_forex_sentiment(news, base, quote)
                                context_parts.append("🎯 SENTIMENT ANALYSIS:")
                                context_parts.append(f"  Base ({base}) Bullish: {sentiment['base_bullish']} | Bearish: {sentiment['base_bearish']}")
                                context_parts.append(f"  Quote ({quote}) Bullish: {sentiment['quote_bullish']} | Bearish: {sentiment['quote_bearish']}")
                                context_parts.append(f"  Pair Sentiment Score: {sentiment['pair_sentiment']:+d}")
                                context_parts.append(f"  Recommendation: {sentiment['recommendation']}")
                                context_parts.append("")
                    else:
                        context_parts.append(f"⚠️ Yahoo Finance data unavailable: {result.get('error', 'Unknown error')}")
                        context_parts.append("")
                        
                except Exception as e:
                    logger.error(f"❌ Error fetching Yahoo Finance data for {asset}: {e}")
                    context_parts.append(f"⚠️ Error fetching Yahoo Finance data: {str(e)}")
                    context_parts.append("")
            
            # Technical indicators
            tech_section = next((s for s in market_sections if s.get('asset') == asset), None)
            if tech_section:
                context_parts.append("📊 TECHNICAL INDICATORS:")
                context_parts.append(f"  Current Price: {tech_section.get('current_price', 'N/A')}")
                
                indicators = tech_section.get('indicators', {})
                intraday = indicators.get('intraday', {})
                long_term = indicators.get('long_term', {})
                
                if intraday:
                    context_parts.append("  Intraday:")
                    for key, value in intraday.items():
                        context_parts.append(f"    {key}: {value}")
                
                if long_term:
                    context_parts.append("  Long-term:")
                    for key, value in long_term.items():
                        context_parts.append(f"    {key}: {value}")
                
                context_parts.append("")
        
        # Recent trading diary
        diary = dashboard.get('recent_diary', [])
        if diary:
            context_parts.append("=" * 80)
            context_parts.append("📝 RECENT TRADING DIARY:")
            context_parts.append("=" * 80)
            for entry in diary[-5:]:  # Last 5 entries
                context_parts.append(f"  [{entry.get('timestamp', 'N/A')}] {entry.get('action', 'N/A')}")
                context_parts.append(f"    {entry.get('notes', '')}")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for the LLM.
        
        Returns:
            System prompt string
        """
        return """You are an expert FOREX trading agent for OpenClaw bot. Your role is to analyze market data and make informed trading decisions.

DATA SOURCES:
- Yahoo Finance: Real-time news, market data, and sentiment for major FOREX pairs
- Technical Indicators: EMA, RSI, MACD, and other technical analysis tools (via TAAPI)
- Trading History: Past trades, performance metrics, and account status

FUNDAMENTAL ANALYSIS PRINCIPLES:
1. Central Bank Policy: Monitor interest rate decisions, policy statements, and forward guidance
2. Economic Data: GDP, inflation, employment, trade balances affect currency strength
3. News Sentiment: Analyze news headlines for bullish/bearish signals
4. Geopolitical Events: Political stability, elections, and global events impact currencies

TECHNICAL ANALYSIS GUIDELINES:
1. Trend: Identify primary trend using EMAs (20, 50, 200 periods)
2. Momentum: Use RSI (14) to identify overbought (>70) or oversold (<30) conditions
3. Support & Resistance: Identify key levels from historical highs and lows
4. Volatility: Use ATR to assess market volatility and adjust position sizing

RISK MANAGEMENT RULES:
1. Position Sizing: Never risk more than 2% of account balance per trade
2. Stop Loss: Always set stop loss at key support/resistance levels
3. Take Profit: Target minimum 2:1 reward-to-risk ratio
4. Diversification: Don't concentrate more than 30% in a single currency
5. Max Positions: Maximum 3-4 open positions simultaneously

DECISION LOGIC:
- BUY: When trend is up, sentiment is bullish, and price near support with confirmation
- SELL: When trend is down, sentiment is bearish, and price near resistance with confirmation  
- HOLD: When signals are mixed, volatility is too high, or no clear setup exists

OUTPUT FORMAT:
Provide your analysis in strict JSON format with the following structure:
{
  "reasoning": "Comprehensive analysis explaining market conditions, sentiment, and technical setup for each pair",
  "trade_decisions": [
    {
      "asset": "EURUSD",
      "action": "BUY|SELL|HOLD",
      "allocation_usd": 1000,
      "tp_price": 1.1200,
      "sl_price": 1.0900,
      "exit_plan": "Take profit at resistance or if sentiment shifts",
      "rationale": "Specific reason for this trade decision"
    }
  ]
}

Be disciplined, patient, and always prioritize capital preservation over profit maximization."""
    
    async def make_decision(self, assets: List[str], market_sections: List[Dict], 
                           dashboard: Dict) -> Dict:
        """
        Make trading decision using LLM with market data.
        
        Args:
            assets: List of FOREX pairs to analyze
            market_sections: Technical indicators for each asset
            dashboard: Account and performance data
            
        Returns:
            Decision dictionary with reasoning and trade_decisions
        """
        try:
            # Build context
            context = self._build_context(assets, market_sections, dashboard)
            
            # Get system prompt
            system_prompt = self._get_system_prompt()
            
            # Prepare messages
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context}
            ]
            
            # Check if API key is configured
            if not self.api_key:
                logger.error("❌ OpenRouter API key not configured")
                return self._get_fallback_decision(assets)
            
            # Make API request
            logger.info(f"🤖 Sending request to LLM: {self.model}")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": self.referer,
                "X-Title": self.app_title,
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000,
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            # Extract content
            content = response_data['choices'][0]['message']['content']
            
            # Clean markdown wrappers
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            elif content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            # Parse JSON
            decision = json.loads(content)
            
            logger.info("✅ Decision received from LLM")
            return decision
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ API request error: {e}")
            return self._get_fallback_decision(assets)
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parse error: {e}")
            logger.error(f"Raw content: {content[:500] if 'content' in locals() else 'N/A'}")
            return self._get_fallback_decision(assets)
        except Exception as e:
            logger.error(f"❌ Unexpected error in make_decision: {e}", exc_info=True)
            return self._get_fallback_decision(assets)
    
    def _get_fallback_decision(self, assets: List[str]) -> Dict:
        """
        Get fallback decision when LLM fails.
        
        Args:
            assets: List of FOREX pairs
            
        Returns:
            Safe fallback decision (HOLD all)
        """
        return {
            "reasoning": "Unable to make informed decision due to API error. Holding all positions for safety.",
            "trade_decisions": [
                {
                    "asset": asset,
                    "action": "HOLD",
                    "allocation_usd": 0,
                    "tp_price": None,
                    "sl_price": None,
                    "exit_plan": "Wait for stable market conditions",
                    "rationale": "API error - defaulting to HOLD for capital preservation"
                }
                for asset in assets
            ]
        }
