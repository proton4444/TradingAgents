# TradingAgents Scripts

Utility scripts for TradingAgents setup, testing, and maintenance.

## Available Scripts

### `check_setup.py`

Comprehensive setup validation script that checks:
- Python version compatibility
- Required package installation
- API key configuration
- Directory structure
- Internet connectivity
- Configuration validity

**Usage:**
```bash
python scripts/check_setup.py
```

**What it checks:**
- ✅ Python 3.10+ installed
- ✅ All required packages present
- ✅ API keys configured (not placeholders)
- ✅ Configuration valid
- ✅ Directories exist or can be created
- ✅ Internet connection active

**Output:**
- Detailed status tables for each check
- Summary of passed/failed checks
- Helpful suggestions if something is wrong

## Adding New Scripts

When creating new scripts:

1. Place them in this `scripts/` directory
2. Make them executable (if on Linux/Mac): `chmod +x script_name.py`
3. Add a shebang line: `#!/usr/bin/env python`
4. Document usage in this README
5. Add a task to `.zed/tasks.json` for easy access in Zed

## Running Scripts

### From Command Line

```bash
# Activate virtual environment first
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Linux/Mac

# Run any script
python scripts/check_setup.py
```

### From Zed Editor

1. Open command palette: Ctrl+Shift+P (or Cmd+Shift+P)
2. Type "task spawn" or "run task"
3. Select the script task from the menu

## Common Script Patterns

### Loading Environment Variables
```python
from dotenv import load_dotenv
load_dotenv()
```

### Adding Project to Path
```python
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
```

### Using Rich Console
```python
from rich.console import Console
console = Console()
console.print("[bold green]Success![/bold green]")
```

### Importing TradingAgents
```python
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.utils import logger, ConfigurationError
```
