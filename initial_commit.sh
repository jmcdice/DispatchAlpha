#!/bin/bash

# This script performs the initial commit and push to the DispatchAlpha repository.

# --- Git Configuration ---
REMOTE_URL="git@github.com:jmcdice/DispatchAlpha.git"
COMMIT_MESSAGE="Initial commit: Phase 1 and AI Core Stub"
BRANCH_NAME="main"

# --- Execution ---
echo "Adding all files to git..."
git add .

echo "Creating the initial commit..."
git commit -m "$COMMIT_MESSAGE"

echo "Renaming the branch to '$BRANCH_NAME'..."
git branch -M $BRANCH_NAME

echo "Adding remote origin: $REMOTE_URL"
# Check if remote 'origin' already exists and remove it if it does
if git remote | grep -q "origin"; then
    git remote rm origin
fi
git remote add origin $REMOTE_URL

echo "Pushing the initial commit to GitHub..."
git push -u origin $BRANCH_NAME

echo ""
echo "✅ Done! Your project is now on GitHub."
echo "You can now clone it on your Raspberry Pi using: git clone $REMOTE_URL"