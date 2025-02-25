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

# Configure Selenium WebDriver
def create_driver():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"  # Set Chrome binary path
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up WebDriver using ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
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
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# Web scraping functions
def get_odds(driver, url, selector):
    driver.get(url)
    time.sleep(3)  # Adjust timing as necessary
    odds_elements = driver.find_elements(By.CSS_SELECTOR, selector)
    odds = [elem.text for elem in odds_elements if elem.text]
    return odds

# Scrape odds from Bet365, Stake, and BetMGM
def get_odds_from_bet365(driver):
    return get_odds(driver, "https://www.bet365.com/", "span.sac-ParticipantOddsOnly500__Odds")

def get_odds_from_stake(driver):
    return get_odds(driver, "https://www.stake.com/", "div.outcome-content.svelte-12qjp05")

def get_odds_from_betmgm(driver):
    return get_odds(driver, "https://www.betmgm.com/", "div.option-indicator")

# Function to check for arbitrage opportunities
def check_arbitrage(odds1, odds2, odds3):
    opportunities = []
    try:
        for o1 in odds1:
            for o2 in odds2:
                for o3 in odds3:
                    try:
                        # Convert to float before comparison
                        o1, o2, o3 = float(o1), float(o2), float(o3)

                        # Arbitrage condition (example logic, replace with real calculations)
                        if o1 < o2 and o1 < o3:
                            opportunities.append(f"Arbitrage opportunity: {o1} from Bet365, {o2} from Stake, {o3} from BetMGM.")

                    except ValueError:
                        continue  # Skip invalid odds

    except Exception as e:
        logging.error(f"Error in arbitrage calculation: {e}")

    if opportunities:
        send_email("Arbitrage Opportunity Found!", "\n".join(opportunities))
    else:
        logging.info("No arbitrage opportunity found.")

# Keep the bot active
def heartbeat():
    logging.info("Heartbeat - Bot is running.")
    time.sleep(60)  # Sleep for 1 minute

# Main function
def main():
    send_email("Arbitrage Bot is Running!", "The bot is now running and scraping odds.")
    
    driver = create_driver()

    while True:
        try:
            bet365_odds = get_odds_from_bet365(driver)
            stake_odds = get_odds_from_stake(driver)
            betmgm_odds = get_odds_from_betmgm(driver)

            check_arbitrage(bet365_odds, stake_odds, betmgm_odds)

            time.sleep(120)  # Wait 2 minutes
            heartbeat()

        except Exception as e:
            logging.error(f"Error occurred: {e}")
            send_email("Arbitrage Bot Error", f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()
