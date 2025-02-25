#!/bin/bash

# Update package list
apt-get update

# Install Google Chrome if required
wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > chrome.deb
apt-get install -y ./chrome.deb

# Install dependencies for Chrome and Selenium (for proper functioning)
apt-get install -y \
    libxss1 \
    libappindicator3-1 \
    libindicator7 \
    fonts-liberation \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxrandr2 \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libnspr4 \
    libxtst6 \
    lsb-release \
    wget

# Upgrade pip to the latest version
pip install --upgrade pip

# Check if Selenium is installed
pip show selenium

# Install selenium explicitly to avoid any issues
pip install selenium==4.29.0

# Install the rest of the requirements from requirements.txt
pip install -r requirements.txt
