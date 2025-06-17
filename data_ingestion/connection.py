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
# Database Connection Module
 
# Create a Python module named `connection.py` inside the `data_ingestion` folder within the `statistics_service` project. This module should handle establishing a secure connection to a remote PostgreSQL database hosted on Digital Ocean.
 
# 📁 File Location:
# statistics_service/data_ingestion/connection.py
 
# 🧱 Requirements:
# - Read all PostgreSQL connection parameters from the `.env` file:
#   POSTGRES_DB_HOST
#   POSTGRES_DB_PORT
#   POSTGRES_DB_NAME
#   POSTGRES_DB_USER
#   POSTGRES_DB_PASSWORD
#   POSTGRES_DB_SSL_MODE
 
# - Use `psycopg2` as the PostgreSQL client library.
# - The module must expose a single function `get_connection()` that returns an open connection object.
# - Handle exceptions gracefully and return `None` if the connection fails.
# - Never overwrite or alter the `historical_bars` table in any way.
# - Do not add extra functionality such as query execution or schema inspection—this module is strictly for establishing the database connection.
# - Keep the implementation minimal, modular, and clean.
# - Add a clear comment block at the top of the file with the full project guidelines (see Prompt #2).
 
# 🧪 Example Usage (for reference only, not part of the module):
# from data_ingestion.connection import get_connection
 
# conn = get_connection()
# if conn:
#     print("Connection established")
# else:
#     print("Failed to connect")

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_connection():
    """
    Establishes a secure connection to the remote PostgreSQL database.
    
    Returns:
        psycopg2.connection: Database connection object if successful, None if failed
    """
    try:
        # Read connection parameters from environment variables
        connection_params = {
            'host': os.getenv('POSTGRES_DB_HOST'),
            'port': os.getenv('POSTGRES_DB_PORT'),
            'database': os.getenv('POSTGRES_DB_NAME'),
            'user': os.getenv('POSTGRES_DB_USER'),
            'password': os.getenv('POSTGRES_DB_PASSWORD'),
            'sslmode': os.getenv('POSTGRES_DB_SSL_MODE')
        }
        
        # Establish connection
        connection = psycopg2.connect(**connection_params)
        return connection
        
    except Exception as e:
        # Handle connection errors gracefully
        print(f"Database connection failed: {e}")
        return None

