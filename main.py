import logging
from arbit import check_sports, send_email, send_heartbeat, send_test_email
import time
import sys

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Send test email only once (skip after first run)
def send_initial_test_email():
    # Check if this is the first run and send the test email
    try:
        with open("first_run.txt", "r") as f:
            first_run = f.read()
    except FileNotFoundError:
        first_run = "True"

    if first_run == "True":
        send_test_email()
        with open("first_run.txt", "w") as f:
            f.write("False")
            logging.info("Test email sent successfully!")
    else:
        logging.info("Test email has already been sent.")

def main():
    # Send test email on the first run
    send_initial_test_email()

    # Start heartbeat thread
    import threading
    heartbeat_thread = threading.Thread(target=send_heartbeat)
    heartbeat_thread.daemon = True
    heartbeat_thread.start()

    # Start the arbitrage check in a loop
    while True:
        logging.info("Starting the arbitrage check.")
        check_sports()
        time.sleep(60)  # Wait a minute before checking again

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        send_email("Arbitrage Bot Error", f"An error occurred: {e}")
        sys.exit(1)
