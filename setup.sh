#!/bin/bash
# Setup script for OpenClaw FOREX Bot

echo "🚀 OpenClaw FOREX Bot - Setup"
echo "=============================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "   Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
echo ""
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "   ✅ .env created from .env.example"
    echo "   ⚠️  Please edit .env and add your OpenRouter API key"
else
    echo "📝 .env file already exists"
fi

# Verify installation
echo ""
echo "✅ Verifying installation..."
python -c "import yfinance; print('   ✅ yfinance installed')"
python -c "from skills.yahoo_finance_forex_majors import YahooFinanceForexSkill; print('   ✅ Skill module loaded')"
python -c "from src.backend.config_loader import CONFIG; print('   ✅ Config loader working')"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your OpenRouter API key"
echo "  2. Activate virtual environment: source venv/bin/activate"
echo "  3. Run tests: python tests/test_integration.py"
echo "  4. Start bot: ./run.sh or python src/main.py"
echo ""
