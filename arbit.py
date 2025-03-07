import traceback
import os
import time
import logging
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
import schedule

# Load environment variables for sensitive data
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "Social.marketing638@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "qqgx lluj wqmr rhgz")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "Ashishsharmaa2007@gmail.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("arbitrage_bot.log"), logging.StreamHandler()],
)

# Global variable to track if the test email has been sent
test_email_sent = False

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
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
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
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Wait for the page to fully load (increased time)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )

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
        "BetMGM": ("https://sports.on.betmgm.ca/en/sports/basketball-7", "div.option-indicator")  # ✅ BetMGM selector added
    }

    for website, (url, selector) in urls.items():
        logging.info(f"Scraping {website} for arbitrage opportunities...")
        odds = scrape_odds(url, selector)
        if odds:
            is_arbitrage, profit = calculate_arbitrage(odds)
            if is_arbitrage:
                logging.info(f"Arbitrage opportunity found on {website}: {odds} with profit {profit:.2%}")
                send_email(f"Arbitrage Opportunity Found on {website}", f"Found arbitrage with {odds} and profit {profit:.2%}")
        else:
            logging.warning(f"No odds found on {website}")
        time.sleep(5)  # Added a small delay between requests

# Function to test if email is working properly (will only send once)
def send_test_email():
    global test_email_sent
    if not test_email_sent:
        send_email("Test Email", "This is a test email to ensure that the email functionality works.")
        test_email_sent = True

# Main function to run the bot
def main():
    # Start heartbeat in a separate thread
    heartbeat_thread = threading.Thread(target=send_heartbeat, daemon=True)
    heartbeat_thread.start()

    # Send a test email on startup
    send_test_email()

    # Schedule the sports check to run every minute
    schedule.every(1).minutes.do(check_sports)

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
