import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Set up email credentials
SENDER_EMAIL = "social.marketing638@gmail.com"
SENDER_PASSWORD = "sbhb wscc dbua qsho"  # App password for Gmail
RECEIVER_EMAIL = "Ashishsharmaa2007@gmail.com"

# Web scraping setup - configure Selenium options for headless browsing
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Driver setup using webdriver_manager to avoid version issues
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Function to send email notifications
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# Scraping odds from Bet365, Stake, BetMGM using provided selectors
def get_odds_from_bet365(driver):
    driver.get("https://www.bet365.com/")
    time.sleep(3)  # Adjust timing as necessary
    
    # Use the provided selector to extract odds from Bet365
    odds_elements = driver.find_elements(By.CSS_SELECTOR, "span.sac-ParticipantOddsOnly500__Odds")
    odds = [elem.text for elem in odds_elements]
    logging.info(f"Scraped odds from Bet365: {odds}")
    return odds

def get_odds_from_stake(driver):
    driver.get("https://www.stake.com/")
    time.sleep(3)  # Adjust timing as necessary
    
    # Use the provided selector to extract odds from Stake
    odds_elements = driver.find_elements(By.CSS_SELECTOR, "div.outcome-content.svelte-12qjp05")
    odds = [elem.text for elem in odds_elements]
    logging.info(f"Scraped odds from Stake: {odds}")
    return odds

def get_odds_from_betmgm(driver):
    driver.get("https://www.betmgm.com/")
    time.sleep(3)  # Adjust timing as necessary
    
    # Use the provided selector to extract odds from BetMGM
    odds_elements = driver.find_elements(By.CSS_SELECTOR, "div.option-indicator")
    odds = [elem.text for elem in odds_elements]
    logging.info(f"Scraped odds from BetMGM: {odds}")
    return odds

# Function to check for arbitrage opportunities
def check_arbitrage(odds1, odds2, odds3):
    # Placeholder logic for arbitrage check, should be replaced with real calculations
    # Assuming odds1, odds2, and odds3 are lists of odds from the 3 bookmakers
    # This is a basic example of comparing odds
    opportunities = []
    for o1 in odds1:
        for o2 in odds2:
            for o3 in odds3:
                # Arbitrage condition - simple example
                if (o1 < o2 and o1 < o3):
                    opportunities.append(f"Arbitrage opportunity: {o1} from Bet365, {o2} from Stake, {o3} from BetMGM.")
    if opportunities:
        send_email("Arbitrage Opportunity Found!", "\n".join(opportunities))
    else:
        logging.info("No arbitrage opportunity found.")

# Heartbeat function to prevent Render from labeling the bot as inactive
def heartbeat():
    logging.info("Heartbeat - Bot is running.")
    time.sleep(60)  # Sleep for 1 minute before next ping

# Main function to scrape the odds and check for arbitrage
def main():
    # Send a test email the first time the bot runs
    send_email("Arbitrage Bot is Running!", "The bot is now running and scraping odds.")

    # Initialize the Selenium WebDriver
    driver = create_driver()

    while True:
        try:
            # Scrape odds from the 3 websites
            bet365_odds = get_odds_from_bet365(driver)
            stake_odds = get_odds_from_stake(driver)
            betmgm_odds = get_odds_from_betmgm(driver)

            # Check for arbitrage opportunities
            check_arbitrage(bet365_odds, stake_odds, betmgm_odds)

            # Wait for 2 minutes before scraping again
            time.sleep(120)
            
            # Send heartbeat every minute to keep the bot active
            heartbeat()

        except Exception as e:
            logging.error(f"Error occurred: {e}")
            send_email("Arbitrage Bot Error", f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()
