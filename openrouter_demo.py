"""
OpenRouter Demo Script for TradingAgents

This script demonstrates how to use TradingAgents with OpenRouter instead of OpenAI.
It's a simple test to verify your API keys and configuration are working correctly.

Usage:
    python openrouter_demo.py                    # Default: NVDA on 2024-05-10
    python openrouter_demo.py --ticker AAPL      # Custom ticker
    python openrouter_demo.py --ticker TSLA --date 2024-06-15
    python openrouter_demo.py --help             # Show all options

Before running:
- Make sure your .env file has your OpenRouter API key in OPENAI_API_KEY
- Make sure your .env file has your Alpha Vantage API key in ALPHA_VANTAGE_API_KEY
- Make sure the virtual environment is activated
"""

import os
import sys
import argparse
from datetime import datetime
from typing import Optional, Tuple
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Initialize rich console for beautiful output
console = Console()


def load_api_keys() -> Tuple[Optional[str], Optional[str]]:
    """
    Load API keys from .env file.

    Returns:
        Tuple of (openai_key, alpha_vantage_key)
    """
    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    return openai_key, alpha_vantage_key


def validate_api_keys(openai_key: Optional[str], alpha_vantage_key: Optional[str]) -> bool:
    """
    Validate that API keys are present and not placeholder values.

    Args:
        openai_key: OpenRouter API key
        alpha_vantage_key: Alpha Vantage API key

    Returns:
        True if valid, False otherwise
    """
    if not openai_key:
        console.print("[red]❌ ERROR: OPENAI_API_KEY not found in .env file![/red]")
        console.print("Please edit the .env file and add your OpenRouter API key.")
        return False

    if "REPLACE" in openai_key.upper():
        console.print("[red]❌ ERROR: OPENAI_API_KEY still contains placeholder text![/red]")
        console.print("Please edit the .env file and replace with your actual OpenRouter API key.")
        return False

    if not alpha_vantage_key:
        console.print("[red]❌ ERROR: ALPHA_VANTAGE_API_KEY not found in .env file![/red]")
        console.print("Please edit the .env file and add your Alpha Vantage API key.")
        return False

    if "REPLACE" in alpha_vantage_key.upper():
        console.print("[red]❌ ERROR: ALPHA_VANTAGE_API_KEY still contains placeholder text![/red]")
        console.print("Please edit the .env file and replace with your actual Alpha Vantage API key.")
        return False

    return True


def display_api_keys_info(openai_key: str, alpha_vantage_key: str) -> None:
    """Display API key information (partially masked for security)."""
    table = Table(title="🔑 API Keys Loaded")
    table.add_column("Key Type", style="cyan")
    table.add_column("Preview", style="green")

    table.add_row("OpenRouter", f"{openai_key[:15]}...")
    table.add_row("Alpha Vantage", f"{alpha_vantage_key[:8]}...")

    console.print(table)
    console.print()


def create_config(deep_model: str = "openai/gpt-4o-mini",
                 quick_model: str = "openai/gpt-4o-mini") -> dict:
    """
    Create TradingAgents configuration for OpenRouter.

    Args:
        deep_model: Model for complex reasoning
        quick_model: Model for quick analysis

    Returns:
        Configuration dictionary
    """
    from tradingagents.default_config import DEFAULT_CONFIG

    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "openrouter"
    config["backend_url"] = "https://openrouter.ai/api/v1"
    config["deep_think_llm"] = deep_model
    config["quick_think_llm"] = quick_model

    return config


def display_config(config: dict) -> None:
    """Display configuration information."""
    table = Table(title="📋 TradingAgents Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="yellow")

    table.add_row("LLM Provider", config["llm_provider"])
    table.add_row("Backend URL", config["backend_url"])
    table.add_row("Deep Think Model", config["deep_think_llm"])
    table.add_row("Quick Think Model", config["quick_think_llm"])

    console.print(table)
    console.print()


def initialize_trading_agents(config: dict, debug: bool = True):
    """
    Initialize TradingAgents with the given configuration.

    Args:
        config: Configuration dictionary
        debug: Enable debug mode

    Returns:
        TradingAgentsGraph instance

    Raises:
        Exception if initialization fails
    """
    from tradingagents.graph.trading_graph import TradingAgentsGraph

    with console.status("[bold green]🔧 Initializing TradingAgents with OpenRouter..."):
        ta = TradingAgentsGraph(debug=debug, config=config)

    console.print("[green]✅ TradingAgents initialized successfully![/green]")
    return ta


def run_analysis(ta, ticker: str, date: str) -> Tuple[any, str]:
    """
    Run trading analysis on a stock.

    Args:
        ta: TradingAgentsGraph instance
        ticker: Stock ticker symbol
        date: Analysis date in YYYY-MM-DD format

    Returns:
        Tuple of (final_state, decision)
    """
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]📊 Running Trading Analysis[/bold cyan]\n\n"
        f"[yellow]Ticker:[/yellow] {ticker}\n"
        f"[yellow]Date:[/yellow] {date}",
        border_style="cyan"
    ))
    console.print()

    console.print("[dim]⏳ This may take a minute or two as it:[/dim]")
    console.print("[dim]   - Fetches stock data from Alpha Vantage[/dim]")
    console.print("[dim]   - Analyzes market trends using AI[/dim]")
    console.print("[dim]   - Generates trading recommendations[/dim]")
    console.print()

    with console.status("[bold green]Analyzing..."):
        final_state, decision = ta.propagate(ticker, date)

    return final_state, decision


