import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText
import time
import logging

# Email configurations
SENDER_EMAIL = "Social.marketing638@gmail.com"
SENDER_PASSWORD = "qqgx lluj wqmr rhgz"
RECEIVER_EMAIL = "Ashishsharmaa2007@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Heartbeat function to keep Render from marking the bot as inactive
def send_heartbeat():
    while True:
        logging.info("Sending heartbeat to prevent inactivity.")
        time.sleep(60)  # Send heartbeat every minute

# Function to send email notifications
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            logging.info(f"Email sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# Function to scrape odds with error handling
def scrape_odds(url, css_selector):
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Wait for the page to fully load
        time.sleep(5)  

        # Extract odds using the given CSS selector
        odds_elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
        odds = [e.text for e in odds_elements if e.text.strip()]

        driver.quit()
        return odds
    except Exception as e:
        error_message = f"Error scraping {url}: {str(e)}\n{traceback.format_exc()}"
        send_email("Arbitrage Bot Error", error_message)
        return []

# Function to calculate arbitrage
def calculate_arbitrage(odds):
    try:
        if len(odds) < 2:
            return False, None
        profit = 1.0 / float(odds[0]) + 1.0 / float(odds[1])
        return profit < 1, profit
    except Exception as e:
        error_message = f"Error calculating arbitrage: {str(e)}\n{traceback.format_exc()}"
        send_email("Arbitrage Bot Error", error_message)
        return False, None

# Function to check sports odds for arbitrage
def check_sports():
    urls = {
        "Bet365": ("https://www.on.bet365.ca", "span.sac-ParticipantOddsOnly500__Odds"),  # ✅ Bet365 selector added
        "Stake": ("https://stake.com/sports/basketball", "div.outcome-content.svelte-12qjp05"),  # ✅ Stake selector added
        "BetMGM": ("https://sports.on.betmgm.ca/en/sports/basketball-7", "div.option-indicator")  # ✅ BetMG...
