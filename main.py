import os
import time
import logging
import traceback
import threading
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

# Load environment variables for sensitive data
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "social.marketing638@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "sbhb wscc dbua qsho")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "Ashishsharmaa2007@gmail.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
HEARTBEAT_INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", 180))  # 3 minutes
SCRAPE_INTERVAL = int(os.getenv("SCRAPE_INTERVAL", 120))  # 2 minutes

# Setup logging with rotation
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("arbitrage_bot.log", maxBytes=5*1024*1024, backupCount=3),
        logging.StreamHandler()
    ],
)
logger = logging.getLogger(__name__)

# Track if the startup email has been sent
startup_email_sent = False

# Betting sites configuration with detailed selectors and wait times
BETTING_SITES = {
    "Bet365": {
        "url": "https://www.on.bet365.ca/en/sports/",
        "market_selector": "div.srb-EventContainer",
        "event_selector": "div.srb-ParticipantFixtureDetails_BookCloses",
        "odds_selector": "span.sac-ParticipantOddsOnly500__Odds",
        "timeout": 10,
        "wait_time": 5
    },
    "Stake": {
        "url": "https://stake.com/sports/all/canada",
        "market_selector": "div.market-group",
        "event_selector": "div.event-data",
        "odds_selector": "div.outcome-content",
        "timeout": 10,
        "wait_time": 5
    },
    "BetMGM": {
        "url": "https://sports.on.betmgm.ca/en/sports",
        "market_selector": "ms-event-group",
        "event_selector": "ms-event",
        "odds_selector": "div.option-indicator",
        "timeout": 10,
        "wait_time": 5
    }
}

