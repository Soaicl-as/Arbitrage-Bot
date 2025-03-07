#!/bin/bash

# Exit immediately if any command fails
set -e

# Update package list
echo "Updating package list..."
apt-get update

# Install Google Chrome
echo "Installing Google Chrome..."
wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > chrome.deb
apt-get install -y ./chrome.deb
rm -f chrome.deb  # Clean up

# Install ChromeDriver (matching the installed Chrome version)
echo "Installing ChromeDriver..."
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1)
CHROMEDRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION)
wget -qO- https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip > chromedriver.zip
unzip chromedriver.zip -d /usr/local/bin/
rm -f chromedriver.zip  # Clean up
chmod +x /usr/local/bin/chromedriver

# Install dependencies for Chrome and Selenium
echo "Installing dependencies..."
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
    wget \
    unzip

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install Selenium explicitly
echo "Installing Selenium..."
pip install selenium==4.29.0

# Install the rest of the requirements from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing requirements from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping..."
fi

echo "Build completed successfully!"
