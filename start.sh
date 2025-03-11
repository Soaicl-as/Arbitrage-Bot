#!/bin/bash

# Create logs directory if it doesn't exist
mkdir -p logs

# Start Xvfb for headless browsing
export DISPLAY=:99
Xvfb :99 -screen 0 1280x1024x24 &
XVFB_PID=$!

echo "Starting Xvfb with PID: $XVFB_PID"

# Function to clean up resources when script exits
cleanup() {
    echo "Cleaning up resources..."
    if [ -n "$XVFB_PID" ]; then
        kill $XVFB_PID
    fi
    exit 0
}

# Set up trap to call cleanup function on exit
trap cleanup SIGINT SIGTERM

# Redirect stdout and stderr to log file with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="logs/arbitrage_bot_${TIMESTAMP}.log"

echo "Starting arbitrage bot, logging to $LOG_FILE"
echo "========== Bot Started at $(date) ==========" >> $LOG_FILE

# Run the bot with proper error handling
python main.py 2>&1 | tee -a $LOG_FILE

# If the bot crashes, restart with exponential backoff
RETRY_DELAY=10
MAX_RETRY_DELAY=3600  # 1 hour max delay
while true; do
    echo "Bot exited. Restarting in $RETRY_DELAY seconds..." | tee -a $LOG_FILE
    sleep $RETRY_DELAY
    
    echo "========== Restarting Bot at $(date) ==========" | tee -a $LOG_FILE
    python main.py 2>&1 | tee -a $LOG_FILE
    
    # Increase delay for next failure (exponential backoff)
    RETRY_DELAY=$((RETRY_DELAY * 2))
    if [ $RETRY_DELAY -gt $MAX_RETRY_DELAY ]; then
        RETRY_DELAY=$MAX_RETRY_DELAY
    fi
done
