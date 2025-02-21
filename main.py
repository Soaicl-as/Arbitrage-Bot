import time
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sqlite3
import requests
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)

# Email setup
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_email_password"
RECEIVER_EMAIL = "your_receiver_email@gmail.com"

# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# SQLite setup
conn = sqlite3.connect('arbitrage.db')
cursor = conn.cursor()

# Ensure the table exists
cursor.execute('''CREATE TABLE IF NOT EXISTS odds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bookmaker TEXT,
                    sport TEXT,
                    event TEXT,
                    odds REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

def send_email(subject, body):
    try:
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = RECEIVER_EMAIL
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

def heartbeat():
    # Just print a message for the heartbeat instead of sending an email
    print(f"Heartbeat: {datetime.now()} - The bot is still running")

def get_odds_from_bet365():
    # Example function to scrape Bet365 odds (simplified version)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://www.bet365.com")
    time.sleep(5)  # Wait for the page to load

    odds = []
    # Example extraction of data (adjust based on the actual website structure)
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, '.market .betButton')
        for element in elements:
            event = element.text
            odds.append(event)
    except Exception as e:
        logging.error(f"Error scraping Bet365: {e}")
    finally:
        driver.quit()
    
    return odds

def get_odds_from_stake():
    # Example function to scrape Stake odds (simplified version)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://www.stake.com")
    time.sleep(5)

    odds = []
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, '.market .betButton')
        for element in elements:
            event = element.text
            odds.append(event)
    except Exception as e:
        logging.error(f"Error scraping Stake: {e}")
    finally:
        driver.quit()

    return odds

def get_odds_from_betmgm():
    # Example function to scrape BetMGM odds (simplified version)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://www.betmgm.com")
    time.sleep(5)

    odds = []
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, '.market .betButton')
        for element in elements:
            event = element.text
            odds.append(event)
    except Exception as e:
        logging.error(f"Error scraping BetMGM: {e}")
    finally:
        driver.quit()

    return odds

def check_for_arbitrage(odds1, odds2, odds3):
    # Placeholder for arbitrage check logic (simplified)
    opportunities = []
    for i, odd1 in enumerate(odds1):
        for j, odd2 in enumerate(odds2):
            if abs(odd1 - odd2) > 0.5:  # Arbitrary condition for opportunity
                opportunities.append(f"Arbitrage opportunity: Bet365 vs Stake on event {i+1}")
        for j, odd3 in enumerate(odds3):
            if abs(odd1 - odd3) > 0.5:  # Arbitrary condition for opportunity
                opportunities.append(f"Arbitrage opportunity: Bet365 vs BetMGM on event {i+1}")
    return opportunities

def scrape_and_check():
    logging.info("Starting the arbitrage bot.")

    odds_bet365 = get_odds_from_bet365()
    odds_stake = get_odds_from_stake()
    odds_betmgm = get_odds_from_betmgm()

    opportunities = check_for_arbitrage(odds_bet365, odds_stake, odds_betmgm)

    if opportunities:
        body = "\n".join(opportunities)
        send_email("Arbitrage Opportunity Found!", body)
    else:
        logging.info("No arbitrage opportunities found.")

def main():
    # Send a test email when the bot first runs
    send_email("Bot is Running", "The arbitrage bot is working.")

    while True:
        scrape_and_check()
        heartbeat()  # Heartbeat to avoid inactivity detection
        time.sleep(120)  # Scrape every 2 minutes

if __name__ == "__main__":
    main()
