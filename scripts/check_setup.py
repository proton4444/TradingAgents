#!/usr/bin/env python
"""
Setup validation script for TradingAgents.

Checks that everything is configured correctly before running analyses.

Usage:
    python scripts/check_setup.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tradingagents.default_config import DEFAULT_CONFIG, validate_config

console = Console()


def check_api_keys():
    """Check if required API keys are configured."""
    console.print("\n[bold cyan]🔑 Checking API Keys...[/bold cyan]")

    load_dotenv()

    table = Table(title="API Keys Status")
    table.add_column("Key", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Notes", style="yellow")

    # Check OpenAI/OpenRouter key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        table.add_row("OPENAI_API_KEY", "❌ Missing", "Required for LLM access")
    elif "REPLACE" in openai_key.upper():
        table.add_row("OPENAI_API_KEY", "⚠️  Placeholder", "Replace with actual key")
    else:
        table.add_row("OPENAI_API_KEY", "✅ Configured", f"Starts with: {openai_key[:15]}...")

    # Check Alpha Vantage key
    av_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not av_key:
        table.add_row("ALPHA_VANTAGE_API_KEY", "❌ Missing", "Required for market data")
    elif "REPLACE" in av_key.upper():
        table.add_row("ALPHA_VANTAGE_API_KEY", "⚠️  Placeholder", "Replace with actual key")
    else:
        table.add_row("ALPHA_VANTAGE_API_KEY", "✅ Configured", f"Starts with: {av_key[:8]}...")

    console.print(table)

    return bool(openai_key and "REPLACE" not in openai_key.upper() and
                av_key and "REPLACE" not in av_key.upper())


def check_python_version():
    """Check Python version."""
    console.print("\n[bold cyan]🐍 Checking Python Version...[/bold cyan]")

    version_info = sys.version_info
    version_str = f"{version_info.major}.{version_info.minor}.{version_info.micro}"

    if version_info >= (3, 10):
        console.print(f"✅ Python {version_str} (Compatible)")
        return True
    else:
        console.print(f"❌ Python {version_str} (Requires 3.10+)")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    console.print("\n[bold cyan]📦 Checking Dependencies...[/bold cyan]")

    required_packages = [
        "langchain_openai",
        "langchain_anthropic",
        "langchain_community",
        "langgraph",
        "pandas",
        "yfinance",
        "chromadb",
        "rich",
        "questionary",
        "dotenv",
    ]

    table = Table(title="Package Status")
    table.add_column("Package", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Version", style="yellow")

    all_installed = True

    for package in required_packages:
        try:
            if package == "dotenv":
                import python_dotenv as pkg
            else:
                pkg = __import__(package.replace("-", "_"))

            version = getattr(pkg, "__version__", "unknown")
            table.add_row(package, "✅ Installed", version)
        except ImportError:
            table.add_row(package, "❌ Missing", "-")
            all_installed = False

    console.print(table)

    if not all_installed:
        console.print("\n[yellow]To install missing packages:[/yellow]")
        console.print("  pip install -r requirements.txt")

    return all_installed


def check_configuration():
    """Check configuration validity."""
    console.print("\n[bold cyan]⚙️  Checking Configuration...[/bold cyan]")

    is_valid, errors = validate_config(DEFAULT_CONFIG)

    if is_valid:
        console.print("✅ Configuration is valid")

        table = Table(title="Current Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="yellow")

        table.add_row("LLM Provider", DEFAULT_CONFIG["llm_provider"])
        table.add_row("Backend URL", DEFAULT_CONFIG["backend_url"])
        table.add_row("Deep Think Model", DEFAULT_CONFIG["deep_think_llm"])
        table.add_row("Quick Think Model", DEFAULT_CONFIG["quick_think_llm"])
        table.add_row("Results Dir", DEFAULT_CONFIG["results_dir"])
        table.add_row("Data Dir", DEFAULT_CONFIG["data_dir"])

        console.print(table)
    else:
        console.print("❌ Configuration has errors:")
        for error in errors:
            console.print(f"  - {error}")

    return is_valid


def check_directories():
    """Check that required directories exist."""
    console.print("\n[bold cyan]📁 Checking Directories...[/bold cyan]")

    dirs_to_check = {
        "Results": DEFAULT_CONFIG["results_dir"],
        "Data": DEFAULT_CONFIG["data_dir"],
        "Cache": DEFAULT_CONFIG["data_cache_dir"],
    }

    table = Table(title="Directory Status")
    table.add_column("Directory", style="cyan")
    table.add_column("Path", style="yellow")
    table.add_column("Status", style="green")

    all_ok = True

    for name, path in dirs_to_check.items():
        path_obj = Path(path)
        if path_obj.exists():
            table.add_row(name, str(path), "✅ Exists")
        else:
            try:
                path_obj.mkdir(parents=True, exist_ok=True)
                table.add_row(name, str(path), "✅ Created")
            except Exception as e:
                table.add_row(name, str(path), f"❌ Error: {e}")
                all_ok = False

    console.print(table)
    return all_ok


def check_internet():
    """Check internet connectivity."""
    console.print("\n[bold cyan]🌐 Checking Internet Connection...[/bold cyan]")

    try:
        import urllib.request
        urllib.request.urlopen("https://www.google.com", timeout=5)
        console.print("✅ Internet connection active")
        return True
    except Exception as e:
        console.print(f"❌ No internet connection: {e}")
        return False


def main():
    """Run all checks."""
    console.print(Panel.fit(
        "[bold cyan]TradingAgents Setup Checker[/bold cyan]\n"
        "[dim]Validating your configuration and environment[/dim]",
        border_style="cyan"
    ))

    checks = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "API Keys": check_api_keys(),
        "Configuration": check_configuration(),
        "Directories": check_directories(),
        "Internet": check_internet(),
    }

    # Summary
    console.print("\n" + "=" * 70)
    console.print("[bold cyan]📊 Setup Summary[/bold cyan]")
    console.print("=" * 70)

    all_passed = True
    for check_name, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        console.print(f"  {check_name:20s} {status}")
        if not passed:
            all_passed = False

    console.print("=" * 70)

    if all_passed:
        console.print("\n[bold green]✅ All checks passed! You're ready to use TradingAgents.[/bold green]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("  1. Test OpenRouter: python openrouter_demo.py")
        console.print("  2. Run the CLI:     python -m cli.main")
        return 0
    else:
        console.print("\n[bold red]❌ Some checks failed. Please fix the issues above.[/bold red]")
        console.print("\n[bold]Common solutions:[/bold]")
        console.print("  - Missing API keys: Edit the .env file")
        console.print("  - Missing packages: pip install -r requirements.txt")
        console.print("  - Python too old:   Install Python 3.10 or newer")
        return 1


if __name__ == "__main__":
    sys.exit(main())
