import os
import time
import json
import random
import logging
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_test_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class LinkedInTestScraper:
    def __init__(self):
        # Try a different URL format
        self.COMPANY_URL = "https://www.linkedin.com/company/safaricom/"
        
        # Simplified selectors - just find any post content
        self.SELECTORS = {
            'any_post': 'div[class*="feed-shared-update-v2"]',
            'any_text': 'span[class*="break-words"]',
            'any_time': 'time',
            'any_button': 'button'
        }
        
        # Wait for posts to load selector
        self.POSTS_LOAD_WAIT = 'div.scaffold-finite-scroll__content'

        self.KEYWORDS = [
            'AI', 'artificial intelligence', 'machine learning',
            'digital transformation', 'automation', 'innovation',
            'tech', 'technology', 'future of work', 'digital',
            'data', 'analytics', 'cloud', 'blockchain',
            'upskilling', 'reskilling', 'workforce'
        ]
        
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver with anti-detection options"""
        try:
            options = Options()
            
            # Anti-detection options
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-extensions')
            options.add_argument('--profile-directory=Default')
            options.add_argument("--incognito")
            options.add_argument("--disable-plugins-discovery")
            options.add_argument("--start-maximized")
            
            # Add random user agent
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            ]
            options.add_argument(f'user-agent={random.choice(user_agents)}')
            
            # Add experimental options
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Initialize driver
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            self.wait = WebDriverWait(self.driver, 20)  # Increased wait time
            
            # Execute CDP commands to prevent detection
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": random.choice(user_agents)
            })
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """
            })
            
            logger.info("Successfully initialized Chrome WebDriver")
            return True
        except Exception as e:
            logger.error(f"Error setting up WebDriver: {str(e)}")
            return False

    def login(self):
        """Log into LinkedIn"""
        try:
            logger.info("Attempting to log in to LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(random.uniform(2, 4))
            
            # Wait for elements and login
            username = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            password = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
            
            username.send_keys(os.getenv('LINKEDIN_EMAIL'))
            time.sleep(random.uniform(1, 2))
            password.send_keys(os.getenv('LINKEDIN_PASSWORD'))
            time.sleep(random.uniform(1, 2))
            
            submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            submit_button.click()
            
            time.sleep(5)
            logger.info("Successfully logged in to LinkedIn")
            
        except Exception as e:
            logger.error(f"Failed to log in: {str(e)}")
            raise

    def scroll_page(self, scroll_count=5):
        """Scroll the page to load more content"""
        try:
            for i in range(scroll_count):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))
                logger.debug(f"Completed scroll {i+1}/{scroll_count}")
        except Exception as e:
            logger.error(f"Error during scrolling: {str(e)}")

    def extract_post_data(self, post):
        """Extract data from a single post"""
        try:
            # Get post text
            try:
                text_container = post.find_element(By.CSS_SELECTOR, self.SELECTORS['post_text'])
                # Get text before the "...see more" button if it exists
                text = text_container.text.split('…more')[0].strip()
            except NoSuchElementException:
                text = ""
            
            # Get post timestamp
            try:
                time_element = post.find_element(By.CSS_SELECTOR, self.SELECTORS['post_time'])
                post_time = time_element.text.split('•')[0].strip()  # Get time part before the bullet point
            except NoSuchElementException:
                post_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Get engagement metrics
            try:
                likes_elem = post.find_element(By.CSS_SELECTOR, self.SELECTORS['engagement']['likes'])
                likes_text = likes_elem.text.split('and')[0]  # Handle "X and Y others" format
                likes = int(''.join(filter(str.isdigit, likes_text))) if likes_text else 0
            except (NoSuchElementException, ValueError):
                likes = 0
                
            try:
                comments_elem = post.find_element(By.CSS_SELECTOR, self.SELECTORS['engagement']['comments'])
                comments = int(''.join(filter(str.isdigit, comments_elem.text))) if comments_elem.text else 0
            except (NoSuchElementException, ValueError):
                comments = 0
                
            try:
                reposts_elem = post.find_element(By.CSS_SELECTOR, self.SELECTORS['engagement']['reposts'])
                reposts = int(''.join(filter(str.isdigit, reposts_elem.text))) if reposts_elem.text else 0
            except (NoSuchElementException, ValueError):
                reposts = 0
            
            # Check if post contains relevant keywords
            if text and any(keyword.lower() in text.lower() for keyword in self.KEYWORDS):
                post_data = {
                    'text': text,
                    'post_time': post_time,
                    'likes': likes,
                    'comments': comments,
                    'reposts': reposts,
                    'company': 'Safaricom',
                    'url': self.COMPANY_URL,
                    'collected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                logger.info(f"Found relevant post with {likes} likes, {comments} comments")
                return post_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting post data: {str(e)}")
            return None

    def scrape_posts(self):
        """Scrape posts from Safaricom's LinkedIn page"""
        try:
            logger.info("Navigating to Safaricom's LinkedIn page")
            self.driver.get(self.COMPANY_URL)
            time.sleep(10)  # Long initial wait
            
            # Try to click the posts tab
            try:
                posts_tab = self.driver.find_element(By.XPATH, "//a[contains(@href, '/posts/')]")
                posts_tab.click()
                logger.info("Clicked posts tab")
                time.sleep(5)
            except Exception as e:
                logger.error(f"Could not find posts tab: {str(e)}")
            
            logger.info("Looking for any posts...")
            # Try different post selectors
            post_selectors = [
                'div[class*="feed-shared-update-v2"]',
                'div[class*="update-components-text"]',
                'div[class*="feed-shared-update"]',
                'div[class*="update-components-actor"]',
                'div[class*="feed-shared-inline-show-more-text"]',
                'div[class*="update-components-text"]'
            ]
            
            # Scroll a few times
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            
            found_elements = []
            for selector in post_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        logger.info(f"Found {len(elements)} elements with selector: {selector}")
                        found_elements.extend(elements)
                except Exception as e:
                    logger.error(f"Error with selector {selector}: {str(e)}")
            
            if not found_elements:
                logger.warning("No elements found with any selector")
                # Save page source for debugging
                with open('linkedin_page.html', 'w', encoding='utf-8') as f:
                    f.write(self.driver.page_source)
                logger.info("Saved page source to linkedin_page.html")
                return []
            
            # Try to get any text content
            posts_data = []
            for element in found_elements:
                try:
                    # Get element HTML for debugging
                    html = element.get_attribute('outerHTML')
                    logger.info(f"Found element HTML: {html[:200]}...")  # Log first 200 chars
                    
                    # Try to get text
                    text = element.text
                    if text:
                        logger.info(f"Found text content: {text[:100]}...")
                        posts_data.append({
                            'text': text,
                            'html': html,
                            'tag_name': element.tag_name,
                            'class_name': element.get_attribute('class')
                        })
                except Exception as e:
                    logger.error(f"Error extracting content: {str(e)}")
                    continue
            
            logger.info(f"Found {len(posts_data)} elements with content")
            return posts_data
            
        except Exception as e:
            logger.error(f"Error scraping posts: {str(e)}")
            # Save page source for debugging
            with open('linkedin_error_page.html', 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            logger.info("Saved error page source to linkedin_error_page.html")
            return []

    def save_data(self, posts_data):
        """Save collected data"""
        try:
            if not posts_data:
                logger.warning("No posts to save")
                return
            
            # Create data directory if it doesn't exist
            os.makedirs('data', exist_ok=True)
            
            # Save to CSV
            df = pd.DataFrame(posts_data)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'data/safaricom_posts_{timestamp}.csv'
            
            df.to_csv(filename, index=False)
            logger.info(f"Successfully saved {len(df)} posts to {filename}")
            
            # Save raw data as backup
            with open(f'data/safaricom_raw_{timestamp}.json', 'w', encoding='utf-8') as f:
                json.dump(posts_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved raw data backup to data/safaricom_raw_{timestamp}.json")
            
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")

    def run(self):
        """Main execution method"""
        try:
            self.setup_driver()
            self.login()
            posts = self.scrape_posts()
            
            if posts:
                # Save raw data for analysis
                with open('linkedin_debug.json', 'w', encoding='utf-8') as f:
                    json.dump(posts, f, indent=2, ensure_ascii=False)
                logger.info("Saved debug data to linkedin_debug.json")
            
            self.driver.quit()
            return posts
        except Exception as e:
            logger.error(f"Error in main execution: {str(e)}")
            if self.driver:
                self.driver.quit()
            return []

if __name__ == "__main__":
    scraper = LinkedInTestScraper()
    scraper.run() 