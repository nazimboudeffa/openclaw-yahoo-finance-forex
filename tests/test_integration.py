"""
Integration test for Yahoo Finance FOREX skill with OpenClaw.
"""

import asyncio
from src.backend.agent.decision_maker import TradingAgent
from src.backend.config_loader import CONFIG


async def test():
    """Run integration tests."""
    print("=" * 70)
    print("🧪 Testing FOREX Skill Integration")
    print("=" * 70)
    print()
    
    # Test 1: Agent initialization
    print("📝 Test 1: Initializing Trading Agent...")
    agent = TradingAgent()
    
    if agent.forex_skill:
        print("✅ FOREX skill loaded successfully")
        print(f"   Skill name: {agent.forex_skill.name}")
        print(f"   Supported pairs: {', '.join(agent.forex_skill.MAJOR_PAIRS)}")
    else:
        print("❌ FOREX skill not loaded")
        print("⚠️  Make sure yfinance is installed: pip install yfinance")
        return
    
    print()
    
    # Test 2: Fetch EUR/USD data
    print("=" * 70)
    print("📝 Test 2: Testing EUR/USD Data Fetch...")
    print("=" * 70)
    result = agent.forex_skill.execute("EURUSD", news_limit=5)
    
    if result['success']:
        print("✅ Data fetched successfully")
        print(f"   News articles: {len(result['raw_data']['news'])}")
        
        market_data = result['raw_data'].get('market_data', {})
        if market_data:
            print(f"   Current rate: {market_data.get('current_rate', 'N/A')}")
            print(f"   Change: {market_data.get('change_pct', 0):+.2f}%")
            print(f"   Volatility: {market_data.get('volatility', 'N/A')}")
        
        print("\n📄 LLM Context Preview (first 500 chars):")
        print("-" * 70)
        print(result['llm_context'][:500] + "...")
        print("-" * 70)
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    print()
    
    # Test 3: Test all major pairs overview
    print("=" * 70)
    print("📝 Test 3: Testing All Major Pairs Overview...")
    print("=" * 70)
    overview = agent.forex_skill.get_all_majors_overview()
    
    if overview:
        print(f"✅ Retrieved data for {len(overview)} pairs:")
        for pair_data in overview:
            print(f"   {pair_data['pair']}: {pair_data['rate']:.5f} ({pair_data['change_pct']:+.2f}%)")
    else:
        print("⚠️  No overview data available")
    
    print()
    
    # Test 4: Full decision making
    print("=" * 70)
    print("📝 Test 4: Testing Full Decision Making...")
    print("=" * 70)
    print("🤖 Calling LLM to make trading decision...")
    
    decision = await agent.make_decision(
        assets=['EURUSD'],
        market_sections=[{
            'asset': 'EURUSD',
            'current_price': 1.1000,
            'indicators': {
                'intraday': {'ema20': 1.0980, 'rsi14': 55},
                'long_term': {'ema20': 1.0950, 'ema50': 1.0900}
            }
        }],
        dashboard={
            'balance': 10000,
            'account_value': 10000,
            'total_return_pct': 0,
            'sharpe_ratio': 0,
            'positions': [],
            'recent_diary': []
        }
    )
    
    print("\n✅ Decision received:")
    if decision.get('trade_decisions'):
        trade = decision['trade_decisions'][0]
        print(f"   Asset: {trade['asset']}")
        print(f"   Action: {trade['action']}")
        print(f"   Allocation: ${trade.get('allocation_usd', 0):,.2f}")
        print(f"   Rationale: {trade.get('rationale', 'N/A')[:100]}...")
    
    print("\n💭 Reasoning (first 300 chars):")
    print("-" * 70)
    print(decision.get('reasoning', 'N/A')[:300] + "...")
    print("-" * 70)
    
    print()
    print("=" * 70)
    print("✅ Integration test complete!")
    print("=" * 70)
    print()
    print("💡 Next steps:")
    print("   1. Configure OpenRouter API key in .env file")
    print("   2. Run the main bot: python src/main.py")
    print("   3. Monitor trades and adjust configuration as needed")
    print()


if __name__ == "__main__":
    asyncio.run(test())
