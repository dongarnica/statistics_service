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
# Prompt #7 – Configuration Loader Module
 
# Create a Python module named `settings.py` inside the `config` folder of the `statistics_service` project. This module will be responsible for loading environment variables from the `.env` file and making them accessible throughout the application.
 
# 📁 File Location:
# statistics_service/config/settings.py
 
# 🧱 Requirements:
# - Use the `os` and `dotenv` libraries to load and expose configuration values.
# - Automatically load the `.env` file from the root directory.
# - Define named constants for the following environment variables:
#   POSTGRES_DB_HOST
#   POSTGRES_DB_PORT
#   POSTGRES_DB_NAME
#   POSTGRES_DB_USER
#   POSTGRES_DB_PASSWORD
#   POSTGRES_DB_SSL_MODE
#   STATS_ENABLED
#   DEFAULT_TIMEFRAME
# - Convert values to appropriate types (e.g., integers for ports, lists for comma-separated strings).
# - Raise a clear error if any required environment variable is missing.
# - Do not hardcode any fallback values—assume all required variables are defined in `.env`.
# - Do not add logic unrelated to loading configuration.
 
# 🧪 Example Usage (for reference only):
# from config.settings import POSTGRES_DB_HOST, DEFAULT_TIMEFRAME
 
# print(POSTGRES_DB_HOST)
# print(DEFAULT_TIMEFRAME)
 
# 🧼 Code Comments Requirement:
# - You must preserve the project guidelines comment block at the top of this file.
# - Never remove or modify the comment block inserted during Prompt #2.
# - Place all implementation code below that comment block, keeping it untouched.
 
# ✅ Guidelines (Recap):
# - Only work on this module—do not create or change others.
# - Always read configuration values from the `.env` file.
# - Do not inject default logic, transformations, or processing beyond what’s explicitly requested.
# - Avoid unnecessary imports or complexity.
# - Be extremely careful with syntax and indentation.
# - Keep the code clean, modular, and minimal.
# - Write minimal but clear inline comments if needed.
# - Follow the "simple and clean" principle strictly.

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def _get_required_env(key: str) -> str:
    """Helper function to get required environment variable or raise error."""
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value

# PostgreSQL database configuration
POSTGRES_DB_HOST = _get_required_env('POSTGRES_DB_HOST')
POSTGRES_DB_PORT = int(_get_required_env('POSTGRES_DB_PORT'))
POSTGRES_DB_NAME = _get_required_env('POSTGRES_DB_NAME')
POSTGRES_DB_USER = _get_required_env('POSTGRES_DB_USER')
POSTGRES_DB_PASSWORD = _get_required_env('POSTGRES_DB_PASSWORD')
POSTGRES_DB_SSL_MODE = _get_required_env('POSTGRES_DB_SSL_MODE')

# Statistics configuration
STATS_ENABLED = _get_required_env('STATS_ENABLED').split(',')
DEFAULT_TIMEFRAME = int(_get_required_env('DEFAULT_TIMEFRAME'))
COINTEGRATED_SYMBOLS = _get_required_env('COINTEGRATED_SYMBOLS').split(',')
