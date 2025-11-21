"""
TradingAgents Web UI - Streamlit Application

A simple web interface for running trading analysis and visualizing results.

Usage:
    streamlit run app.py

The app will open in your browser at http://localhost:8501
"""

import os
import sys
import traceback
from datetime import datetime, timedelta
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph


# Page configuration
st.set_page_config(
    page_title="TradingAgents - AI Trading Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_api_keys():
    """Load API keys from .env file."""
    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    return openai_key, alpha_vantage_key


def validate_api_keys(openai_key, alpha_vantage_key):
    """Validate that API keys are present and not placeholder values."""
    errors = []

    if not openai_key:
        errors.append("OPENAI_API_KEY not found in .env file")
    elif "REPLACE" in openai_key.upper() or "your_" in openai_key.lower():
        errors.append("OPENAI_API_KEY still contains placeholder text")

    if not alpha_vantage_key:
        errors.append("ALPHA_VANTAGE_API_KEY not found in .env file")
    elif "REPLACE" in alpha_vantage_key.upper() or "your_" in alpha_vantage_key.lower():
        errors.append("ALPHA_VANTAGE_API_KEY still contains placeholder text")

    return errors


def get_config(deep_model, quick_model):
    """Create TradingAgents configuration."""
    config = DEFAULT_CONFIG.copy()
    config["deep_think_llm"] = deep_model
    config["quick_think_llm"] = quick_model
    return config


@st.cache_resource
def initialize_trading_agents(deep_model, quick_model):
    """Initialize TradingAgents (cached to avoid re-initialization)."""
    config = get_config(deep_model, quick_model)
    return TradingAgentsGraph(debug=True, config=config)


def create_price_chart(ticker, date):
    """Create a placeholder price chart (enhanced version would fetch real data)."""
    # This is a simplified version - in production, you'd fetch real historical data
    dates = pd.date_range(end=date, periods=30, freq='D')

    # Create placeholder data
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=[100 + i * 2 + (i % 5) for i in range(30)],
        mode='lines',
        name='Price',
        line=dict(color='#1f77b4', width=2)
    ))

    fig.update_layout(
        title=f"{ticker} Price Chart (Last 30 Days)",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        hovermode='x unified',
        height=400
    )

    return fig


