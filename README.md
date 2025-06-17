<!--
===========================================
Project Structure
- Assume you are in a folder named statistics_service
- Only complete one module at a time, do not start creating or working on other modules unless directed to
- Assume all operations start from the root directory
- Do not create files during setup
- Maintain a modular, organized code structure
- Don't create unnecessary files (.gitignore, Makefiles, helper scripts, etc.)
- Don't create docker-compose files

Data Handling
- Never overwrite the `historical_bars` table
- Use real data, not test data
- Always read configurations from the `.env` file

Infrastructure
- PostgreSQL is hosted on Digital Ocean (remote)
- Verify topics and consumer groups exist; create them if missing
- Never create multiple dev containers

Development Environment
- Keep Dockerfile minimal and functional
- Keep `.devcontainer.json` configuration simple
- Create only one dev container when needed

Documentation
- Create a detailed README with clear ground rules
- Include setup instructions and usage guidelines

Code Quality
- Write minimal but clear comments
- Avoid indentation errors
- Be extremely careful with syntax
- Don't add creative or additional functions beyond requirements
- Follow a "simple and clean" approach to all implementations
===========================================
-->

# Statistics Service

A bare-bones Python project for statistical analysis with PostgreSQL integration.

## Setup Instructions

1. **Prerequisites**
   - Docker Desktop installed and running
   - VS Code with the Dev Containers extension

2. **Getting Started**
   - Open this folder in VS Code
   - When prompted, click "Reopen in Container" or use Command Palette: `Dev Containers: Reopen in Container`
   - The dev container will build automatically using the provided Dockerfile

3. **Environment Configuration**
   - All configuration is stored in the `.env` file
   - Database connection details are pre-configured for Digital Ocean PostgreSQL
   - No manual configuration changes needed

4. **Development Workflow**
   - Work inside the dev container environment
   - All dependencies will be managed through `requirements.txt`
   - The container exposes port 8000 for the application

## Usage Guidelines

- Read all configurations from the `.env` file
- Use a modular and organized folder structure
- Complete only one module at a time
- Follow the ground rules strictly

## Ground Rules

⚠️ **CRITICAL REQUIREMENTS - MUST BE FOLLOWED:**

1. **Always use real data** - Never use test or mock data
2. **Never overwrite historical_bars** - This table is protected and must not be modified
3. **Read all configurations from .env** - No hardcoded values allowed
4. **Use a modular and organized folder structure** - Keep code clean and organized
5. **Only complete one module at a time** - Focus on single functionality before moving on
6. **Never add creative or extra functionality** - Stick to requirements only
7. **Never create multiple dev containers** - Use the single provided container
8. **Be careful with syntax and indentation** - Follow Python best practices
9. **Write minimal but clear comments** - Code should be self-documenting
10. **Keep everything simple and clean** - Avoid unnecessary complexity

## Development Status

🚧 **Project is ready for development**

Do not begin building any modules until specifically directed.

## Database Information

- **Host**: Digital Ocean PostgreSQL (configured in .env)
- **Protected Table**: `historical_bars` (read-only)
- **SSL**: Required connection mode
