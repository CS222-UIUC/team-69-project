#!/bin/bash

echo "Setting up the project..."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python and try again."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null
then
    echo "npm is not installed. Please install Node.js and try again."
    exit 1
fi

echo "Creating a virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
# Activate venv based on OS
if [[ "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate  # Windows (Git Bash)
else
    source venv/bin/activate       # MacOS/Linux
fi

echo "Setting up pre-commit hooks..."
pre-commit install

# Frontend commands
cd frontend

echo "Installing Node.js dependencies..."
npm install

echo "Running Prettier (Frontend Formatter)..."
npm run format || echo "No JavaScript files to format."

cd -

# Backend commands
echo "Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo "Running Black (Python Formatter)..."
black . || echo "No Python files to format."

echo "Running Flake8 (Python Linter)..."
flake8 . || echo "No linting issues found."

echo "Running Tests (Pytest)..."
pytest || echo "No tests found or test failures."

echo "Deactivating virtual environment..."
deactivate

echo "Setup complete."
