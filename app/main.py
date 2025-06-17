# ===========================================
# Project Structure
# - Assume you are in a folder named statistics_service
# - Only complete one module at a time, do not start creating or working on other modules unless directed to
# - Assume all operations start from the root directory
# - Do not create files during setup
# - Maintain a modular, organized code structure
# - Don't create unnecessary files (.gitignore, Makefiles, helper scripts, etc.)
# - Don't create docker-compose files
#
# Data Handling
# - Never overwrite the `historical_bars` table
# - Use real data, not test data
# - Always read configurations from the `.env` file
#
# Infrastructure
# - PostgreSQL is hosted on Digital Ocean (remote)
# - Verify topics and consumer groups exist; create them if missing
# - Never create multiple dev containers
#
# Development Environment
# - Keep Dockerfile minimal and functional
# - Keep `.devcontainer.json` configuration simple
# - Create only one dev container when needed
#
# Documentation
# - Create a detailed README with clear ground rules
# - Include setup instructions and usage guidelines
#
# Code Quality
# - Write minimal but clear comments
# - Avoid indentation errors
# - Be extremely careful with syntax
# - Don't add creative or additional functions beyond requirements
# - Follow a "simple and clean" approach to all implementations
# ===========================================
# Main Entry Point for Running Statistics
 
# Create a Python module named `main.py` inside the `app` folder of the `statistics_service` project. This file will serve as the entry point for orchestrating the flow of data: pulling historical bars, computing enabled statistics, and writing the results back to the database.
 
# 📁 File Location:
# statistics_service/app/main.py
 
# 🧱 Requirements:
# - The script must:
#   - Read all configuration from `config/settings.py`
#   - Use `data_ingestion/query.py` to fetch historical bar data for each symbol and timeframe
#   - Dynamically check which statistics are enabled using the `STATS_ENABLED` environment variable
#   - Call the appropriate statistical functions from `statistics/zscore.py`, `statistics/correlation.py`, and `statistics/cointegration.py`
#   - Use `data_ingestion/writer.py` to write the latest computed statistic back to the database
# - Iterate through each symbol and timeframe combination
# - Assume the `historical_bars` table contains valid real data
# - Do not use simulated/test/mocked data
 
# 🧪 Execution (from inside the container):
# ```bash
# python3 app/main.py
# ```
 
# 🧼 Code Comments Requirement:
# - You must preserve the project guidelines comment block at the top of this file.
# - Never remove or modify the comment block inserted during Prompt #2.
# - Place all implementation code below that comment block, keeping it untouched.
 
# ✅ Guidelines (Recap):
# - Only work on this file as the orchestration layer—do not modify other modules.
# - All configuration must be loaded from `settings.py`
# - Never overwrite or affect the `historical_bars` table
# - Be extremely careful with syntax and indentation
# - Use only real data—no test placeholders or debugging code
# - Write minimal but clear inline comments
# - Follow a “simple and clean” execution flow

import sys
import os
from datetime import datetime, timezone

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import STATS_ENABLED, DEFAULT_TIMEFRAME, COINTEGRATED_SYMBOLS
from data_ingestion.query import fetch_bars
from data_ingestion.writer import write_statistic
from stats.zscore import calculate_zscore
from stats.correlation import calculate_correlation
from stats.cointegration import calculate_cointegration

def main():
    """
    Main orchestration function for computing and storing statistics.
    """
    # Define symbols and timeframes to process
    symbols = COINTEGRATED_SYMBOLS  # Symbols from environment configuration
    timeframes = ["5 mins", "15 mins", "30 mins", "1 hour"]  # Bar sizes as they appear in DB
    
    print("Starting statistics computation...")
    
    for symbol in symbols:
        for timeframe in timeframes:
            print(f"Processing {symbol} at {timeframe} timeframe...")
            
            # Fetch historical bar data
            bars = fetch_bars(symbol, timeframe, 100)  # Get last 100 bars
            
            if not bars or len(bars) < 2:
                print(f"  Insufficient data for {symbol} at {timeframe}")
                continue            # Extract price data (close_price is at index 10)
            prices = [float(bar[10]) if bar[10] is not None else None for bar in bars]
            
            # Process enabled statistics
            timestamp = datetime.now(timezone.utc)
            
            if "zscore" in STATS_ENABLED:
                # Convert timeframe to minutes for MLflow logging
                timeframe_minutes = None
                if timeframe == "5 mins":
                    timeframe_minutes = 5
                elif timeframe == "15 mins":
                    timeframe_minutes = 15
                elif timeframe == "30 mins":
                    timeframe_minutes = 30
                elif timeframe == "1 hour":
                    timeframe_minutes = 60
                
                # Calculate z-score for the price series with symbol and timeframe
                z_scores = calculate_zscore(prices, symbol, timeframe_minutes)
                if z_scores and z_scores[-1] is not None:
                    # Write the latest z-score value - convert to Python float
                    zscore_value = float(z_scores[-1])
                    write_statistic(symbol, timeframe, "zscore", zscore_value, timestamp)
                    print(f"  Z-score computed: {zscore_value:.4f}")
            
            if "correlation" in STATS_ENABLED and len(symbols) > 1:
                # Calculate correlation with SPY (market benchmark)
                if symbol != "SPY":
                    spy_bars = fetch_bars("SPY", timeframe, len(bars))
                    if spy_bars and len(spy_bars) == len(bars):
                        spy_prices = [float(bar[10]) if bar[10] is not None else None for bar in spy_bars]
                        correlation = calculate_correlation(prices, spy_prices)
                        if correlation is not None:
                            # Convert to Python float to avoid numpy type issues
                            correlation_value = float(correlation)
                            write_statistic(symbol, timeframe, "correlation", correlation_value, timestamp)
                            print(f"  Correlation with SPY: {correlation_value:.4f}")
            
            if "cointegration" in STATS_ENABLED and len(symbols) > 1:
                # Calculate cointegration with SPY (market benchmark)
                if symbol != "SPY":
                    spy_bars = fetch_bars("SPY", timeframe, len(bars))
                    if spy_bars and len(spy_bars) == len(bars):
                        spy_prices = [float(bar[10]) if bar[10] is not None else None for bar in spy_bars]
                        cointegration_pvalue = calculate_cointegration(prices, spy_prices)
                        if cointegration_pvalue is not None:
                            # Convert to Python float to avoid numpy type issues
                            cointegration_value = float(cointegration_pvalue)
                            write_statistic(symbol, timeframe, "cointegration", cointegration_value, timestamp)
                            print(f"  Cointegration p-value with SPY: {cointegration_value:.4f}")

if __name__ == "__main__":
    main()
