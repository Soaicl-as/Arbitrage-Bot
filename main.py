import logging
import smtplib
import ssl
import time
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Email configuration
SENDER_EMAIL = "Social.marketing638@gmail.com"
SENDER_PASSWORD = "gpsv gcwc ejts jvrn"  # Replace with your App Password
RECEIVER_EMAIL = "Ashishsharmaa2007@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL connection port

# Flag to ensure test email is sent only once
test_email_sent = False

# List of websites to scrape
WEBSITES = ["https://www.bet365.com", "https://www.stake.com", "https://www.betmgm.com"]

# Initialize the logger
logging.basicConfig(level=logging.INFO)

def send_email(subject, body):
    """Send email function."""
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

def send_test_email():
    """Send a test email when the bot first starts."""
    global test_email_sent
    if not test_email_sent:
        send_email("Arbitrage Bot - Test Email", "The arbitrage bot is working!")
        test_email_sent = True

def send_heartbeat():
    """Heartbeat function to ping Render every minute to prevent inactivity."""
    while True:
        try:
            logging.info("Sending heartbeat to prevent inactivity...")
            send_email("Heartbeat", "Bot is still running.")
            time.sleep(60)  # Wait for 1 minute
        except Exception as e:
            logging.error(f"Failed to send heartbeat: {e}")

def scrape_websites():
    """Scrape odds from the websites and check for arbitrage opportunities."""
    opportunities = []
    try:
        # Setup WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        for website in WEBSITES:
            logging.info(f"Scraping website: {website}")
            driver.get(website)
            time.sleep(3)  # Adjust this time if needed, to let the page load

            # Scrape odds - You need to adapt this logic for each website
            odds_elements = driver.find_elements(By.CLASS_NAME, 'odds')  # Example class name for odds
            odds = [element.text for element in odds_elements]
            logging.info(f"Odds scraped from {website}: {odds}")

            # Check for arbitrage opportunities (this is a simplified placeholder)
            if check_arbitrage(odds):
                opportunities.append(f"Arbitrage opportunity found on {website}. Odds: {odds}")

        driver.quit()
        return opportunities

    except Exception as e:
        logging.error(f"Error during scraping: {e}")
        send_email("Error in Arbitrage Bot", f"An error occurred during scraping: {e}")
        return []

def check_arbitrage(odds):
    """Check for arbitrage opportunities from scraped odds."""
    # Replace with actual arbitrage detection logic
    # For example: find if the combined odds from 3 websites offer a risk-free profit
    if len(odds) >= 3:  # Placeholder condition for arbitrage
        return True
    return False

def start_arbitrage_check():
    """Start the arbitrage check and scrape websites every 2 minutes."""
    while True:
        logging.info("Starting the arbitrage bot.")
        send_test_email()
        opportunities = scrape_websites()

        if opportunities:
            for opportunity in opportunities:
                send_email("Arbitrage Opportunity Found", opportunity)
        else:
            logging.info("No arbitrage opportunities found.")

        # Wait for 2 minutes before the next scrape
        time.sleep(120)

# Start the heartbeat in a separate thread to keep Render alive
heartbeat_thread = threading.Thread(target=send_heartbeat, daemon=True)
heartbeat_thread.start()

# Start the arbitrage bot
start_arbitrage_check()
