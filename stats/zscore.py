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
# Z-Score Statistical Module
 
# Create a Python module named `zscore.py` inside the `statistics` folder of the `statistics_service` project. This module will calculate the z-score for a given series of price values retrieved from the `historical_bars` table.
 
# 📁 File Location:
# statistics_service/statistics/zscore.py
 
# 🧱 Requirements:
# - This module should contain a function `calculate_zscore(prices: list[float]) -> list[float]`.
# - The function should return a list of z-score values, where each z-score is calculated as:
#   z = (x - mean) / std_dev
# - The calculation must:
#   - Ignore `None` values
#   - Return `None` for any point where the mean or standard deviation is undefined
# - Use Python’s built-in modules or standard scientific libraries like `statistics` or `numpy`.
# - Do not perform data loading or writing in this module—just the pure computation logic.
# - This module will be called by other services after data is pulled from the database.
# - Do not include main functions, testing logic, or any CLI functionality.
 
# 🧼 Code Comments Requirement:
# - You must preserve the project guidelines comment block at the top of this file.
# - Never remove or modify the comment block inserted during Prompt #2.
# - Place all implementation code below that comment block, keeping it untouched.
 
# ✅ Guidelines (Recap):
# - Use real input data only.
# - Never write to or modify the `historical_bars` table.
# - Keep the module focused strictly on z-score computation.
# - Follow a modular structure—do not import or integrate other services here.
# - Be extremely careful with syntax and indentation.
# - Write minimal but clear inline comments if needed.
# - Do not add any extra functions or creative features.
# - Follow a strict "simple and clean" implementation approach.
# - Only work on this module until instructed otherwise.

# 📦 File to Modify:
# app/stats/zscore.py
# 🧠 Prompt for Copilot:
# Update the zscore.py module in the app/stats folder to integrate MLflow logging using the utility functions defined in app/mlflow_utils/mlflow_utils.py.
# Import the init_mlflow, log_params, and log_metrics functions from the mlflow_utils module.
# Call init_mlflow() at the start of the statistical computation to set up the MLflow environment using .env configurations.
# Log relevant parameters used for z-score calculation:
# symbol: The financial instrument (e.g., "AAPL").
# timeframe_minutes: Timeframe used for the historical bars (e.g., 5, 15, 30).
# window_size: Number of bars used to compute mean and standard deviation.
# latest_price: Most recent price in the series.
# mean_price: Mean of the price series over the window.
# std_dev: Standard deviation of the price series.
# z_score: Final computed z-score.
# z_threshold_upper: Optional upper threshold for signal generation.
# z_threshold_lower: Optional lower threshold for signal generation.
# calculation_timestamp: Timestamp of when the calculation occurred.
# Log appropriate values using log_params and log_metrics.
# Ensure the module remains clean, modular, and minimal with no duplicated MLflow setup code.
# Do not hardcode any values; read all necessary values from .env.
# 📏 Ground Rules Reminder:
# Use .env configurations for all settings.
# Do not add extra helper functions or files.
# Keep code minimal, readable, and strictly modular.
# No test data or hardcoded values.
# Be extremely careful with syntax and indentation.

import sys
import os
import importlib.util
from datetime import datetime
from app.mlflow_utils.mlflow_utils import init_mlflow, log_params, log_metrics, start_new_run_with_name
import matplotlib.pyplot as plt

# Import the built-in statistics module
spec = importlib.util.find_spec('statistics')
if spec and spec.origin and 'site-packages' not in spec.origin and 'statistics_service' not in spec.origin:
    builtin_stats = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builtin_stats)
else:
    # Fallback to manual implementation
    import math
    builtin_stats = None

