# TradingAgents Setup Guide (Windows + OpenRouter)

Complete guide for setting up TradingAgents on Windows 11 with OpenRouter integration.

> **Note:** This guide is specifically for the Windows + OpenRouter configuration. For the original setup instructions, see [README.md](README.md).

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Detailed Setup](#detailed-setup)
4. [Configuration](#configuration)
5. [Running TradingAgents](#running-tradingagents)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Usage](#advanced-usage)

---

## Prerequisites

### Required Software

| Software | Minimum Version | Recommended | Download |
|----------|----------------|-------------|----------|
| **Python** | 3.10 | 3.11+ | [python.org](https://www.python.org/downloads/) |
| **Git** | 2.30+ | Latest | [git-scm.com](https://git-scm.com/download/win) |
| **Zed Editor** | Any | Latest | [zed.dev](https://zed.dev/) (optional) |

### Required API Keys

| Service | Purpose | Free Tier | Get Key |
|---------|---------|-----------|---------|
| **OpenRouter** | AI Models (LLM) | Limited free credits | [openrouter.ai](https://openrouter.ai/) |
| **Alpha Vantage** | Market Data | 5 calls/min, 100/day | [alphavantage.co](https://www.alphavantage.co/support/#api-key) |

---

## Quick Start

**⚡ Get up and running in 5 minutes!**

### 1. Open PowerShell

```powershell
# Navigate to where you want the project
cd C:\Projects
```

### 2. Clone and Setup

```powershell
# Clone the repository
git clone https://github.com/YOUR_USERNAME/TradingAgents.git
cd TradingAgents

# Create virtual environment
py -3.11 -m venv .venv

# Activate it (if this fails, see Troubleshooting)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys

```powershell
# Copy the .env file and edit it
cp .env.example .env
# Open .env in your editor and add your API keys
```

### 4. Validate Setup

```powershell
# Run the setup checker
python scripts/check_setup.py
```

### 5. Test It!

```powershell
# Quick test
python openrouter_demo.py --ticker NVDA

# Or run the full CLI
python -m cli.main
```

---

## Detailed Setup

### Step 1: Install Python

1. **Download Python 3.11+** from [python.org](https://www.python.org/downloads/)
2. **During installation:**
   - ✅ **CHECK** "Add Python to PATH"
   - ✅ **CHECK** "Install for all users" (optional)
   - Click "Install Now"

3. **Verify installation:**
   ```powershell
   py --version
   # Should show: Python 3.11.x
   ```

### Step 2: Install Git

1. **Download Git** from [git-scm.com](https://git-scm.com/download/win)
2. **During installation:**
   - Accept all defaults (they're good for Windows)
   - Use "Git from the command line and also from 3rd-party software"

3. **Verify installation:**
   ```powershell
   git --version
   # Should show: git version 2.x.x
   ```

### Step 3: Clone TradingAgents

```powershell
# Navigate to your projects folder
cd C:\Projects  # or wherever you keep projects

# Clone the repository
git clone https://github.com/YOUR_USERNAME/TradingAgents.git

# Enter the directory
cd TradingAgents

# Verify you're in the right place
ls
# Should see: README.md, requirements.txt, cli/, tradingagents/, etc.
```

### Step 4: Create Virtual Environment

**Why?** Keeps Python packages isolated from your system.

```powershell
# Create .venv folder with Python 3.11
py -3.11 -m venv .venv

# If py -3.11 doesn't work, try:
py -3 -m venv .venv
```

### Step 5: Activate Virtual Environment

```powershell
# Activate the venv
.\.venv\Scripts\Activate.ps1
```

**Success:** You should see `(.venv)` at the start of your prompt.

**If you get an error** about execution policy:

```powershell
# Run this once (allows scripts you create)
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# Then try activating again
.\.venv\Scripts\Activate.ps1
```

### Step 6: Install Dependencies

**With venv active:**

```powershell
# Upgrade pip first (recommended)
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**This installs:**
- LangChain (AI framework)
- OpenAI SDK (for OpenRouter)
- Pandas, yfinance (data processing)
- Rich, Questionary (beautiful CLI)
- ChromaDB (vector database)
- And more... (~50 packages)

**Takes:** 2-5 minutes depending on your internet speed.

### Step 7: Configure API Keys

#### A) Get Your API Keys

**OpenRouter:**
1. Go to [openrouter.ai](https://openrouter.ai/)
2. Sign up or log in
3. Navigate to: **Settings → API Keys**
4. Click "Create API Key"
5. Copy the key (starts with `sk-or-v1-...`)

**Alpha Vantage:**
1. Go to [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)
2. Enter your email
3. Check your email for the API key
4. Copy the key

#### B) Add Keys to .env File

```powershell
# Open .env in your editor (Notepad, VS Code, Zed, etc.)
notepad .env
```

**Replace the placeholders:**

```env
# Change this line:
OPENAI_API_KEY=sk-or-v1-REPLACE_WITH_YOUR_OPENROUTER_KEY

# To your actual key:
OPENAI_API_KEY=sk-or-v1-abc123xyz789...

# Same for Alpha Vantage:
ALPHA_VANTAGE_API_KEY=YOUR_ACTUAL_KEY_HERE
```

**⚠️ IMPORTANT:**
- Remove `REPLACE_WITH_` text
- No quotes around the keys
- No spaces before/after the `=`
- Save the file

### Step 8: Validate Everything

```powershell
# Run the comprehensive setup checker
python scripts/check_setup.py
```

**What it checks:**
- ✅ Python version (3.10+)
- ✅ All packages installed
- ✅ API keys configured correctly
- ✅ API keys not placeholders
- ✅ Configuration valid
- ✅ Directories exist
- ✅ Internet connection

**Expected result:** All checks pass ✅

If anything fails, see [Troubleshooting](#troubleshooting).

---

## Configuration

### Environment Variables

TradingAgents supports extensive configuration via `.env` file.

#### Basic Configuration (Required)

```env
# Required: AI Model API Key
OPENAI_API_KEY=sk-or-v1-your-openrouter-key

# Required: Market Data API Key
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key
```

#### Advanced Configuration (Optional)

```env
# LLM Provider Settings
LLM_PROVIDER=openrouter
BACKEND_URL=https://openrouter.ai/api/v1
DEEP_THINK_MODEL=anthropic/claude-3.5-sonnet
QUICK_THINK_MODEL=openai/gpt-4o-mini

# Directory Settings
TRADINGAGENTS_DATA_DIR=C:\TradingData
TRADINGAGENTS_RESULTS_DIR=C:\TradingResults
TRADINGAGENTS_CACHE_DIR=C:\TradingCache

# Data Vendors
CORE_STOCK_VENDOR=yfinance
TECHNICAL_INDICATORS_VENDOR=yfinance
FUNDAMENTAL_DATA_VENDOR=alpha_vantage
NEWS_DATA_VENDOR=alpha_vantage

# Analysis Parameters
MAX_DEBATE_ROUNDS=2
MAX_RISK_DISCUSS_ROUNDS=2
MAX_RECUR_LIMIT=100
```

### Model Selection

OpenRouter provides access to many models:

| Model | Provider | Speed | Cost | Best For |
|-------|----------|-------|------|----------|
| `openai/gpt-4o-mini` | OpenAI | Fast | $ | Quick analysis |
| `openai/gpt-4o` | OpenAI | Medium | $$$ | High quality |
| `anthropic/claude-3.5-sonnet` | Anthropic | Medium | $$$ | Best reasoning |
| `google/gemini-pro` | Google | Fast | $$ | Good balance |
| `meta-llama/llama-3.1-8b-instruct` | Meta | Very Fast | $ | Budget option |

**Tip:** Start with `gpt-4o-mini` for testing, upgrade to `claude-3.5-sonnet` for production.

---

## Running TradingAgents

### Method 1: Quick Demo Script

**Test a single stock quickly:**

```powershell
# With defaults (NVDA on 2024-05-10)
python openrouter_demo.py

# Custom ticker
python openrouter_demo.py --ticker AAPL

# Custom ticker and date
python openrouter_demo.py --ticker TSLA --date 2024-06-15

# Different model
python openrouter_demo.py --ticker MSFT --deep-model anthropic/claude-3.5-sonnet

# See all options
python openrouter_demo.py --help
```

### Method 2: Interactive CLI

**Full-featured command-line interface:**

```powershell
# Start the CLI
python -m cli.main
```

**You'll be prompted for:**
1. **LLM Provider** - Select "Openrouter"
2. **Stock Ticker** - e.g., `NVDA`, `AAPL`, `TSLA`
3. **Analysis Date** - Format: `YYYY-MM-DD`
4. **Analysts** - Choose which types of analysis to run

### Method 3: From Zed Editor

**If you use Zed:**

1. Open the project in Zed
2. Press **Ctrl+Shift+P** (Command Palette)
3. Type "task spawn"
4. Select a task:
   - **✅ Check Setup** - Validate configuration
   - **🧪 Test OpenRouter** - Quick connection test
   - **📊 Quick Test - NVDA** - Analyze NVIDIA
   - **🚀 Run TradingAgents CLI** - Full interface

### Method 4: From Scratch (Python API)

**Programmatic usage:**

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Configure for OpenRouter
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openrouter"
config["backend_url"] = "https://openrouter.ai/api/v1"
config["deep_think_llm"] = "openai/gpt-4o-mini"
config["quick_think_llm"] = "openai/gpt-4o-mini"

# Create trading agents
ta = TradingAgentsGraph(debug=True, config=config)

# Analyze a stock
final_state, decision = ta.propagate("AAPL", "2024-05-10")

print(f"Decision: {decision}")
```

---

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

### Quick Fixes

**PowerShell won't run Activate.ps1:**
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**"API key not found" error:**
- Check `.env` file exists in project root
- Verify keys don't have `REPLACE_WITH_` text
- No spaces around `=` sign

**"Rate limit exceeded":**
- Alpha Vantage free tier: 5 calls/min, 100/day
- Wait 1 minute and try again
- Consider upgrading to premium

**"Model not found":**
- Check available models at [openrouter.ai/models](https://openrouter.ai/models)
- Use format: `provider/model-name`
- Try `openai/gpt-4o-mini` (always available)

**Python version too old:**
- Requires Python 3.10+
- Download from [python.org](https://www.python.org/downloads/)
- Make sure "Add to PATH" is checked during install

---

## Advanced Usage

### Custom Analysis Script

Create `my_analysis.py`:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.utils import logger

# Load config from .env automatically
config = DEFAULT_CONFIG.copy()

# Analyze multiple stocks
tickers = ["NVDA", "AAPL", "TSLA", "MSFT"]
date = "2024-06-01"

for ticker in tickers:
    logger.info(f"Analyzing {ticker}...")

    ta = TradingAgentsGraph(debug=False, config=config)
    _, decision = ta.propagate(ticker, date)

    logger.info(f"{ticker} Decision: {decision}")
    print(f"\n{'='*70}\n")
```

### Batch Analysis

See `scripts/batch_analyze.py` for analyzing multiple stocks at once.

### Custom Data Sources

Modify `data_vendors` in `.env`:

```env
# Use local data instead of APIs
CORE_STOCK_VENDOR=local
FUNDAMENTAL_DATA_VENDOR=local

# Mix and match
TECHNICAL_INDICATORS_VENDOR=yfinance
NEWS_DATA_VENDOR=openai
```

### Logging Configuration

```python
from tradingagents.utils import get_logger

# Create custom logger
logger = get_logger(
    name="my_analysis",
    level="DEBUG",
    log_file="logs/my_analysis.log"
)

logger.debug("Detailed debug info")
logger.info("Normal progress updates")
logger.warning("Warning messages")
logger.error("Error messages")
```

---

## Next Steps

- **Read:** [REFACTORING.md](REFACTORING.md) - Learn about code improvements
- **Read:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Detailed problem solutions
- **Explore:** `scripts/` - Helper utilities
- **Join:** [TauricResearch Discord](https://discord.com/invite/hk9PGKShPK)

---

## Files and Folders

```
TradingAgents/
├── .env                    # Your API keys (DO NOT COMMIT!)
├── .env.example            # Template for .env
├── .gitignore              # Files to ignore in Git
├── .zed/                   # Zed editor tasks
│   └── tasks.json
├── README.md               # Original project README
├── SETUP_GUIDE.md          # This file
├── REFACTORING.md          # Code improvements documentation
├── TROUBLESHOOTING.md      # Detailed problem solutions
├── openrouter_demo.py      # Quick demo script
├── requirements.txt        # Python dependencies
├── cli/                    # Command-line interface
│   ├── main.py            # CLI entry point
│   └── utils.py           # CLI utilities
├── scripts/               # Helper scripts
│   ├── check_setup.py     # Setup validator
│   └── README.md          # Scripts documentation
├── tradingagents/         # Main package
│   ├── agents/            # Trading agents
│   ├── dataflows/         # Data fetching
│   ├── graph/             # Agent orchestration
│   ├── utils/             # Utilities
│   │   ├── logging_utils.py
│   │   └── error_handling.py
│   └── default_config.py  # Configuration
└── .venv/                 # Virtual environment (created by you)
```

---

## Support

**Issues:** [GitHub Issues](https://github.com/TauricResearch/TradingAgents/issues)
**Discord:** [TradingResearch Community](https://discord.com/invite/hk9PGKShPK)
**Email:** Check the main [README.md](README.md) for contact info

---

## License

See [LICENSE](LICENSE) file for details.
