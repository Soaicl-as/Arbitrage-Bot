import logging
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
