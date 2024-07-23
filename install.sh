#!/bin/bash

# Ensure the user has sudo privileges
if [ "$(id -u)" != "0" ]; then
  echo "This script must be run as root or with sudo" 1>&2
  exit 1
fi

# Set the package name and version
PACKAGE_NAME="keylogger_project"

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "No requirements.txt file found. Skipping dependency installation."
fi

# Install the package
echo "Installing the package..."
pip install .


# Notify the user 
echo "Installation complete. You can now use the 'keylogger' command."