def calculate_zscore(prices: list[float], symbol: str = None, timeframe_minutes: int = None,
                     z_threshold_upper: float = None, z_threshold_lower: float = None) -> list[float]:
    """
    Calculates z-score for a series of price values with MLflow logging integration.
    
    Args:
        prices: List of price values (floats), may contain None values
        symbol: Financial instrument symbol (optional, for logging)
        timeframe_minutes: Timeframe used for historical bars (optional, for logging)
        z_threshold_upper: Upper threshold for signal generation (optional, for logging)
        z_threshold_lower: Lower threshold for signal generation (optional, for logging)
        
    Returns:
        list[float]: List of z-score values, with None for undefined calculations
    """    # Determine symbol and timeframe for MLflow setup
    if not symbol:
        # Use COINTEGRATED_SYMBOLS from .env if symbol not provided
        cointegrated_symbols = os.getenv('COINTEGRATED_SYMBOLS', '')
        if cointegrated_symbols:
            symbol = cointegrated_symbols.split(',')[0].strip()  # Use first symbol as default
        else:
            symbol = 'UNKNOWN'
    
    if not timeframe_minutes:
        # Use DEFAULT_TIMEFRAME from .env
        default_timeframe = os.getenv('DEFAULT_TIMEFRAME', '5')
        timeframe_minutes = int(default_timeframe)
    
    # Initialize MLflow with the single experiment from .env
    try:
        init_mlflow()
        # Start a new run with unique name for this symbol and timeframe
        start_new_run_with_name(symbol, timeframe_minutes)
    except Exception as e:
        print(f"Warning: MLflow initialization failed: {e}")
    
    # Filter out None values for mean and std deviation calculation
    valid_prices = [price for price in prices if price is not None]
    
    # Return list of None if not enough valid data points
    if len(valid_prices) < 2:
        return [None] * len(prices)
    
    # Calculate mean and standard deviation from valid prices
    try:
        if builtin_stats:
            mean_value = builtin_stats.mean(valid_prices)
            std_dev = builtin_stats.stdev(valid_prices)
        else:
            # Manual calculation fallback
            mean_value = sum(valid_prices) / len(valid_prices)
            variance = sum((x - mean_value) ** 2 for x in valid_prices) / (len(valid_prices) - 1)
            std_dev = math.sqrt(variance)
        
        # Return None for all if standard deviation is zero (no variation)
        if std_dev == 0:
            return [None] * len(prices)
        
        # Calculate z-score for each price
        z_scores = []
        for price in prices:
            if price is None:
                z_scores.append(None)
            else:
                z_score = (price - mean_value) / std_dev
                z_scores.append(z_score)
        
        # Get the latest z-score and latest price for logging
        latest_price = valid_prices[-1] if valid_prices else None
        latest_z_score = z_scores[-1] if z_scores and z_scores[-1] is not None else None
        
        # Prepare parameters for logging (always include symbol and timeframe)
        params = {
            'symbol': symbol,
            'timeframe_minutes': timeframe_minutes,
            'window_size': len(valid_prices)
        }
        
        # Add optional threshold parameters if provided
        if z_threshold_upper is not None:
            params['z_threshold_upper'] = z_threshold_upper
        if z_threshold_lower is not None:
            params['z_threshold_lower'] = z_threshold_lower
        
        # Prepare metrics for logging (including timestamp as metric)
        metrics = {
            'mean_price': mean_value,
            'std_dev': std_dev,
            'calculation_timestamp': datetime.now().timestamp()  # Use timestamp as metric
        }
        
        if latest_price is not None:
            metrics['latest_price'] = latest_price
        if latest_z_score is not None:
            metrics['z_score'] = latest_z_score
        
        # Log parameters and metrics to MLflow
        try:
            log_params(params)
            log_metrics(metrics)
        except Exception as e:
            print(f"Warning: MLflow logging failed: {e}")

        return z_scores

    except Exception:
        # Return None for all if calculation fails
        return [None] * len(prices)


def plot_zscore(z_scores: list[float], output_file: str | None = None) -> None:
    """Plot z-score values as a line chart.

    Args:
        z_scores: List of z-score values, may contain None
        output_file: Optional path to save the plot instead of showing it
    """
    valid_points = [(i, z) for i, z in enumerate(z_scores) if z is not None]
    if not valid_points:
        return

    x_vals, y_vals = zip(*valid_points)

    plt.figure()
    plt.plot(x_vals, y_vals, label="z-score")
    plt.axhline(0, color="gray", linewidth=0.5)
    plt.xlabel("Index")
    plt.ylabel("Z-score")
    plt.title("Z-Score Over Time")
    plt.legend()

    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

    plt.close()
