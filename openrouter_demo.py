"""
OpenRouter Demo Script for TradingAgents

This script demonstrates how to use TradingAgents with OpenRouter instead of OpenAI.
It's a simple test to verify your API keys and configuration are working correctly.

What this script does:
1. Loads your OpenRouter API key from the .env file
2. Configures TradingAgents to use OpenRouter's API
3. Runs a simple trading analysis on a stock (NVDA) for a specific date
4. Prints the result

Before running:
- Make sure your .env file has your OpenRouter API key in OPENAI_API_KEY
- Make sure your .env file has your Alpha Vantage API key in ALPHA_VANTAGE_API_KEY
- Make sure the virtual environment is activated
"""

import os
from dotenv import load_dotenv
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Load environment variables from .env file
# This reads OPENAI_API_KEY (your OpenRouter key) and ALPHA_VANTAGE_API_KEY
load_dotenv()

# Verify the API keys are loaded
openai_api_key = os.getenv("OPENAI_API_KEY")
alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")

if not openai_api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
    print("Please edit the .env file and add your OpenRouter API key.")
    exit(1)

if not alpha_vantage_key:
    print("❌ ERROR: ALPHA_VANTAGE_API_KEY not found in .env file!")
    print("Please edit the .env file and add your Alpha Vantage API key.")
    exit(1)

print("✅ API keys loaded successfully")
print(f"   OpenRouter key starts with: {openai_api_key[:15]}...")
print(f"   Alpha Vantage key starts with: {alpha_vantage_key[:8]}...")
print()

# Create a configuration for OpenRouter
# We start with the default config and customize it
config = DEFAULT_CONFIG.copy()

# Configure to use OpenRouter
config["llm_provider"] = "openrouter"  # This tells TradingAgents to use OpenRouter
config["backend_url"] = "https://openrouter.ai/api/v1"  # OpenRouter's API endpoint

# Choose models that are available on OpenRouter
# These are OpenAI-compatible model names that OpenRouter supports
# You can change these to other models available on OpenRouter
config["deep_think_llm"] = "openai/gpt-4o-mini"  # For complex reasoning
config["quick_think_llm"] = "openai/gpt-4o-mini"  # For quick analysis

print("📋 Configuration:")
print(f"   LLM Provider: {config['llm_provider']}")
print(f"   Backend URL: {config['backend_url']}")
print(f"   Deep Think Model: {config['deep_think_llm']}")
print(f"   Quick Think Model: {config['quick_think_llm']}")
print()

# Create the TradingAgents graph with our configuration
print("🔧 Initializing TradingAgents with OpenRouter...")
try:
    ta = TradingAgentsGraph(debug=True, config=config)
    print("✅ TradingAgents initialized successfully!")
except Exception as e:
    print(f"❌ ERROR initializing TradingAgents: {e}")
    exit(1)

print()
print("=" * 70)
print("📊 Running trading analysis on NVDA for 2024-05-10...")
print("=" * 70)
print()
print("⏳ This may take a minute or two as it:")
print("   - Fetches stock data from Alpha Vantage")
print("   - Analyzes market trends using AI")
print("   - Generates trading recommendations")
print()

try:
    # Run the analysis
    # ticker: "NVDA" (NVIDIA stock)
    # date: "2024-05-10" (a specific date for analysis)
    final_state, decision = ta.propagate("NVDA", "2024-05-10")

    print()
    print("=" * 70)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 70)
    print()
    print("📈 Trading Decision:")
    print(f"   {decision}")
    print()
    print("💡 This means OpenRouter is working correctly with TradingAgents!")
    print()

except Exception as e:
    print()
    print("=" * 70)
    print("❌ ERROR during analysis:")
    print("=" * 70)
    print(f"{e}")
    print()
    print("Common issues:")
    print("1. Check that your OpenRouter API key is correct")
    print("2. Check that your Alpha Vantage API key is correct")
    print("3. Make sure you have internet connectivity")
    print("4. Verify the model names are available on your OpenRouter account")
    print()