# Function to create and configure the WebDriver
def create_driver():
    logger.info("Setting up Chrome WebDriver...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    try:
        # Try to use the service with specified chromedriver path
        service = Service(executable_path="/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set webdriver properties to evade detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("WebDriver successfully created")
        return driver
    except Exception as e:
        logger.error(f"Error creating WebDriver: {str(e)}")
        logger.error(traceback.format_exc())
        send_email("Arbitrage Bot Error", f"Failed to create WebDriver: {str(e)}\n{traceback.format_exc()}")
        raise

# Function to send email notifications
def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        
        # Add timestamp to all emails
        timestamped_body = f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{body}"
        msg.attach(MIMEText(timestamped_body, 'plain'))
        
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            
        logger.info(f"Email sent: {subject}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        logger.error(traceback.format_exc())
        return False

# Heartbeat function to keep Render from marking the bot as inactive
def send_heartbeat():
    while True:
        try:
            logger.info(f"Heartbeat: Bot is active at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            # Only log heartbeat, don't email to avoid spam
            time.sleep(HEARTBEAT_INTERVAL)
        except Exception as e:
            logger.error(f"Error in heartbeat: {str(e)}")
            time.sleep(60)  # If error, retry after 1 minute

# Class to represent a betting event
class BettingEvent:
    def __init__(self, event_name, market_type, bookmaker, odds=None, timestamp=None):
        self.event_name = event_name
        self.market_type = market_type  # e.g., "Money Line", "Spread", etc.
        self.bookmaker = bookmaker
        self.odds = odds or []  # List of odds values
        self.timestamp = timestamp or datetime.now()
    
    def __str__(self):
        return f"{self.event_name} | {self.market_type} | {self.bookmaker} | Odds: {', '.join(map(str, self.odds))}"

# Function to safely scrape odds with better error handling
def scrape_betting_site(driver, site_name):
    site_config = BETTING_SITES.get(site_name)
    if not site_config:
        logger.error(f"No configuration found for site: {site_name}")
        return []
    
    events = []
    url = site_config["url"]
    
    try:
        logger.info(f"Navigating to {site_name}: {url}")
        driver.get(url)
        
        # Wait for the main content to load
        WebDriverWait(driver, site_config["timeout"]).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, site_config["market_selector"]))
        )
        
        # Additional wait to ensure dynamic content loads
        time.sleep(site_config["wait_time"])
        
        # Take a screenshot for debugging (disabled in production)
        # driver.save_screenshot(f"{site_name.lower()}_screenshot.png")
        
        # Find all event containers
        market_elements = driver.find_elements(By.CSS_SELECTOR, site_config["market_selector"])
        logger.info(f"Found {len(market_elements)} market elements on {site_name}")
        
        # For each market, try to extract events and odds
        for i, market in enumerate(market_elements[:5]):  # Limit to first 5 markets to prevent overload
            try:
                # Try to extract market type (might need adjustment based on site structure)
                market_type = "Money Line"  # Default
                try:
                    market_type_elem = market.find_element(By.CSS_SELECTOR, "div.market-name")
                    if market_type_elem:
                        market_type = market_type_elem.text
                except NoSuchElementException:
                    pass  # Use default market type
                
                # Find events in this market
                event_elements = market.find_elements(By.CSS_SELECTOR, site_config["event_selector"])
                
                for event in event_elements:
                    try:
                        # Try to extract event name
                        event_name = "Unknown Event"
                        try:
                            name_elem = event.find_element(By.CSS_SELECTOR, "div.event-name, span.srb-ParticipantFixtureDetails_TeamName")
                            if name_elem:
                                event_name = name_elem.text
                        except NoSuchElementException:
                            # If we can't find the specific element, use the event text
                            event_name = event.text.split('\n')[0] if event.text else "Unknown Event"
                        
                        # Extract odds for this event
                        odds_elements = event.find_elements(By.CSS_SELECTOR, site_config["odds_selector"])
                        odds = []
                        
                        for odd in odds_elements:
                            if odd.text and odd.text.strip():
                                # Clean odds text and convert to a decimal value if possible
                                odd_text = odd.text.strip()
                                try:
                                    # Handle American odds format (+150, -200) and convert to decimal
                                    if odd_text.startswith('+'):
                                        odd_value = float(odd_text[1:]) / 100 + 1
                                    elif odd_text.startswith('-'):
                                        odd_value = 100 / float(odd_text[1:]) + 1
                                    else:
                                        odd_value = float(odd_text)
                                    odds.append(round(odd_value, 2))
                                except ValueError:
                                    odds.append(odd_text)  # Keep as string if conversion fails
                        
                        if odds:
                            new_event = BettingEvent(event_name, market_type, site_name, odds)
                            events.append(new_event)
                            logger.info(f"Extracted event: {new_event}")
                    except Exception as e:
                        logger.warning(f"Error processing event in {site_name}: {str(e)}")
                        continue
            except Exception as e:
                logger.warning(f"Error processing market {i} in {site_name}: {str(e)}")
                continue
        
        logger.info(f"Successfully scraped {len(events)} events from {site_name}")
        return events
    
    except TimeoutException:
        logger.error(f"Timeout waiting for {site_name} to load")
        error_screenshot = f"{site_name.lower()}_error.png"
        driver.save_screenshot(error_screenshot)
        send_email(
            f"Arbitrage Bot - {site_name} Timeout Error", 
            f"The bot timed out while trying to load {url}. Check the logs for more details."
        )
        return []
    
    except WebDriverException as e:
        logger.error(f"WebDriver error for {site_name}: {str(e)}")
        return []
    
    except Exception as e:
        logger.error(f"Unexpected error scraping {site_name}: {str(e)}")
        logger.error(traceback.format_exc())
        send_email(
            f"Arbitrage Bot - {site_name} Scraping Error", 
            f"Error scraping {site_name}: {str(e)}\n{traceback.format_exc()}"
        )
        return []

# Function to find matching events across different bookmakers
def find_matching_events(events_by_site):
    # Group events by name to find matches
    events_by_name = {}
    
    for site, events in events_by_site.items():
        for event in events:
            event_key = event.event_name.lower().strip()
            if event_key not in events_by_name:
                events_by_name[event_key] = []
            events_by_name[event_key].append(event)
    
    # Find events that appear in multiple bookmakers
    matching_events = []
    for event_name, events in events_by_name.items():
        if len(set(event.bookmaker for event in events)) >= 2:  # At least 2 different bookmakers
            matching_events.append(events)
    
    return matching_events

# Function to check for arbitrage opportunities in matching events
def check_arbitrage(matching_events):
    opportunities = []
    
    for events in matching_events:
        # Group events by market type
        events_by_market = {}
        for event in events:
            if event.market_type not in events_by_market:
                events_by_market[event.market_type] = []
            events_by_market[event.market_type].append(event)
        
        # For each market type, check for arbitrage
        for market_type, market_events in events_by_market.items():
            # Skip markets with fewer than 2 bookmakers
            bookmakers = set(event.bookmaker for event in market_events)
            if len(bookmakers) < 2:
                continue
            
            # Check if we have enough odds data
            valid_odds = all(len(event.odds) > 0 for event in market_events)
            if not valid_odds:
                continue
            
            # For 2-way markets (e.g., tennis, player props)
            if all(len(event.odds) == 2 for event in market_events):
                # Try all combinations of odds from different bookmakers
                for i, event1 in enumerate(market_events):
                    for event2 in market_events[i+1:]:
                        # Check home/away combinations
                        try:
                            # Home from event1, Away from event2
                            implied_prob1 = 1 / event1.odds[0] + 1 / event2.odds[1]
                            
                            # Home from event2, Away from event1
                            implied_prob2 = 1 / event2.odds[0] + 1 / event1.odds[1]
                            
                            # Check for arbitrage
                            if implied_prob1 < 1 or implied_prob2 < 1:
                                arb_margin = min(implied_prob1, implied_prob2)
                                profit = round((1 - arb_margin) * 100, 2)
                                
                                opportunity = {
                                    "event_name": event1.event_name,
                                    "market_type": market_type,
                                    "bookmakers": [event1.bookmaker, event2.bookmaker],
                                    "implied_probability": arb_margin,
                                    "profit_percentage": profit,
                                    "bet_details": [
                                        f"{event1.bookmaker} - {event1.odds[0]} for outcome 1",
                                        f"{event2.bookmaker} - {event2.odds[1]} for outcome 2"
                                    ] if implied_prob1 < implied_prob2 else [
                                        f"{event2.bookmaker} - {event2.odds[0]} for outcome 1",
                                        f"{event1.bookmaker} - {event1.odds[1]} for outcome 2"
                                    ]
                                }
                                opportunities.append(opportunity)
                        except (IndexError, ZeroDivisionError, TypeError):
                            continue
            
            # For 3-way markets (e.g., soccer)
            elif all(len(event.odds) == 3 for event in market_events):
                # Try all combinations of odds from different bookmakers
                for i, event1 in enumerate(market_events):
                    for j, event2 in enumerate(market_events[i+1:], i+1):
                        for event3 in market_events[j+1:]:
                            for idx1 in range(3):
                                for idx2 in range(3):
                                    if idx1 == idx2:
                                        continue
                                    for idx3 in range(3):
                                        if idx1 == idx3 or idx2 == idx3:
                                            continue
                                        
                                        try:
                                            # Calculate implied probability
                                            implied_prob = (1 / event1.odds[idx1]) + (1 / event2.odds[idx2]) + (1 / event3.odds[idx3])
                                            
                                            # Check for arbitrage
                                            if implied_prob < 1:
                                                profit = round((1 - implied_prob) * 100, 2)
                                                
                                                opportunity = {
                                                    "event_name": event1.event_name,
                                                    "market_type": market_type,
                                                    "bookmakers": [event1.bookmaker, event2.bookmaker, event3.bookmaker],
                                                    "implied_probability": implied_prob,
                                                    "profit_percentage": profit,
                                                    "bet_details": [
                                                        f"{event1.bookmaker} - {event1.odds[idx1]} for outcome {idx1+1}",
                                                        f"{event2.bookmaker} - {event2.odds[idx2]} for outcome {idx2+1}",
                                                        f"{event3.bookmaker} - {event3.odds[idx3]} for outcome {idx3+1}"
                                                    ]
                                                }
                                                opportunities.append(opportunity)
                                        except (IndexError, ZeroDivisionError, TypeError):
                                            continue
    
    return opportunities

# Function to format arbitrage opportunity into a readable message
def format_opportunity(opportunity):
    message = [
        f"Event: {opportunity['event_name']}",
        f"Market: {opportunity['market_type']}",
        f"Profit: {opportunity['profit_percentage']}%",
        f"Implied Probability: {opportunity['implied_probability']:.4f}",
        "\nBetting instructions:",
    ]
    
    for detail in opportunity['bet_details']:
        message.append(f"- {detail}")
    
    # Calculate optimal stake distribution
    total_stake = 1000  # Example total stake
    message.append(f"\nStake Distribution (Total: ${total_stake}):")
    
    for detail in opportunity['bet_details']:
        parts = detail.split(" - ")
        if len(parts) == 2:
            bookmaker = parts[0]
            odds_part = parts[1].split(" for ")[0]
            try:
                odds = float(odds_part)
                stake_percentage = (1 / odds) / opportunity['implied_probability']
                stake_amount = round(total_stake * stake_percentage, 2)
                message.append(f"- {bookmaker}: ${stake_amount} ({stake_percentage:.2%})")
            except ValueError:
                message.append(f"- {bookmaker}: Stake calculation failed")
    
    return "\n".join(message)

# Main function
def main():
    global startup_email_sent
    
    logger.info("Starting arbitrage betting bot...")
    
    # Send startup email only once
    if not startup_email_sent:
        send_email(
            "Arbitrage Bot Started",
            "The arbitrage betting bot has been started and is now monitoring betting sites for opportunities."
        )
        startup_email_sent = True
    
    # Start heartbeat in a separate thread
    heartbeat_thread = threading.Thread(target=send_heartbeat, daemon=True)
    heartbeat_thread.start()
    
    driver = None
    try:
        # Create WebDriver
        driver = create_driver()
        
        # Main loop
        while True:
            try:
                logger.info("Starting new scraping cycle...")
                
                # Collect events from all sites
                events_by_site = {}
                for site_name in BETTING_SITES.keys():
                    events = scrape_betting_site(driver, site_name)
                    events_by_site[site_name] = events
                    # Small delay between sites to avoid overloading
                    time.sleep(5)
                
                # Find matching events across sites
                matching_events = find_matching_events(events_by_site)
                logger.info(f"Found {len(matching_events)} potentially matching events across sites")
                
                # Check for arbitrage opportunities
                opportunities = check_arbitrage(matching_events)
                
                # Report any opportunities found
                if opportunities:
                    # Sort by profit percentage (highest first)
                    opportunities.sort(key=lambda x: x['profit_percentage'], reverse=True)
                    
                    # Send top 5 opportunities to avoid email overload
                    top_opportunities = opportunities[:5]
                    
                    for i, opportunity in enumerate(top_opportunities):
                        message = format_opportunity(opportunity)
                        subject = f"Arbitrage Opportunity #{i+1} - {opportunity['profit_percentage']}% Profit"
                        send_email(subject, message)
                        
                    logger.info(f"Found {len(opportunities)} arbitrage opportunities, sent top {len(top_opportunities)}")
                else:
                    logger.info("No arbitrage opportunities found in this cycle")
                
                # Sleep before the next cycle
                logger.info(f"Sleeping for {SCRAPE_INTERVAL} seconds before next cycle...")
                time.sleep(SCRAPE_INTERVAL)
            
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                logger.error(traceback.format_exc())
                send_email(
                    "Arbitrage Bot Error",
                    f"An error occurred in the main processing loop: {str(e)}\n{traceback.format_exc()}"
                )
                # Sleep before retry
                time.sleep(60)
    
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
        logger.critical(traceback.format_exc())
        send_email(
            "Arbitrage Bot - FATAL ERROR",
            f"A fatal error occurred and the bot is stopping: {str(e)}\n{traceback.format_exc()}"
        )
    
    finally:
        if driver:
            try:
                driver.quit()
                logger.info("WebDriver closed")
            except Exception:
                pass

if __name__ == "__main__":
    main()
