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
# Prompt – Correlation Statistical Module
 
# Create a Python module named `correlation.py` inside the `statistics` folder of the `statistics_service` project. This module will compute the Pearson correlation coefficient between two time series of asset prices.
 
# 📁 File Location:
# statistics_service/statistics/correlation.py
 
# 🧱 Requirements:
# - Create a function named `calculate_correlation(series_a: list[float], series_b: list[float]) -> float | None`.
# - The function must:
#   - Accept two equal-length lists of float price values
#   - Ignore or clean `None` values from both series before computing correlation
#   - Return the Pearson correlation coefficient as a float
#   - Return `None` if input is invalid, lists are empty, or insufficient valid data exists
# - Use `scipy.stats.pearsonr` or `numpy.corrcoef`—any standard scientific implementation is acceptable
# - Do not handle data loading or saving—this module is for computation only
# - Do not include testing logic, CLI usage, or logging
# - Avoid any non-standard libraries or extra logic
 
# 🧪 Example Usage (for reference only):
# from stats.correlation import calculate_correlation
 
# score = calculate_correlation([100.1, 101.2, 102.3], [99.5, 100.4, 101.1])
# print(score)
 
# 🧼 Code Comments Requirement:
# - You must preserve the project guidelines comment block at the top of this file.
# - Never remove or modify the comment block inserted during Prompt #2.
# - Place all implementation code below that comment block, keeping it untouched.
 
# ✅ Guidelines (Recap):
# - Only implement this module—do not work on others.
# - Never affect or overwrite the `historical_bars` table.
# - Do not generate, fetch, or simulate data—use real inputs only.
# - Keep the function minimal, modular, and focused on correlation computation.
# - Be careful with syntax and indentation.
# - Write minimal but clear comments.
# - Do not add features beyond the requested functionality.
# - Follow a strict “simple and clean” code style.

from scipy.stats import pearsonr

def calculate_correlation(series_a: list[float], series_b: list[float]) -> float | None:
    """
    Calculates the Pearson correlation coefficient between two time series.
    
    Args:
        series_a: First time series of price values
        series_b: Second time series of price values
        
    Returns:
        float: Pearson correlation coefficient, or None if calculation fails
    """
    # Check if series have equal length
    if len(series_a) != len(series_b):
        return None
    
    # Clean data by removing pairs where either value is None
    clean_pairs = [(a, b) for a, b in zip(series_a, series_b) if a is not None and b is not None]
    
    # Check if enough data points remain after cleaning
    if len(clean_pairs) < 2:
        return None
    
    # Separate cleaned data back into two series
    clean_a = [pair[0] for pair in clean_pairs]
    clean_b = [pair[1] for pair in clean_pairs]
    
    try:
        # Calculate Pearson correlation coefficient
        correlation_coefficient, p_value = pearsonr(clean_a, clean_b)
        return correlation_coefficient
        
    except Exception:
        # Return None if correlation calculation fails
        return None
