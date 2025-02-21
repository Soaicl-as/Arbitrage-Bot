import logging
import smtplib
import ssl
import time
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Gmail credentials
SENDER_EMAIL = "Social.marketing638@gmail.com"
SENDER_PASSWORD = "gpsv gcwc ejts jvrn"  # Replace with your App Password
RECEIVER_EMAIL = "Ashishsharmaa2007@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL connection port

# Flag to ensure the test email is sent only once
test_email_sent = False

def send_email(subject, body):
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()

        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send the email
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            logging.info(f"Email sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# Send test email only once
def send_test_email():
    global test_email_sent
    if not test_email_sent:
        send_email("Test Email", "This is a test email from your arbitrage bot.")
        test_email_sent = True

# Heartbeat function to ping Render every minute
def send_heartbeat():
    while True:
        try:
            logging.info("Sending heartbeat to prevent inactivity...")
            send_email("Heartbeat", "Bot is still running.")
            time.sleep(60)  # Wait for 1 minute
        except Exception as e:
            logging.error(f"Failed to send heartbeat: {e}")

# Arbitrage checking function
def start_arbitrage_check():
    while True:
        logging.info("Starting the arbitrage bot.")
        send_test_email()
        logging.info("Performing arbitrage check...")
        
        # Your arbitrage scraping logic goes here...
        # Simulate arbitrage check (replace with actual logic)
        arbitrage_found = False  # Replace with your actual check result

        if arbitrage_found:
            send_email("Arbitrage Opportunity Found!", "Details of the opportunity.")
        else:
            logging.info("Arbitrage check finished, no opportunities found.")
        
        # Sleep for 90 seconds before scraping again
        time.sleep(90)

# Start the heartbeat in a separate thread
heartbeat_thread = threading.Thread(target=send_heartbeat, daemon=True)
heartbeat_thread.start()

# Start the arbitrage bot
start_arbitrage_check()
