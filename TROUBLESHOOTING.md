# TradingAgents Troubleshooting Guide

Comprehensive solutions to common problems when using TradingAgents on Windows with OpenRouter.

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Configuration Problems](#configuration-problems)
3. [API and Network Errors](#api-and-network-errors)
4. [Runtime Errors](#runtime-errors)
5. [Performance Issues](#performance-issues)
6. [Data Fetching Problems](#data-fetching-problems)
7. [Model and LLM Issues](#model-and-llm-issues)
8. [Advanced Debugging](#advanced-debugging)

---

## Installation Issues

### PowerShell Execution Policy Error

**Error:**
```
.\.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

**Cause:** Windows PowerShell security policy prevents running scripts.

**Solution:**
```powershell
# Option 1: Set for current user only (recommended)
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# Option 2: Temporarily bypass (less secure)
PowerShell -ExecutionPolicy Bypass

# Then try activating again
.\.venv\Scripts\Activate.ps1
```

**What this does:** `RemoteSigned` allows scripts you create locally while requiring downloaded scripts to be signed.

---

###  Python Not Found

**Error:**
```
'py' is not recognized as an internal or external command
```

**Cause:** Python not installed or not in PATH.

**Solutions:**

1. **Check if Python is installed:**
   ```powershell
   python --version
   # Try alternative
   python3 --version
   ```

2. **If not installed:**
   - Download from [python.org](https://www.python.org/downloads/)
   - **IMPORTANT:** Check "Add Python to PATH" during installation

3. **If installed but not in PATH:**
   - Search Windows for "Environment Variables"
   - Edit "Path" variable
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\`
   - Also add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts\`

---

### Package Installation Fails

**Error:**
```
ERROR: Could not build wheels for XXX
```

**Common causes and solutions:**

**1. Missing Microsoft C++ Build Tools:**
```powershell
# Download and install:
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Select "Desktop development with C++"
```

**2. Outdated pip:**
```powershell
python -m pip install --upgrade pip
```

**3. Specific package issues:**
```powershell
# Try installing problematic package separately
pip install --upgrade packagename

# Or skip it temporarily
pip install -r requirements.txt --no-binary :all:
```

**4. Network/proxy issues:**
```powershell
# Use a different index
pip install -r requirements.txt --index-url https://pypi.org/simple
```

---

### Git Clone Fails

**Error:**
```
fatal: unable to access 'https://github.com/...': Could not resolve host
```

**Solutions:**

1. **Check internet connection**
2. **Try HTTPS instead of SSH:**
   ```powershell
   git clone https://github.com/YOUR_USERNAME/TradingAgents.git
   ```
3. **Configure Git proxy (if behind corporate firewall):**
   ```powershell
   git config --global http.proxy http://proxy.server:port
   ```

---

## Configuration Problems

### API Keys Not Recognized

**Error:**
```
❌ ERROR: OPENAI_API_KEY not found in .env file!
```

**Checklist:**

1. **File exists:**
   ```powershell
   # Check if .env exists
   ls .env
   ```

2. **File is in project root** (same folder as `openrouter_demo.py`)

3. **Keys are not placeholders:**
   ```env
   # ❌ WRONG:
   OPENAI_API_KEY=REPLACE_WITH_YOUR_KEY

   # ✅ CORRECT:
   OPENAI_API_KEY=sk-or-v1-abc123xyz789...
   ```

4. **No spaces around equals:**
   ```env
   # ❌ WRONG:
   OPENAI_API_KEY = sk-or-v1-...

   # ✅ CORRECT:
   OPENAI_API_KEY=sk-or-v1-...
   ```

5. **No quotes:**
   ```env
   # ❌ WRONG:
   OPENAI_API_KEY="sk-or-v1-..."

   # ✅ CORRECT:
   OPENAI_API_KEY=sk-or-v1-...
   ```

6. **File saved as `.env`, not `.env.txt`:**
   ```powershell
   # Check actual filename
   Get-ChildItem -Force | Where-Object {$_.Name -like ".env*"}
   ```

---

### Configuration Validation Fails

**Run the checker to see what's wrong:**
```powershell
python scripts/check_setup.py
```

**Common issues:**

**Missing configuration:**
```
Missing required configuration: llm_provider
```
**Solution:** Set in `.env`:
```env
LLM_PROVIDER=openrouter
```

**Invalid provider:**
```
Invalid llm_provider: wrong_name
```
**Solution:** Must be one of: `openai`, `anthropic`, `google`, `openrouter`, `ollama`

**Directory issues:**
```
Cannot create directory data_dir='X:\InvalidPath'
```
**Solution:** Use valid Windows path or remove to use default (`./data`)

---

## API and Network Errors

### OpenRouter API Errors

**Error: "Invalid API key"**

**Causes:**
1. Key is incorrect or expired
2. Key has wrong prefix (should start with `sk-or-v1-`)
3. Key has extra spaces/newlines

**Solutions:**
1. **Verify key at [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys)**
2. **Copy key again** (don't type it manually)
3. **Check for hidden characters:**
   ```powershell
   # View actual characters in .env
   Get-Content .env | Format-Hex
   ```

---

**Error: "Rate limit exceeded"**

**Causes:**
1. Free tier has limits
2. Too many requests in short time

**Solutions:**
1. **Wait 60 seconds** and try again
2. **Check usage at [openrouter.ai](https://openrouter.ai/)**
3. **Add credits** to your account
4. **Use slower models** (cheaper, less frequent calls)

---

**Error: "Model not found" or "Model not available"**

**Causes:**
1. Model name incorrect
2. Model not available on your account
3. Model temporarily unavailable

**Solutions:**
1. **Check available models:** [openrouter.ai/models](https://openrouter.ai/models)
2. **Use correct format:** `provider/model-name`
   ```env
   # ✅ CORRECT:
   DEEP_THINK_MODEL=openai/gpt-4o-mini

   # ❌ WRONG:
   DEEP_THINK_MODEL=gpt-4o-mini
   ```
3. **Try default model:**
   ```env
   DEEP_THINK_MODEL=openai/gpt-4o-mini
   QUICK_THINK_MODEL=openai/gpt-4o-mini
   ```

---

### Alpha Vantage API Errors

**Error: "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute"**

**Cause:** Hit rate limit (5 calls/minute on free tier)

**Solutions:**
1. **Wait 1 minute** between analyses
2. **Use caching** (automatically enabled)
3. **Upgrade to premium:** [alphavantage.co/premium](https://www.alphavantage.co/premium/)
4. **Switch to yfinance** for some data:
   ```env
   CORE_STOCK_VENDOR=yfinance
   TECHNICAL_INDICATORS_VENDOR=yfinance
   ```

---

**Error: "Invalid API key"**

**Solutions:**
1. **Verify key at [alphavantage.co](https://www.alphavantage.co/support/#support)**
2. **Request new key** if needed (instant, free)
3. **Check .env file** for typos

---

### Network Connection Errors

**Error: "Connection timeout" or "Network unreachable"**

**Solutions:**
1. **Check internet connection:**
   ```powershell
   python scripts/check_setup.py
   # Look for "Internet" check
   ```

2. **Test specific APIs:**
   ```powershell
   # Test OpenRouter
   curl https://openrouter.ai/api/v1/models

   # Test Alpha Vantage
   curl "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
   ```

3. **Check firewall/antivirus** (may block Python)

4. **Try different network** (mobile hotspot, etc.)

5. **Configure proxy if behind corporate firewall:**
   ```powershell
   # Set environment variables
   $env:HTTP_PROXY="http://proxy.company.com:8080"
   $env:HTTPS_PROXY="http://proxy.company.com:8080"
   ```

---

## Runtime Errors

### Module Not Found Errors

**Error:**
```
ModuleNotFoundError: No module named 'tradingagents'
```

**Causes:**
1. Virtual environment not activated
2. Running from wrong directory
3. Package not installed

**Solutions:**
1. **Activate venv:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   # Should see (.venv) in prompt
   ```

2. **Check current directory:**
   ```powershell
   pwd
   # Should be in TradingAgents root
   ```

3. **Reinstall packages:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```powershell
   python -c "import tradingagents; print('OK')"
   ```

---

### Import Errors

**Error:**
```
ImportError: cannot import name 'XXX' from 'tradingagents'
```

**Solutions:**
1. **Update dependencies:**
   ```powershell
   pip install --upgrade -r requirements.txt
   ```

2. **Clear Python cache:**
   ```powershell
   # Remove __pycache__ folders
   Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
   ```

3. **Reinstall package:**
   ```powershell
   pip uninstall tradingagents
   pip install -e .
   ```

---

### Memory Errors

**Error:**
```
MemoryError: Unable to allocate array
```

**Causes:**
1. Analyzing too many stocks at once
2. Large date range
3. Insufficient RAM

**Solutions:**
1. **Analyze fewer stocks:**
   ```python
   # Instead of 100 stocks, do 10 at a time
   ```

2. **Close other programs** to free RAM

3. **Use lighter models:**
   ```env
   # Smaller, faster models use less memory
   DEEP_THINK_MODEL=openai/gpt-4o-mini
   ```

4. **Increase virtual memory** (Windows):
   - Settings → System → About → Advanced system settings
   - Performance Settings → Advanced → Virtual memory

---

## Performance Issues

### Slow Analysis

**Symptom:** Analysis takes 5+ minutes per stock

**Causes and solutions:**

1. **Using expensive models:**
   ```env
   # Try faster models
   QUICK_THINK_MODEL=openai/gpt-4o-mini
   ```

2. **Alpha Vantage rate limits:**
   - Free tier is throttled
   - Consider premium: [alphavantage.co/premium](https://www.alphavantage.co/premium/)

3. **Network latency:**
   - Check internet speed
   - Use wired connection if possible

4. **Too many agent rounds:**
   ```env
   # Reduce debate rounds
   MAX_DEBATE_ROUNDS=1
   MAX_RISK_DISCUSS_ROUNDS=1
   ```

---

### High API Costs

**Symptom:** OpenRouter charges are high

**Solutions:**

1. **Use cheaper models:**
   ```env
   # GPT-4o-mini is ~15x cheaper than GPT-4o
   DEEP_THINK_MODEL=openai/gpt-4o-mini
   QUICK_THINK_MODEL=openai/gpt-4o-mini
   ```

2. **Reduce rounds:**
   ```env
   MAX_DEBATE_ROUNDS=1
   MAX_RISK_DISCUSS_ROUNDS=1
   ```

3. **Set spending limits:** [openrouter.ai/settings/limits](https://openrouter.ai/settings/limits)

4. **Monitor usage:** [openrouter.ai/activity](https://openrouter.ai/activity)

---

## Data Fetching Problems

### Stock Data Not Found

**Error:**
```
DataFetchError: Failed to fetch data for XXXXX
```

**Solutions:**

1. **Verify ticker symbol:**
   ```powershell
   # Check at Yahoo Finance
   # https://finance.yahoo.com/quote/TICKER
   ```

2. **Use correct format:**
   - US stocks: `AAPL`, `TSLA`, `NVDA`
   - Non-US: Add exchange suffix: `0700.HK` (Hong Kong)

3. **Check if market is open/closed**
   - Can't get realtime data if market closed
   - Use historical dates

4. **Try different vendor:**
   ```env
   # Switch from Alpha Vantage to yfinance
   CORE_STOCK_VENDOR=yfinance
   ```

---

### Historical Data Issues

**Error:**
```
No data available for date YYYY-MM-DD
```

**Solutions:**

1. **Use trading days only:**
   - Not weekends
   - Not holidays
   - Use dates like: `2024-06-03` (Monday)

2. **Check data range:**
   - Some stocks have limited history
   - Newly listed stocks have less data

3. **Use recent dates:**
   - Alpha Vantage free tier may have delays
   - Try date from 2-3 weeks ago

---

## Model and LLM Issues

### Inconsistent Results

**Symptom:** Same analysis gives different results each time

**Cause:** LLMs are non-deterministic

**This is normal!** But you can:

1. **Set temperature = 0** for more consistency:
   ```python
   # In your custom code
   llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
   ```

2. **Run multiple times** and average results

3. **Use same model** consistently

4. **Use reasoning models** (more consistent):
   ```env
   DEEP_THINK_MODEL=anthropic/claude-3.5-sonnet
   ```

---

### Model Timeout

**Error:**
```
Timeout waiting for model response
```

**Solutions:**

1. **Try again** (sometimes temporary)

2. **Use faster model:**
   ```env
   DEEP_THINK_MODEL=openai/gpt-4o-mini
   ```

3. **Check OpenRouter status:** [status.openrouter.ai](https://status.openrouter.ai)

4. **Increase timeout** in custom code:
   ```python
   llm = ChatOpenAI(model="...", timeout=300)  # 5 minutes
   ```

---

## Advanced Debugging

### Enable Debug Logging

```python
from tradingagents.utils import get_logger

logger = get_logger(level="DEBUG", log_file="logs/debug.log")
```

**Or use debug mode:**
```python
ta = TradingAgentsGraph(debug=True, config=config)
```

---

### Check Configuration

```python
from tradingagents.default_config import DEFAULT_CONFIG, validate_config

print("Current config:")
for key, value in DEFAULT_CONFIG.items():
    print(f"  {key}: {value}")

is_valid, errors = validate_config(DEFAULT_CONFIG)
if not is_valid:
    print("Errors:")
    for error in errors:
        print(f"  - {error}")
```

---

### Test API Connections Individually

**Test OpenRouter:**
```python
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[{"role": "user", "content": "Say 'OK'"}]
)

print(response.choices[0].message.content)
```

**Test Alpha Vantage:**
```python
import requests
import os

api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={api_key}"

response = requests.get(url)
print(response.json())
```

---

### Clear Cache

```powershell
# Clear data cache
Remove-Item -Recurse -Force tradingagents\dataflows\data_cache\*

# Clear Python cache
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force

# Clear results
Remove-Item -Recurse -Force results\*
```

---

### Reinstall Everything

**Nuclear option - start fresh:**

```powershell
# Deactivate venv
deactivate

# Remove venv
Remove-Item -Recurse -Force .venv

# Recreate venv
py -3.11 -m venv .venv

# Activate
.\.venv\Scripts\Activate.ps1

# Reinstall
pip install --upgrade pip
pip install -r requirements.txt

# Validate
python scripts/check_setup.py
```

---

## Still Having Issues?

### Diagnostic Report

**Create a diagnostic report:**

```powershell
# Run all checks and save output
python scripts/check_setup.py > diagnostic_report.txt
```

**Include when asking for help:**
1. Output of `diagnostic_report.txt`
2. Python version: `py --version`
3. OS: `systeminfo | findstr /C:"OS"`
4. Error message (full traceback)
5. What you were trying to do

### Get Help

1. **Check existing issues:** [GitHub Issues](https://github.com/TauricResearch/TradingAgents/issues)
2. **Create new issue:** Include diagnostic report
3. **Join Discord:** [TradingResearch Community](https://discord.com/invite/hk9PGKShPK)

---

## Common Error Codes

| Error Code | Meaning | Solution |
|------------|---------|----------|
| 401 | Unauthorized | Check API key |
| 403 | Forbidden | Check permissions/credits |
| 429 | Rate limit | Wait and retry |
| 500 | Server error | Try again later |
| 503 | Service unavailable | Check service status |

---

## Prevention Tips

1. **Always activate venv** before running commands
2. **Run `check_setup.py`** before each session
3. **Monitor API usage** to avoid surprises
4. **Use version control** (Git) for your changes
5. **Keep dependencies updated:** `pip install --upgrade -r requirements.txt`
6. **Read error messages** carefully (they usually tell you what's wrong!)

---

## Useful Commands Reference

```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Check setup
python scripts/check_setup.py

# Quick test
python openrouter_demo.py

# Full CLI
python -m cli.main

# Check Python version
py --version

# List installed packages
pip list

# Update all packages
pip install --upgrade -r requirements.txt

# Clear cache
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
```

---

**Remember:** Most issues are configuration problems. Run `check_setup.py` first!
