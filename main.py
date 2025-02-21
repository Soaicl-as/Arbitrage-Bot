from flask import Flask
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from arbit import check_sports, send_email  # Assuming check_sports and send_email are in arbit.py

app = Flask(__name__)

# Email configurations
SENDER_EMAIL = "Social.marketing638@gmail.com"
SENDER_PASSWORD = "vojsif-bujxuw-jynTu6"
RECEIVER_EMAIL = "Ashishsharmaa2007@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

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
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
            print("Test email sent successfully!")
    except Exception as e:
        print(f"Failed to send test email: {e}")

# This route will confirm the server is up
@app.route("/")
def home():
    return "Arbitrage Bot is running!"

# Send a forever opportunity found email (this is just an example)
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
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
            print("Opportunity email sent successfully!")
    except Exception as e:
        print(f"Failed to send opportunity email: {e}")

# Main loop for the arbitrage bot
def run_arbitrage_bot():
    while True:
        # Check sports for arbitrage opportunities
        opportunity_found = check_sports()

        if opportunity_found:
            # Send email if an opportunity is found
            send_forever_email("Arbitrage Opportunity Found", "An arbitrage opportunity has been detected!")
        
        # Sleep for a while before checking again
        time.sleep(30)

if __name__ == "__main__":
    # Send a test email on start-up to confirm the bot is functional
    send_test_email()

    # Start the arbitrage bot in the background
    # Run the Flask app to expose a port (default is 5000)
    from threading import Thread
    bot_thread = Thread(target=run_arbitrage_bot)
    bot_thread.start()

    # Run the Flask app on port 8000 (to be detected by Render)
    app.run(host="0.0.0.0", port=8000)
