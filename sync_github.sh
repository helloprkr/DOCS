#!/bin/bash

# Define variables
PROJECT_DIR="/Users/maximvs/Library/Mobile Documents/com~apple~CloudDocs/00X_000_JORDAN-PARKER-PLANS 📑"
REMOTE_REPO="https://github.com/helloprkr/DOCS.git"
TEMP_DIR="/tmp/DOCS"

# Create backup
BACKUP_DIR="${PROJECT_DIR}_backup_$(date +%Y%m%d%H%M%S)"
echo "Creating backup at $BACKUP_DIR..."
cp -r "$PROJECT_DIR" "$BACKUP_DIR"

# Initialize Git if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
fi

# Configure Git to handle spaces in filenames
git config core.quotepath false

# Add remote if it doesn't exist
if ! git remote | grep -q "^DOCS$"; then
    echo "Adding DOCS remote..."
    git remote add DOCS $REMOTE_REPO
fi

# Fetch latest changes
echo "Fetching from DOCS repository..."
git fetch DOCS

# Add all files to staging
echo "Adding files to staging..."
git add .

# Create initial commit if needed
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
    echo "Creating initial commit..."
    git commit -m "Initial commit"
fi

# Merge with remote repository
echo "Merging with DOCS repository..."
git merge DOCS/main --allow-unrelated-histories

echo "Script completed. Please check for any merge conflicts."
echo "To resolve conflicts:"
echo "1. Open conflicted files and resolve conflicts"
echo "2. git add <resolved-files>"
echo "3. git commit -m 'Resolved merge conflicts'" 