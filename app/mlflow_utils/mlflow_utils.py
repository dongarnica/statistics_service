# 📦 Folder Placement:
# app/mlflow/mlflow_utils.py
# 🧠 Prompt for Copilot:
# Create a new Python module named mlflow_utils.py inside the app/mlflow folder. This module should provide centralized MLflow functionality for the entire statistics service.
# Environment Configs: Read MLFLOW_TRACKING_URI and MLFLOW_EXPERIMENT_NAME from the .env file using the os module.
# Initialization Function: Implement a function init_mlflow() that sets the tracking URI and experiment name using MLflow's API.
# Logging Functions:
# log_params(params: dict) – log model or calculation parameters.
# log_metrics(metrics: dict) – log performance metrics.
# log_artifact(file_path: str) – log a single artifact file.
# log_artifacts(directory_path: str) – log all files in a directory.
# Each function should check if an MLflow run is active and start one if needed.
# Keep the module minimal, clean, and reusable across different statistical modules.
# Ensure there are no hardcoded values; rely fully on .env configurations.
# 📏 Ground Rules:
# Always use configurations from the .env file.
# Keep code modular and organized.
# Never overwrite the history_bars table.
# Don't create docker-compose files.
# Don't create Makefiles.
# Don't create any unnecessary files like e.g. .gitignore.
# Don't create helper scripts.
# Keep everything simple and clean.
# PostgreSQL is hosted remotely on Digital Ocean.
# Kafka is hosted remotely on a Digital Ocean droplet.
# Keep Dockerfile as simple as possible.
# Keep .devcontainer.json as simple as possible.
# Check for Kafka topics, consumer groups and create if they don't exist.
# Make sure data is real and not test data.
# Create detailed README file with ground rules.
# Don't be creative and add additional functions.
# Don't make any indentation errors.
# Be extremely careful with syntax errors.
# Write minimal but clear comments.

"""
MLflow utilities for centralized tracking and logging functionality.
Provides initialization and logging functions for the statistics service.
"""

import os
import mlflow
from datetime import datetime
from typing import Dict, Optional


def init_mlflow() -> None:
    """
    Initialize MLflow tracking URI and experiment name from environment variables.
    Sets up the MLflow environment for the statistics service.
    """
    tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
    experiment_name = os.getenv('MLFLOW_EXPERIMENT_NAME')
    
    if not tracking_uri:
        raise ValueError("MLFLOW_TRACKING_URI not found in environment variables")
    if not experiment_name:
        raise ValueError("MLFLOW_EXPERIMENT_NAME not found in environment variables")
    
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)


def _ensure_active_run() -> None:
    """
    Ensure an MLflow run is active. Start a new run if none is active.
    """
    if mlflow.active_run() is None:
        mlflow.start_run()


def log_params(params: Dict) -> None:
    """
    Log model or calculation parameters to MLflow.
    
    Args:
        params: Dictionary of parameters to log
    """
    _ensure_active_run()
    mlflow.log_params(params)


def log_metrics(metrics: Dict) -> None:
    """
    Log performance metrics to MLflow.
    
    Args:
        metrics: Dictionary of metrics to log
    """
    _ensure_active_run()
    mlflow.log_metrics(metrics)


def log_artifact(file_path: str) -> None:
    """
    Log a single artifact file to MLflow.
    
    Args:
        file_path: Path to the file to log as artifact
    """
    _ensure_active_run()
    mlflow.log_artifact(file_path)


def log_artifacts(directory_path: str) -> None:
    """
    Log all files in a directory as artifacts to MLflow.
    
    Args:
        directory_path: Path to the directory containing artifacts
    """
    _ensure_active_run()
    mlflow.log_artifacts(directory_path)


def start_new_run(run_name: str = None) -> None:
    """
    Start a new MLflow run with optional run name.
    
    Args:
        run_name: Optional name for the run
    """
    if mlflow.active_run() is not None:
        mlflow.end_run()
    mlflow.start_run(run_name=run_name)


def end_run() -> None:
    """
    End the current MLflow run if one is active.
    """
    if mlflow.active_run() is not None:
        mlflow.end_run()


def init_mlflow_with_experiment(symbol: str, timeframe_minutes: int) -> None:
    """
    Initialize MLflow with a unique experiment for each symbol and timeframe combination.
    
    Args:
        symbol: The financial instrument symbol
        timeframe_minutes: The timeframe in minutes
    """
    tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
    base_experiment_name = os.getenv('MLFLOW_EXPERIMENT_NAME', 'statistical-arbitrage-experiments')
    
    if not tracking_uri:
        raise ValueError("MLFLOW_TRACKING_URI not found in environment variables")
    
    # Create unique experiment name for each symbol and timeframe
    experiment_name = f"{base_experiment_name}_{symbol}_{timeframe_minutes}min"
    
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)


def start_new_run_with_name(symbol: str, timeframe_minutes: int) -> None:
    """
    Start a new MLflow run with a unique name based on symbol, timeframe, and timestamp.
    
    Args:
        symbol: The financial instrument symbol
        timeframe_minutes: The timeframe in minutes
    """
    if mlflow.active_run() is not None:
        mlflow.end_run()
    
    # Create unique run name with symbol, timeframe, and timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    run_name = f"{symbol}_{timeframe_minutes}min_{timestamp}"
    
    mlflow.start_run(run_name=run_name)
