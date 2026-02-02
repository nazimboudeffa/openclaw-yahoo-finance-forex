"""
OpenClaw FOREX Trading Bot - Main Entry Point

Runs the main trading loop with Yahoo Finance integration.
"""

import asyncio
import logging
from src.backend.agent.decision_maker import TradingAgent
from src.backend.config_loader import CONFIG

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def trading_loop():
    """Main trading loop."""
    agent = TradingAgent()
    forex_pairs = CONFIG.get('forex_pairs', ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD'])
    
    logger.info("=" * 70)
    logger.info("🚀 Starting OpenClaw FOREX Bot")
    logger.info("=" * 70)
    logger.info(f"📊 Trading pairs: {', '.join(forex_pairs)}")
    logger.info(f"🤖 LLM Model: {CONFIG['llm_model']}")
    logger.info(f"🔧 Yahoo FOREX: {'✅ Enabled' if CONFIG['yahoo_forex_enabled'] else '❌ Disabled'}")
    logger.info("=" * 70)
    
    cycle_count = 0
    
    while True:
        try:
            cycle_count += 1
            logger.info("\n" + "=" * 70)
            logger.info(f"🔄 Starting trading cycle #{cycle_count}")
            logger.info("=" * 70)
            
            # Placeholder market sections (replace with real data from TAAPI or other sources)
            market_sections = []
            for pair in forex_pairs:
                market_sections.append({
                    'asset': pair,
                    'current_price': 1.1000,  # Placeholder - should come from real market data
                    'indicators': {
                        'intraday': {
                            'ema20': 1.0980,
                            'rsi14': 55,
                            'macd': 0.0015,
                            'signal': 0.0012
                        },
                        'long_term': {
                            'ema20': 1.0950,
                            'ema50': 1.0900,
                            'ema200': 1.0850,
                            'trend': 'bullish'
                        }
                    }
                })
            
            # Placeholder dashboard (replace with real account data)
            dashboard = {
                'balance': 10000.00,
                'account_value': 10500.00,
                'total_return_pct': 5.0,
                'sharpe_ratio': 1.2,
                'positions': [],
                'recent_diary': []
            }
            
            # Make trading decision
            logger.info("🤔 Analyzing markets and making decision...")
            decision = await agent.make_decision(forex_pairs, market_sections, dashboard)
            
            # Log results
            logger.info("\n" + "=" * 70)
            logger.info("💭 REASONING:")
            logger.info("=" * 70)
            logger.info(decision.get('reasoning', 'N/A'))
            
            logger.info("\n" + "=" * 70)
            logger.info("🎯 TRADE DECISIONS:")
            logger.info("=" * 70)
            
            for trade in decision.get('trade_decisions', []):
                action = trade['action']
                action_emoji = "🟢" if action == "BUY" else "🔴" if action == "SELL" else "🟡"
                
                logger.info(f"\n  {action_emoji} {trade['asset']}:")
                logger.info(f"    Action: {action}")
                logger.info(f"    Allocation: ${trade.get('allocation_usd', 0):,.2f}")
                logger.info(f"    TP: {trade.get('tp_price', 'N/A')}")
                logger.info(f"    SL: {trade.get('sl_price', 'N/A')}")
                logger.info(f"    Exit Plan: {trade.get('exit_plan', 'N/A')}")
                logger.info(f"    Rationale: {trade.get('rationale', 'N/A')}")
            
            logger.info("\n" + "=" * 70)
            logger.info("⏰ Sleeping for 5 minutes until next cycle...")
            logger.info("=" * 70)
            
            # Sleep 5 minutes
            await asyncio.sleep(300)
            
        except KeyboardInterrupt:
            logger.info("\n" + "=" * 70)
            logger.info("🛑 Bot stopped by user")
            logger.info("=" * 70)
            break
        except Exception as e:
            logger.error(f"❌ Error in trading loop: {e}", exc_info=True)
            logger.info("⏰ Sleeping for 1 minute before retry...")
            await asyncio.sleep(60)


if __name__ == "__main__":
    try:
        asyncio.run(trading_loop())
    except KeyboardInterrupt:
        logger.info("👋 Goodbye!")
