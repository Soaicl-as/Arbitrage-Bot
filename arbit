import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText
import time

# Email credentials
SENDER_EMAIL = "social.marketing638@gmail.com"
SENDER_PASSWORD = "vojsif-bujxuw-jynTu6"
RECEIVER_EMAIL = "Ashishsharmaa2007@gmail.com"

# Function to send email notifications
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")

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
        "BetMGM": ("https://sports.on.betmgm.ca/en/sports/basketball-7", "div.option-indicator")  # ✅ BetMGM selector added
    }

    for site, (url, css_selector) in urls.items():
        if not css_selector:
            print(f"Skipping {site}: CSS selector missing.")
            continue
        
        odds = scrape_odds(url, css_selector)
        arbitrage, profit = calculate_arbitrage(odds)
        if arbitrage:
            subject = f"Arbitrage Opportunity Detected on {site}"
            body = f"Profitable arbitrage opportunity found on {site} with profit: {profit}\n\nBookmaker link: {url}"
            send_email(subject, body)

# Main execution
if __name__ == "__main__":
    try:
        check_sports()
    except Exception as e:
        error_message = f"Critical error: {str(e)}\n{traceback.format_exc()}"
        send_email("Arbitrage Bot Critical Failure", error_message)
