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
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class LinkedInScraper:
    def __init__(self):
        # Top Companies by Revenue and Employee Size
        self.COMPANY_PAGES = {
            # Financial Services
            'safaricom': {'name': 'Safaricom PLC', 'sector': 'Telecommunications'},
            'kcb-bank-kenya': {'name': 'KCB Bank Kenya', 'sector': 'Banking'},
            'equity-bank-kenya': {'name': 'Equity Bank Kenya', 'sector': 'Banking'},
            'co-operative-bank-of-kenya': {'name': 'Co-operative Bank of Kenya', 'sector': 'Banking'},
            'standard-chartered-bank-kenya': {'name': 'Standard Chartered Bank Kenya', 'sector': 'Banking'},
            'absa-bank-kenya': {'name': 'Absa Bank Kenya', 'sector': 'Banking'},
            'ncba-bank-kenya': {'name': 'NCBA Bank Kenya', 'sector': 'Banking'},
            'i&m-bank-kenya': {'name': 'I&M Bank Kenya', 'sector': 'Banking'},
            
            # Insurance
            'jubilee-insurance': {'name': 'Jubilee Insurance', 'sector': 'Insurance'},
            'britam': {'name': 'Britam Holdings', 'sector': 'Insurance'},
            'cic-insurance-group': {'name': 'CIC Insurance Group', 'sector': 'Insurance'},
            'liberty-kenya-holdings': {'name': 'Liberty Kenya Holdings', 'sector': 'Insurance'},
            'apa-insurance': {'name': 'APA Insurance', 'sector': 'Insurance'},
            
            # Technology & Innovation
            'microsoft-africa-development-center': {'name': 'Microsoft ADC', 'sector': 'Technology'},
            'google-kenya': {'name': 'Google Kenya', 'sector': 'Technology'},
            'ibm-kenya': {'name': 'IBM Kenya', 'sector': 'Technology'},
            'oracle-kenya': {'name': 'Oracle Kenya', 'sector': 'Technology'},
            'cisco-kenya': {'name': 'Cisco Kenya', 'sector': 'Technology'},
            
            # Telecommunications
            'airtel-kenya': {'name': 'Airtel Kenya', 'sector': 'Telecommunications'},
            'telkom-kenya': {'name': 'Telkom Kenya', 'sector': 'Telecommunications'},
            
            # Manufacturing & Industry
            'east-african-breweries': {'name': 'East African Breweries', 'sector': 'Manufacturing'},
            'bamburi-cement': {'name': 'Bamburi Cement', 'sector': 'Manufacturing'},
            'kenya-electricity-generating-company-kengen': {'name': 'KenGen', 'sector': 'Energy'},
            'kenya-power': {'name': 'Kenya Power', 'sector': 'Energy'},
            
            # Tech Startups
            'twiga-foods': {'name': 'Twiga Foods', 'sector': 'AgriTech'},
            'sendy': {'name': 'Sendy', 'sector': 'Logistics'},
            'cellulant': {'name': 'Cellulant', 'sector': 'FinTech'},
            'ushahidi': {'name': 'Ushahidi', 'sector': 'Technology'},
            'africa-talking': {'name': "Africa's Talking", 'sector': 'Technology'},
            'andela-kenya': {'name': 'Andela Kenya', 'sector': 'Technology'},
            'm-kopa': {'name': 'M-KOPA', 'sector': 'FinTech'},
            'kopokopo': {'name': 'KopoKopo', 'sector': 'FinTech'},
            
            # Consulting & Professional Services
            'deloitte-east-africa': {'name': 'Deloitte East Africa', 'sector': 'Consulting'},
            'pwc-kenya': {'name': 'PwC Kenya', 'sector': 'Consulting'},
            'kpmg-east-africa': {'name': 'KPMG East Africa', 'sector': 'Consulting'},
            'ernst-young-kenya': {'name': 'EY Kenya', 'sector': 'Consulting'}
        }
        
        # Updated CSS Selectors for LinkedIn 2024
        self.SELECTORS = {
            'post_container': 'div.feed-shared-update-v2',
            'post_text': 'div.feed-shared-update-v2__description span.break-words',
            'author_name': 'span.feed-shared-actor__name',
            'author_title': 'span.feed-shared-actor__description',
            'engagement_stats': 'ul.social-details-social-counts',
            'likes': 'button.social-details-social-counts__reactions-count',
            'comments': 'button.social-details-social-counts__comments',
            'shares': 'button.social-details-social-counts__shares'
        }
        
        self.KEYWORDS = [
            "AI", "artificial intelligence", "machine learning", 
            "automation", "digital transformation", "reskilling", 
            "upskilling", "innovation", "tech", "technology",
            "digital skills", "future of work", "data science",
            "robotics", "blockchain", "cloud computing", "IoT",
            "digital adoption", "tech talent", "digital economy",
            "fintech", "cyber security", "big data", "analytics"
        ]
        
        self.setup_driver()
    
    def setup_driver(self):
        """Configure and initialize the Chrome WebDriver with optimal settings"""
        try:
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            # Add random user agent
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            ]
            options.add_argument(f"user-agent={random.choice(user_agents)}")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 10)
            logger.info("Successfully initialized Chrome WebDriver")
            
        except Exception as e:
            logger.error(f"Error setting up WebDriver: {str(e)}")
            raise

    def login(self):
        """Safely log into LinkedIn with error handling"""
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
            
            # Wait for login to complete
            time.sleep(5)
            logger.info("Successfully logged in to LinkedIn")
            
        except Exception as e:
            logger.error(f"Failed to log in: {str(e)}")
            raise

    def scroll_page(self, scroll_count=5):
        """Scroll the page with random intervals to appear more human-like"""
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
                text_element = post.find_element(By.CSS_SELECTOR, self.SELECTORS['post_text'])
                text = text_element.text
            except NoSuchElementException:
                text = ""
            
            # Get author details
            try:
                author_element = post.find_element(By.CSS_SELECTOR, self.SELECTORS['author_name'])
                author_name = author_element.text
            except NoSuchElementException:
                author_name = ""
                
            try:
                title_element = post.find_element(By.CSS_SELECTOR, self.SELECTORS['author_title'])
                author_title = title_element.text
            except NoSuchElementException:
                author_title = ""
            
            # Get engagement metrics
            try:
                likes = post.find_element(By.CSS_SELECTOR, self.SELECTORS['likes']).text
                likes = int(''.join(filter(str.isdigit, likes))) if likes else 0
            except NoSuchElementException:
                likes = 0
                
            try:
                comments = post.find_element(By.CSS_SELECTOR, self.SELECTORS['comments']).text
                comments = int(''.join(filter(str.isdigit, comments))) if comments else 0
            except NoSuchElementException:
                comments = 0
                
            try:
                shares = post.find_element(By.CSS_SELECTOR, self.SELECTORS['shares']).text
                shares = int(''.join(filter(str.isdigit, shares))) if shares else 0
            except NoSuchElementException:
                shares = 0
            
            return {
                'text': text,
                'author_name': author_name,
                'author_title': author_title,
                'likes': likes,
                'comments': comments,
                'shares': shares,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            logger.error(f"Error extracting post data: {str(e)}")
            return None

    def scrape_company_page(self, company_handle, company_info):
        """Scrape posts from a company's LinkedIn page"""
        try:
            url = f"https://www.linkedin.com/company/{company_handle}/posts/"
            logger.info(f"Scraping company page: {company_handle}")
            
            self.driver.get(url)
            time.sleep(random.uniform(3, 5))
            
            # Wait for content to load
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.SELECTORS['post_container'])))
            except TimeoutException:
                logger.warning(f"No posts found for {company_handle}")
                return []
            
            self.scroll_page()
            posts_data = []
            
            # Find all posts
            posts = self.driver.find_elements(By.CSS_SELECTOR, self.SELECTORS['post_container'])
            
            for post in posts:
                try:
                    post_data = self.extract_post_data(post)
                    if post_data and any(keyword.lower() in post_data['text'].lower() for keyword in self.KEYWORDS):
                        post_data.update({
                            'company': company_info['name'],
                            'company_handle': company_handle,
                            'sector': company_info['sector']
                        })
                        posts_data.append(post_data)
                except Exception as e:
                    logger.error(f"Error processing post: {str(e)}")
                    continue
            
            logger.info(f"Collected {len(posts_data)} relevant posts from {company_handle}")
            return posts_data
            
        except Exception as e:
            logger.error(f"Error scraping company {company_handle}: {str(e)}")
            return []

    def save_data(self, all_posts):
        """Save collected data with timestamp"""
        try:
            if not all_posts:
                logger.warning("No posts to save")
                return
                
            # Create data directory if it doesn't exist
            os.makedirs('data', exist_ok=True)
            
            # Save to CSV
            df = pd.DataFrame(all_posts)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'data/linkedin_posts_{timestamp}.csv'
            
            df.to_csv(filename, index=False)
            logger.info(f"Successfully saved {len(df)} posts to {filename}")
            
            # Save raw data as backup
            with open(f'data/linkedin_raw_{timestamp}.json', 'w', encoding='utf-8') as f:
                json.dump(all_posts, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved raw data backup to data/linkedin_raw_{timestamp}.json")
            
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")

    def run(self):
        """Main execution method"""
        try:
            self.login()
            all_posts = []
            
            for handle, info in self.COMPANY_PAGES.items():
                try:
                    posts = self.scrape_company_page(handle, info)
                    all_posts.extend(posts)
                    # Random delay between companies
                    time.sleep(random.uniform(20, 30))
                except Exception as e:
                    logger.error(f"Error processing company {handle}: {str(e)}")
                    continue
            
            self.save_data(all_posts)
            
        except Exception as e:
            logger.error(f"Error in main execution: {str(e)}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    scraper = LinkedInScraper()
    scraper.run() 