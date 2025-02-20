# main.py
import sys
from arbit import start_bot  # Import the start_bot function from arbit.py

def main():
    try:
        print("Starting the Arbitrage Betting Bot...")
        start_bot()  # This is where you call the function that starts your bot
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()  # Ensure main() gets called when running this file