def display_results(ticker: str, date: str, decision: str) -> None:
    """Display analysis results."""
    console.print()
    console.print(Panel.fit(
        f"[bold green]✅ ANALYSIS COMPLETE![/bold green]\n\n"
        f"[yellow]Stock:[/yellow] {ticker}\n"
        f"[yellow]Date:[/yellow] {date}\n\n"
        f"[bold cyan]📈 Trading Decision:[/bold cyan]\n{decision}",
        border_style="green"
    ))
    console.print()
    console.print("[green]💡 This means OpenRouter is working correctly with TradingAgents![/green]")
    console.print()


def display_error(error: Exception) -> None:
    """Display error information with helpful debugging tips."""
    console.print()
    console.print(Panel.fit(
        f"[bold red]❌ ERROR DURING ANALYSIS[/bold red]\n\n"
        f"[yellow]{str(error)}[/yellow]",
        border_style="red"
    ))
    console.print()
    console.print("[bold]Common issues:[/bold]")
    console.print("1. Check that your OpenRouter API key is correct")
    console.print("2. Check that your Alpha Vantage API key is correct")
    console.print("3. Make sure you have internet connectivity")
    console.print("4. Verify the model names are available on your OpenRouter account")
    console.print("5. Check Alpha Vantage rate limits (5 calls/min, 100/day for free tier)")
    console.print()


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Test TradingAgents with OpenRouter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python openrouter_demo.py
  python openrouter_demo.py --ticker AAPL
  python openrouter_demo.py --ticker TSLA --date 2024-06-15
  python openrouter_demo.py --ticker MSFT --date 2024-03-20 --deep-model anthropic/claude-3.5-sonnet
        """
    )

    parser.add_argument(
        "--ticker",
        type=str,
        default="NVDA",
        help="Stock ticker symbol (default: NVDA)"
    )

    parser.add_argument(
        "--date",
        type=str,
        default="2024-05-10",
        help="Analysis date in YYYY-MM-DD format (default: 2024-05-10)"
    )

    parser.add_argument(
        "--deep-model",
        type=str,
        default="openai/gpt-4o-mini",
        help="Model for deep thinking (default: openai/gpt-4o-mini)"
    )

    parser.add_argument(
        "--quick-model",
        type=str,
        default="openai/gpt-4o-mini",
        help="Model for quick thinking (default: openai/gpt-4o-mini)"
    )

    parser.add_argument(
        "--no-debug",
        action="store_true",
        help="Disable debug mode"
    )

    return parser.parse_args()


def validate_date(date_str: str) -> bool:
    """Validate date format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        console.print(f"[red]❌ Invalid date format: {date_str}[/red]")
        console.print("Please use YYYY-MM-DD format (e.g., 2024-05-10)")
        return False


def main():
    """Main entry point."""
    # Parse arguments
    args = parse_arguments()

    # Validate date
    if not validate_date(args.date):
        return 1

    # Display header
    console.print()
    console.print(Panel.fit(
        "[bold cyan]TradingAgents + OpenRouter Demo[/bold cyan]\n"
        "[dim]Testing API connection and running stock analysis[/dim]",
        border_style="cyan"
    ))
    console.print()

    # Load and validate API keys
    openai_key, alpha_vantage_key = load_api_keys()

    if not validate_api_keys(openai_key, alpha_vantage_key):
        return 1

    display_api_keys_info(openai_key, alpha_vantage_key)

    # Create configuration
    config = create_config(
        deep_model=args.deep_model,
        quick_model=args.quick_model
    )

    display_config(config)

    # Initialize TradingAgents
    try:
        ta = initialize_trading_agents(config, debug=not args.no_debug)
    except Exception as e:
        console.print(f"[red]❌ ERROR initializing TradingAgents: {e}[/red]")
        return 1

    # Run analysis
    try:
        final_state, decision = run_analysis(ta, args.ticker, args.date)
        display_results(args.ticker, args.date, decision)
        return 0
    except Exception as e:
        display_error(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
