from flask import Flask
import time
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from arbit import check_sports, send_email, send_heartbeat  # Updated import for heartbeat
from threading import Thread
from waitress import serve  # Production-ready server

app = Flask(__name__)

# Email configurations
SENDER_EMAIL = "Social.marketing638@gmail.com"
SENDER_PASSWORD = "qqgx lluj wqmr rhgz"
RECEIVER_EMAIL = "Ashishsharmaa2007@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to send a test email to confirm email setup
def send_test_email():
    subject = "Test Email"
    body = "This is a test email to confirm the bot is working."

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            logging.info("Test email sent successfully!")
    except Exception as e:
        logging.error(f"Failed to send test email: {e}")

# This route will confirm the server is up
@app.route("/")
def home():
    return "Arbitrage Bot is running!"

# Send an opportunity found email
def send_forever_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            logging.info("Opportunity email sent successfully!")
    except Exception as e:
        logging.error(f"Failed to send opportunity email: {e}")

# Main loop for the arbitrage bot
def run_arbitrage_bot():
    while True:
        try:
            logging.info("Starting the arbitrage check.")
            # Check sports for arbitrage opportunities
            opportunity_found = check_sports()

            if opportunity_found:
                # Send email if an opportunity is found
                send_forever_email("Arbitrage Opportunity Found", "An arbitrage opportunity has been detected!")
            
            # Sleep for 2 minutes (120 seconds) before checking again
            time.sleep(120)

        except Exception as e:
            logging.error(f"Error in arbitrage bot loop: {e}")

if __name__ == "__main__":
    # Send a test email on start-up to confirm the bot is functional
    send_test_email()

    # Start the arbitrage bot in the background
    bot_thread = Thread(target=run_arbitrage_bot, daemon=True)
    bot_thread.start()

    # Start heartbeat thread to keep the bot alive
    heartbeat_thread = Thread(target=send_heartbeat, daemon=True)
    heartbeat_thread.start()

    # Run the production-ready Waitress server
    logging.info("Starting the production server with Waitress...")
    serve(app, host="0.0.0.0", port=8000)
