#!/bin/bash

# Exit on error
set -e

echo "Installing Cursor Note Automation..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade pip
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p notes logs

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "OPENAI_API_KEY=" > .env
    echo "ANTHROPIC_API_KEY=" >> .env
fi

# Set up configuration
if [ ! -f "config/config.yaml" ]; then
    echo "Setting up configuration..."
    cp config/config.yaml.example config/config.yaml
fi

echo "Installation complete!"
echo "Please edit .env and config/config.yaml with your settings." 