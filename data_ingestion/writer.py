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
# Prompt #6 – Statistics Writer Module
 
# Create a Python module named `writer.py` inside the `data_ingestion` folder of the `statistics_service` project. This module will handle writing the computed statistical results (such as z-score, correlation, or cointegration values) back to the PostgreSQL database.
 
# 📁 File Location:
# statistics_service/data_ingestion/writer.py
 
# 🧱 Requirements:
# - This module must depend on the existing connection logic from `connection.py`.
# - Do not hardcode any database credentials—use the `get_connection()` function from `connection.py`.
# - Do not modify or overwrite the `historical_bars` table.
# - Write statistical output to a new or designated results table (you may assume a `statistics_results` table exists).
# - Create a function named `write_statistic(symbol: str, timeframe: int, name: str, value: float, timestamp: datetime) -> None` that:
#   - Opens a connection
#   - Inserts one record with the provided inputs
#   - Closes the connection cleanly
# - Use parameterized queries to prevent SQL injection.
# - Handle all exceptions gracefully and fail silently or log minimal errors if a write fails.
 
# 🧪 Example Usage (for reference only):
# from data_ingestion.writer import write_statistic
# from datetime import datetime
 
# write_statistic("AAPL", 15, "zscore", -0.42, datetime.utcnow())
 
# 🧼 Code Comments Requirement:
# - You must preserve the project guidelines comment block at the top of this file.
# - Never remove or modify the comment block inserted during Prompt #2.
# - Place all implementation code below that comment block, keeping it untouched.
 
# ✅ Guidelines (Recap):
# - Only complete this module—do not modify or extend others.
# - Do not write to or affect the `historical_bars` table.
# - Always use real, production-grade logic—no test or sample data.
# - Never include multiple database connection strategies—use only `connection.py`.
# - Do not add any extra features like batching, retries, or logging unless explicitly instructed.
# - Keep the code modular, minimal, and clean.
# - Be extremely careful with syntax and indentation.
# - Write minimal but clear comments.
# - Follow the “simple and clean” rule strictly.

from datetime import datetime
from .connection import get_connection

def write_statistic(symbol: str, timeframe: int, name: str, value: float, timestamp: datetime) -> None:
    """
    Writes a computed statistical result to the statistics_results table.
    
    Args:
        symbol: Stock symbol (e.g., "AAPL")
        timeframe: Timeframe in minutes
        name: Name of the statistic (e.g., "zscore", "correlation")
        value: Computed statistical value
        timestamp: Timestamp when the statistic was calculated
    """
    connection = None
    try:
        # Get database connection
        connection = get_connection()
        if not connection:
            return
        
        # Create cursor for query execution
        cursor = connection.cursor()
        
        # Parameterized INSERT query for statistics_results table
        query = """
            INSERT INTO statistics_results (symbol, timeframe, name, value, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        # Execute insert with parameters to prevent SQL injection
        cursor.execute(query, (symbol, timeframe, name, value, timestamp))
        
        # Commit the transaction
        connection.commit()
        
        # Close cursor
        cursor.close()
        
    except Exception as e:
        # Handle write errors gracefully with minimal logging
        print(f"Write failed: {e}")
        
    finally:
        # Always close connection cleanly
        if connection:
            connection.close()
