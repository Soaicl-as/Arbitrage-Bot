# main.py
import sys
from bot import start_bot  # Adjust this based on the actual function you use to run your bot

def main():
    try:
        print("Starting the Arbitrage Betting Bot...")
        start_bot()  # Call the function that starts your bot
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
