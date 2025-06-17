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

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
