#!/bin/bash

# Exit immediately if any command fails
set -e

# Update package list
echo "Updating package list..."
apt-get update

# Install Google Chrome
echo "Installing Google Chrome..."
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Get Chrome version and install matching ChromeDriver
echo "Installing ChromeDriver..."
CHROME_VERSION=$(google-chrome --version | cut -d ' ' -f 3 | cut -d '.' -f 1)
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
wget -q -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip -q /tmp/chromedriver.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
rm /tmp/chromedriver.zip

# Install additional dependencies
echo "Installing dependencies..."
apt-get install -y \
    libxss1 \
    libgbm1 \
    libasound2 \
    libgtk-3-0 \
    libx11-xcb1 \
    xdg-utils \
    lsb-release \
    fonts-liberation \
    libappindicator3-1 \
    libnspr4 \
    libnss3 \
    xvfb

# Setup Xvfb for headless browser
echo "Setting up Xvfb..."
Xvfb :99 -screen 0 1280x1024x24 > /dev/null 2>&1 &
echo "export DISPLAY=:99" >> ~/.bashrc

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip wheel setuptools

# Install Python requirements
echo "Installing Python requirements..."
pip install -r requirements.txt

# Make start.sh executable
echo "Making start.sh executable..."
chmod +x start.sh

echo "Build completed successfully!"