def main():
    """Main application."""

    # Header
    st.title("📈 TradingAgents - AI-Powered Trading Analysis")
    st.markdown("### Analyze stocks with AI-powered multi-agent reasoning")

    # Check API keys
    openai_key, alpha_vantage_key = load_api_keys()
    api_errors = validate_api_keys(openai_key, alpha_vantage_key)

    if api_errors:
        st.error("⚠️ API Key Configuration Issues:")
        for error in api_errors:
            st.error(f"  • {error}")
        st.info("Please edit your `.env` file and add your API keys. See `.env.example` for reference.")
        st.stop()

    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Display current config
        with st.expander("🔑 API Keys Status", expanded=False):
            st.success(f"✅ OpenRouter: {openai_key[:15]}...")
            st.success(f"✅ Alpha Vantage: {alpha_vantage_key[:8]}...")

        with st.expander("🤖 LLM Configuration", expanded=False):
            st.info(f"**Provider:** {DEFAULT_CONFIG['llm_provider']}")
            st.info(f"**Backend:** {DEFAULT_CONFIG['backend_url']}")
            st.info(f"**Deep Model:** {DEFAULT_CONFIG['deep_think_llm']}")
            st.info(f"**Quick Model:** {DEFAULT_CONFIG['quick_think_llm']}")

        st.divider()

        # Analysis inputs
        st.header("📊 Analysis Parameters")

        ticker = st.text_input(
            "Stock Ticker",
            value="NVDA",
            help="Enter a valid stock ticker symbol (e.g., AAPL, TSLA, MSFT)"
        ).upper()

        analysis_date = st.date_input(
            "Analysis Date",
            value=datetime(2024, 5, 10),
            max_value=datetime.now(),
            help="Select the date for analysis"
        )

        # Model selection
        st.subheader("Model Selection")

        available_models = [
            "openai/gpt-4o-mini",
            "openai/gpt-4o",
            "anthropic/claude-3.5-sonnet",
            "anthropic/claude-3-haiku",
            "google/gemini-pro",
            "meta-llama/llama-3.1-70b-instruct",
        ]

        deep_model = st.selectbox(
            "Deep Think Model",
            options=available_models,
            index=0,
            help="Model for complex reasoning and analysis"
        )

        quick_model = st.selectbox(
            "Quick Think Model",
            options=available_models,
            index=0,
            help="Model for quick analysis tasks"
        )

        st.divider()

        # Run analysis button
        run_analysis = st.button("🚀 Run Analysis", type="primary", use_container_width=True)

    # Main content area
    if not run_analysis:
        # Welcome screen
        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("### 🎯 Step 1\nConfigure your analysis parameters in the sidebar")

        with col2:
            st.info("### 🚀 Step 2\nClick 'Run Analysis' to start the AI analysis")

        with col3:
            st.info("### 📊 Step 3\nView results, charts, and trading recommendations")

        st.divider()

        # Features
        st.subheader("✨ Features")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **AI-Powered Analysis**
            - Multi-agent reasoning system
            - Advanced market analysis
            - Risk assessment
            - Sentiment analysis
            """)

        with col2:
            st.markdown("""
            **Data Sources**
            - Real-time stock data
            - Historical price analysis
            - News and sentiment
            - Technical indicators
            """)

        st.divider()

        st.info("👈 Get started by selecting a stock ticker and clicking 'Run Analysis' in the sidebar!")

    else:
        # Run the analysis
        date_str = analysis_date.strftime("%Y-%m-%d")

        st.header(f"Analysis Results: {ticker} ({date_str})")

        # Progress indicators
        with st.spinner("🔧 Initializing TradingAgents..."):
            try:
                ta = initialize_trading_agents(deep_model, quick_model)
                st.success("✅ TradingAgents initialized successfully")
            except Exception as e:
                st.error(f"❌ Error initializing TradingAgents: {str(e)}")
                with st.expander("See error details"):
                    st.code(traceback.format_exc())
                st.stop()

        # Run analysis
        with st.spinner(f"🤖 Analyzing {ticker}... This may take 1-2 minutes..."):
            progress_text = st.empty()

            progress_text.text("📊 Fetching stock data...")

            try:
                final_state, decision = ta.propagate(ticker, date_str)

                progress_text.text("✅ Analysis complete!")

            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")

                with st.expander("See error details"):
                    st.code(traceback.format_exc())

                with st.expander("Common Issues"):
                    st.markdown("""
                    **Possible causes:**
                    1. Invalid ticker symbol
                    2. API rate limits exceeded
                    3. Network connectivity issues
                    4. Invalid API keys
                    5. Model not available on your OpenRouter account

                    **Solutions:**
                    - Verify ticker symbol is valid
                    - Check Alpha Vantage rate limits (5 calls/min free tier)
                    - Ensure you have internet connectivity
                    - Verify API keys in `.env` file
                    """)

                st.stop()

        # Clear progress text
        progress_text.empty()

        # Display results
        st.success("✅ Analysis Complete!")

        # Trading Decision
        st.subheader("📈 Trading Decision")

        # Display decision with color based on recommendation
        if "buy" in decision.lower():
            st.success(decision)
        elif "sell" in decision.lower():
            st.error(decision)
        else:
            st.warning(decision)

        # Results in tabs
        tab1, tab2, tab3 = st.tabs(["📊 Summary", "📈 Charts", "🔍 Details"])

        with tab1:
            st.markdown("### Analysis Summary")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Ticker", ticker)

            with col2:
                st.metric("Analysis Date", date_str)

            with col3:
                st.metric("Status", "Completed", delta="✓")

            st.divider()

            # Display decision
            st.markdown("### 🎯 Trading Recommendation")
            st.info(decision)

            # Additional metrics (if available in final_state)
            if isinstance(final_state, dict):
                st.markdown("### 📋 Analysis Metrics")

                metrics_data = {}
                for key, value in final_state.items():
                    if isinstance(value, (str, int, float, bool)):
                        metrics_data[key] = value

                if metrics_data:
                    metrics_df = pd.DataFrame([metrics_data])
                    st.dataframe(metrics_df, use_container_width=True)

        with tab2:
            st.markdown("### 📈 Price Visualization")

            # Create and display chart
            try:
                fig = create_price_chart(ticker, date_str)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not generate price chart: {str(e)}")

            st.info("💡 **Note:** In production, this would show real historical price data and technical indicators.")

        with tab3:
            st.markdown("### 🔍 Full Analysis Details")

            st.markdown("#### Final State")
            st.json(final_state if isinstance(final_state, dict) else {"result": str(final_state)})

            st.markdown("#### Configuration Used")
            config_display = {
                "llm_provider": DEFAULT_CONFIG["llm_provider"],
                "backend_url": DEFAULT_CONFIG["backend_url"],
                "deep_think_model": deep_model,
                "quick_think_model": quick_model,
                "news_vendor": DEFAULT_CONFIG["data_vendors"]["news_data"],
            }
            st.json(config_display)

        # Download results
        st.divider()

        col1, col2 = st.columns([3, 1])

        with col1:
            st.success("✅ Analysis complete! Review the results above.")

        with col2:
            # Create download data
            download_data = {
                "ticker": ticker,
                "date": date_str,
                "decision": decision,
                "timestamp": datetime.now().isoformat(),
                "models": {
                    "deep": deep_model,
                    "quick": quick_model
                }
            }

            st.download_button(
                label="💾 Download Results (JSON)",
                data=str(download_data),
                file_name=f"{ticker}_{date_str}_analysis.json",
                mime="application/json"
            )


if __name__ == "__main__":
    main()
