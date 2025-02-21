import logging
import time
from email_utils import send_email  # Import the email-sending function from email_utils.py

def run_arbitrage_check():
    try:
        # Start scraping for arbitrage opportunities
        logging.info("Starting the arbitrage check.")

        # Your scraping logic (this is a placeholder, you should insert your scraping code here)
        found_opportunity = False  # You would replace this with the actual logic

        if found_opportunity:
            logging.info("Arbitrage opportunity found! Sending email.")
            send_email(subject="Arbitrage Opportunity Found", body="Details of the opportunity...")

        else:
            logging.warning("No arbitrage opportunity found.")

    except Exception as e:
        logging.error(f"Error during arbitrage check: {e}")
        send_email(subject="Error during arbitrage check", body=f"An error occurred: {e}")

def send_heartbeat():
    logging.info("Sending heartbeat to prevent inactivity.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Send the test email only once at the first run
    send_email(subject="Test Email", body="This is a test email to ensure everything is working.")

    # Main loop for scraping
    while True:
        run_arbitrage_check()
        send_heartbeat()
        time.sleep(60)  # Sleep for a minute before checking again
