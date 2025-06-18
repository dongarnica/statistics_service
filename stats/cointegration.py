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
# Cointegration Statistical Module
 
# Create a Python module named `cointegration.py` inside the `statistics` folder of the `statistics_service` project. This module will compute the cointegration score between two time series of asset prices.
 
# 📁 File Location:
# statistics_service/statistics/cointegration.py
 
# 🧱 Requirements:
# - Create a function named `calculate_cointegration(series_a: list[float], series_b: list[float]) -> float | None`.
# - The function must:
#   - Accept two equal-length lists of price values
#   - Handle `None` values gracefully (skip or clean the input before analysis)
#   - Return the cointegration test statistic (e.g., p-value from the Engle-Granger test)
#   - Return `None` if the input is invalid or not enough data is available
# - Use `statsmodels.tsa.stattools.coint` or equivalent standard scientific method.
# - Do not write any code for loading, saving, or transforming external data—this module must only perform computation.
# - Do not include CLI, test cases, or logging logic.
# - Avoid using non-standard libraries unless explicitly required.
 
# 🧪 Example Usage (for reference only):
# from stats.cointegration import calculate_cointegration
 
# p_value = calculate_cointegration([101.5, 102.3, 103.0], [99.8, 100.5, 101.2])
# print(p_value)
 
# 🧼 Code Comments Requirement:
# - You must preserve the project guidelines comment block at the top of this file.
# - Never remove or modify the comment block inserted during Prompt #2.
# - Place all implementation code below that comment block, keeping it untouched.
 
# ✅ Guidelines (Recap):
# - Only implement this module and nothing else.
# - Never write to or affect the `historical_bars` table.
# - Always use real input data; no mocks or stubs.
# - Do not invent or expand logic beyond calculating the cointegration score.
# - Be extremely careful with syntax and indentation.
# - Write minimal but clear inline comments.
# - Keep everything modular, simple, and clean.

from statsmodels.tsa.stattools import coint
import numpy as np

def calculate_cointegration(series_a: list[float], series_b: list[float]) -> float | None:
    """
    Calculates the cointegration p-value between two time series using the Engle-Granger test.
    
    Args:
        series_a: First time series of price values
        series_b: Second time series of price values
        
    Returns:
        float: P-value from the cointegration test, or None if calculation fails
    """
    # Check if series have equal length
    if len(series_a) != len(series_b):
        return None

    # Convert to numpy arrays and mask out None/NaN values
    arr_a = np.array(series_a, dtype=float)
    arr_b = np.array(series_b, dtype=float)
    mask = ~np.logical_or(np.isnan(arr_a), np.isnan(arr_b))
    clean_a = arr_a[mask]
    clean_b = arr_b[mask]

    # Check if enough data points remain after cleaning
    if clean_a.size < 2:
        return None
    
    try:
        # Perform Engle-Granger cointegration test
        test_stat, p_value, critical_values = coint(clean_a, clean_b)
        return float(p_value)
        
    except Exception:
        # Return None if cointegration test fails
        return None