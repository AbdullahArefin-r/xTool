#!/bin/bash

# Colors for output
GREEN='\033[1;32m'
BLUE='\033[1;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}[*] Initializing X-TERMUX PRO TOOLKIT environment...${NC}"

# Check if Python is installed, install if not
if ! command -v python &> /dev/null; then
    echo -e "${BLUE}[*] Python not found. Installing Python...${NC}"
    pkg update -y && pkg upgrade -y
    pkg install python -y
fi

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo -e "${BLUE}[*] Git not found. Installing Git...${NC}"
    pkg install git -y
fi

# Install required Python packages silently
echo -e "${GREEN}[+] Checking and installing Python dependencies...${NC}"
pip install -r requirements.txt -q

# Clear screen and launch the toolkit
clear
python main.py
