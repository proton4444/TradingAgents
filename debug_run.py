
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Load env vars
load_dotenv()

def main():
    print("Starting debug run...")
    
    ticker = "NVDA"
    date_str = "2024-05-10"
    
    print(f"Initializing TradingAgentsGraph for {ticker} on {date_str}...")
    
    # Use default config but ensure we can see what's happening
    config = DEFAULT_CONFIG.copy()
    # Ensure we are using the keys from env
    print(f"LLM Provider: {config.get('llm_provider')}")
    print(f"Deep Model: {config.get('deep_think_llm')}")
    
    try:
        ta = TradingAgentsGraph(debug=True, config=config)
        print("Graph initialized. Starting propagation...")
        
        final_state, decision = ta.propagate(ticker, date_str)
        
        print("\nAnalysis Complete!")
        print(f"Decision: {decision}")
        
    except Exception as e:
        print(f"\nERROR OCCURRED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
