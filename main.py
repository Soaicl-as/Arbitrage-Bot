import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send an email
def send_email(subject, body):
    sender_email = os.getenv("EMAIL_USER", "Social.marketing638@gmail.com")  # Use environment variables or hardcode temporarily
    receiver_email = "Ashishsharmaa2007@gmail.com"
    password = os.getenv("EMAIL_PASSWORD", "vojsif-bujxuw-jynTu6")  # Use environment variables or hardcode temporarily

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email sent successfully: {subject}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to simulate an arbitrage opportunity detection
def check_for_opportunity():
    # Simulate an opportunity being found (This should be your actual opportunity detection code)
    # This function should return `True` if an opportunity is found, or `False` otherwise.
    return True  # For testing purposes, we'll assume an opportunity is always found.

# Main function to run the bot
def main():
    # Send one-time test email
    send_email("Test Email - Arbitrage Bot", "This is a test email to confirm that the email functionality is working.")

    # Simulate bot running and checking for opportunities continuously
    while True:
        if check_for_opportunity():
            # If an opportunity is found, send an email
            send_email(
                "Arbitrage Opportunity Found!",
                "An arbitrage opportunity has been found! Please check your betting sites for more details."
            )

        # Wait for a while before checking again (e.g., every 10 minutes)
        time.sleep(600)  # 600 seconds = 10 minutes (adjust as needed)

# Run the main function
if __name__ == "__main__":
    main()
