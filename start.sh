#!/bin/bash

# Ensure the script is executable
if [ ! -x "$0" ]; then
    echo "Making start.sh executable..."
    chmod +x "$0"
    exec "$0" "$@"
fi

# Redirect output to a log file
exec > >(tee -a arbitrage_bot.log) 2>&1

# Run the bot using Poetry
echo "Starting arbitrage bot..."
poetry run python main.py

# If the bot crashes, log the error and restart
while true; do
    echo "Bot crashed. Restarting in 10 seconds..."
    sleep 10
    poetry run python main.py
done
