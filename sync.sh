#!/bin/bash

# Navigate to project directory (using quotes to handle spaces and emojis)
cd "/Users/maximvs/Library/Mobile Documents/com~apple~CloudDocs/00X_000_JORDAN-PARKER-PLANS 📑" || {
    echo "Failed to change directory"
    exit 1
}

# Create backup with proper date format
BACKUP_DIR="${PWD}_backup_$(date +%Y%m%d%H%M%S)"
echo "Creating backup at $BACKUP_DIR..."
cp -r "$PWD" "$BACKUP_DIR" || {
    echo "Backup failed"
    exit 1
}

# Initialize and configure git
git init
git config core.quotepath false
git config core.precomposeunicode true

# Remove existing DOCS remote if it exists
git remote remove DOCS 2>/dev/null

# Add remote
git remote add DOCS "https://github.com/helloprkr/DOCS.git"

# Stage and commit changes
git add .
git commit -m "Initial commit: Syncing project structure" || {
    echo "Commit failed"
    exit 1
}

# Fetch and merge
git fetch DOCS
git merge DOCS/main --allow-unrelated-histories

echo "Sync completed. Check for merge conflicts."