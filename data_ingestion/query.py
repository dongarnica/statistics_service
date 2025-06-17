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
# Data Query Module
 
# Create a Python module named `query.py` inside the `data_ingestion` folder within the `statistics_service` project. This module will be responsible for querying historical market data from the remote PostgreSQL database hosted on Digital Ocean.
 
# 📁 File Location:
# statistics_service/data_ingestion/query.py
 
# 🧱 Requirements:
# - This module should only handle the logic for querying historical data.
# - It must depend on the existing connection logic from `connection.py`.
# - Do not handle any database credentials in this file—use the connection returned by `get_connection()` from `connection.py`.
# - Never overwrite or modify the `historical_bars` table.
# - Only read from the `historical_bars` table using safe, read-only SQL queries.
# - Create a function named `fetch_bars(symbol: str, timeframe: int, limit: int) -> list[tuple]` that:
#   - Connects using `get_connection()`
#   - Retrieves the latest `limit` rows for the given `symbol` and `timeframe` ordered by timestamp descending
#   - Returns results as a list of tuples
#   - Closes the database connection cleanly
# - Do not implement caching, transformation, or preprocessing here—just return raw data.
 
# 🧪 Example Usage (for reference only):
# from data_ingestion.query import fetch_bars
 
# rows = fetch_bars("SPY", 5, 100)
# for row in rows:
#     print(row)
 
# 🧼 Code Comments Requirement:
# - You must preserve the project guidelines comment block at the top of this file.
# - Never remove or modify the comment block that was inserted in Prompt #2. All modules must retain it as-is.
# - Place all implementation code below that comment block.
 
# ✅ Guidelines (Recap):
# - Only complete this module—do not create or modify others.
# - Use real market data only.
# - Never write to or overwrite the `historical_bars` table.
# - Read all configurations from the `.env` file indirectly through `connection.py`.
# - Do not create new helper files, scripts, or utilities.
# - Keep the implementation minimal, modular, and simple.
# - Write minimal but clear comments.
# - Avoid all indentation and syntax errors.
# - Do not add creative or extra functions.
# - Always follow the “simple and clean” philosophy.

from .connection import get_connection

def fetch_bars(symbol: str, timeframe: int, limit: int) -> list[tuple]:
    """
    Fetches historical market data from the historical_bars table.
    
    Args:
        symbol: Stock symbol (e.g., "SPY")
        timeframe: Timeframe in minutes
        limit: Number of records to retrieve
        
    Returns:
        list[tuple]: List of tuples containing historical bar data, ordered by timestamp desc
    """
    connection = None
    try:
        # Get database connection
        connection = get_connection()
        if not connection:
            return []
        
        # Create cursor for query execution
        cursor = connection.cursor()        # Safe read-only SQL query for historical_bars table
        query = """
            SELECT * FROM historical_bars 
            WHERE symbol = %s AND bar_size = %s 
            ORDER BY bar_date DESC, bar_time DESC 
            LIMIT %s
        """
        
        # Execute query with parameters to prevent SQL injection
        cursor.execute(query, (symbol, timeframe, limit))
        
        # Fetch all results
        rows = cursor.fetchall()
        
        # Close cursor
        cursor.close()
        
        return rows
        
    except Exception as e:
        print(f"Query execution failed: {e}")
        return []
        
    finally:
        # Always close connection cleanly
        if connection:
            connection.close()
