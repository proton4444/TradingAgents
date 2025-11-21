# TradingAgents Web UI Guide

A simple, beautiful web interface for running TradingAgents analysis built with Streamlit.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Make sure your `.env` file is configured with your API keys:

```bash
# Copy the example file if you haven't already
cp .env.example .env

# Edit .env and add your keys
# OPENAI_API_KEY=your_openrouter_key_here
# ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

### 3. Launch the UI

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 📊 Features

### Interactive Analysis
- **Stock Selection**: Enter any valid stock ticker (AAPL, TSLA, NVDA, etc.)
- **Date Picker**: Choose the analysis date
- **Model Selection**: Pick from various AI models (GPT-4, Claude, Gemini, etc.)
- **One-Click Analysis**: Run complete trading analysis with a single button

### Visualization
- **Trading Decisions**: Clear buy/sell/hold recommendations
- **Analysis Summary**: Key metrics and insights
- **Price Charts**: Visual representation of stock data
- **Detailed Results**: Full analysis state and configuration

### User Experience
- 🎨 Clean, modern interface
- 📱 Responsive design
- ⚡ Fast initialization (cached)
- 💾 Download results as JSON
- 🔄 Real-time progress indicators

## 🖥️ Interface Overview

### Sidebar (Left Panel)
- **API Keys Status**: Verify your keys are loaded
- **LLM Configuration**: View current OpenRouter setup
- **Analysis Parameters**:
  - Stock ticker input
  - Date selection
  - Model selection (deep/quick thinking)
- **Run Analysis Button**: Start the analysis

### Main Area (Center/Right)
- **Welcome Screen**: Instructions and features (before analysis)
- **Results Display**: After running analysis
  - 📊 Summary Tab: Trading recommendation and key metrics
  - 📈 Charts Tab: Price visualization
  - 🔍 Details Tab: Full analysis state and configuration

## 🎯 Usage Examples

### Example 1: Basic Analysis

1. Enter ticker: `NVDA`
2. Select date: `2024-05-10`
3. Keep default models: `openai/gpt-4o-mini`
4. Click "🚀 Run Analysis"
5. View results in tabs

### Example 2: Advanced Analysis with Claude

1. Enter ticker: `AAPL`
2. Select date: `2024-06-15`
3. Change deep model to: `anthropic/claude-3.5-sonnet`
4. Change quick model to: `anthropic/claude-3-haiku`
5. Click "🚀 Run Analysis"
6. Download results

### Example 3: Multi-Stock Comparison

1. Run analysis for stock A
2. Download results
3. Change ticker to stock B
4. Run analysis again
5. Download results
6. Compare the JSON files

## ⚙️ Configuration

The UI uses the same configuration as the CLI:

- **LLM Provider**: OpenRouter (default)
- **Backend URL**: https://openrouter.ai/api/v1
- **Models**: Configurable via UI dropdowns
- **Data Vendors**: Same as configured in `default_config.py`

You can modify defaults in:
- `.env` file for API keys and environment variables
- `tradingagents/default_config.py` for system defaults

## 🐛 Troubleshooting

### UI Won't Start

```bash
# Check Streamlit is installed
streamlit --version

# Reinstall if needed
pip install streamlit plotly
```

### API Key Errors

Check your `.env` file:
```bash
cat .env

# Make sure keys don't contain:
# - "your_" prefix
# - "REPLACE" text
# - Empty values
```

### Analysis Fails

Common causes:
1. **Invalid Ticker**: Verify the stock symbol exists
2. **Rate Limits**: Alpha Vantage free tier = 5 calls/min
3. **Network Issues**: Check internet connection
4. **Model Access**: Verify model is available on your OpenRouter account

### Port Already in Use

If port 8501 is busy:
```bash
streamlit run app.py --server.port 8502
```

## 🔧 Customization

### Change Default Models

Edit the `available_models` list in `app.py`:

```python
available_models = [
    "openai/gpt-4o-mini",
    "anthropic/claude-3.5-sonnet",
    # Add your preferred models here
]
```

### Change Default Ticker/Date

Edit the default values:

```python
ticker = st.text_input("Stock Ticker", value="YOUR_DEFAULT")
analysis_date = st.date_input("Analysis Date", value=datetime(2024, 12, 1))
```

### Add More Visualizations

Extend the `tab2` section in the main function to add custom charts using Plotly.

## 📝 Tips

1. **API Rate Limits**: Wait 12 seconds between analyses on Alpha Vantage free tier
2. **Model Selection**: Use `gpt-4o-mini` for faster/cheaper analysis, `claude-3.5-sonnet` for deeper insights
3. **Save Results**: Always download important analysis results as JSON
4. **Browser Choice**: Works best in Chrome, Firefox, or Edge (latest versions)

## 🚀 Advanced Usage

### Run on Custom Port

```bash
streamlit run app.py --server.port 8080
```

### Run in Production Mode

```bash
streamlit run app.py --server.headless true --server.port 80
```

### Access from Network

```bash
streamlit run app.py --server.address 0.0.0.0
```

Then access from other devices at `http://YOUR_IP:8501`

## 📚 Additional Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **OpenRouter Models**: https://openrouter.ai/models
- **Alpha Vantage API**: https://www.alphavantage.co/documentation/

## 🆘 Support

If you encounter issues:

1. Check the error message in the UI
2. Look at the terminal output where you ran `streamlit run app.py`
3. Review the "Common Issues" section in the error expandable
4. Check your API keys and configuration

For more help, see the main project documentation or create an issue in the repository.
