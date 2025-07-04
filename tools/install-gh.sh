#!/bin/bash
#
# ===================================================================
# GITHUB CLI INSTALLATION SCRIPT
# ===================================================================
#
# Description:
#   This script installs the GitHub CLI (gh) on Debian/Ubuntu systems
#   using the official GitHub package repository. It handles the complete
#   installation process including repository setup and GPG key management.
#
# Author: Lake Holidays Challenge Team
# Version: 1.0
# Last Modified: $(date +%Y-%m-%d)
#
# Prerequisites:
#   - Debian/Ubuntu-based Linux distribution
#   - sudo privileges
#   - Internet connection
#
# Usage:
#   ./install-gh.sh
#
# What this script does:
#   1. Ensures wget is installed (installs if missing)
#   2. Creates APT keyring directory with proper permissions
#   3. Downloads and installs GitHub CLI GPG signing key
#   4. Adds GitHub CLI repository to APT sources
#   5. Updates package lists
#   6. Installs GitHub CLI package
#
# Post-installation:
#   After installation, authenticate with: gh auth login
#
# Supported Systems:
#   - Ubuntu 18.04+
#   - Debian 9+
#   - Other Debian-based distributions
#
# Exit Codes:
#   0 - Success
#   1 - Error during installation
#
# Official Documentation:
#   https://cli.github.com/manual/installation
#
# ===================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Main installation process
log "Starting GitHub CLI installation..."

# Ensure wget is installed
(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \

# Create APT keyring directory
sudo mkdir -p -m 755 /etc/apt/keyrings \

# Download and install GitHub CLI GPG signing key
out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
	&& cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
	&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \

# Add GitHub CLI repository to APT sources
sudo mkdir -p -m 755 /etc/apt/sources.list.d \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \

# Update package lists
sudo apt update \

# Install GitHub CLI package
sudo apt install gh -y

success "GitHub CLI installation completed!"
log "To authenticate, run: gh auth login"
log "For help, run: gh --help"