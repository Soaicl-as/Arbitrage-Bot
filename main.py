import logging
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)

# Your Gmail credentials
SENDER_EMAIL = "Social.marketing638@gmail.com"
SENDER_PASSWORD = "gpsv gcwc ejts jvrn"  # Replace with your App Password
RECEIVER_EMAIL = "Ashishsharmaa2007@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL connection port

def send_email(subject, body):
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()

        # Set up the email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send the email using SMTP over SSL
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            logging.info(f"Email sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# Main execution block
if __name__ == "__main__":
    logging.info("Starting the arbitrage bot.")
    
    # Example of sending a test email, can be replaced with real bot logic
    send_email("Test Email", "This is a test email sent from the Arbitrage Bot.")
    
    logging.info("Arbitrage check finished, no opportunities found.")
    
    # Add any background tasks here, e.g., arbitrage check, heartbeat, etc.
    # For example:
    # while True:
    #     check_arbitrage()
    #     time.sleep(60)  # Delay between checks
