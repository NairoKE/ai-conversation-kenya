import os
import tweepy
import pandas as pd
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('twitter_collector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def setup_twitter_client():
    """Initialize Twitter API client with credentials"""
    try:
        client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            wait_on_rate_limit=True
        )
        logger.info("Successfully authenticated with Twitter API")
        return client
    except Exception as e:
        logger.error(f"Error authenticating with Twitter API: {str(e)}")
        raise

def collect_tweets(client, query, max_results=100):
    """Collect tweets for a specific query"""
    tweets_data = []
    
    try:
        # Search tweets
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=['created_at', 'public_metrics', 'author_id'],
            user_fields=['username', 'public_metrics', 'verified'],
            expansions=['author_id']
        )
        
        if not response.data:
            logger.warning(f"No tweets found for query: {query}")
            return []
            
        # Process users lookup
        users = {user.id: user for user in response.includes['users']}
        
        for tweet in response.data:
            user = users.get(tweet.author_id, {})
            
            tweet_data = {
                'created_at': tweet.created_at,
                'text': tweet.text,
                'username': user.username if user else None,
                'user_followers': user.public_metrics['followers_count'] if user else None,
                'user_verified': user.verified if user else None,
                'retweet_count': tweet.public_metrics['retweet_count'],
                'like_count': tweet.public_metrics['like_count'],
                'reply_count': tweet.public_metrics['reply_count'],
                'quote_count': tweet.public_metrics['quote_count'],
                'query': query
            }
            tweets_data.append(tweet_data)
            
        logger.info(f"Collected {len(tweets_data)} tweets for query: {query}")
        
    except Exception as e:
        logger.error(f"Error collecting tweets for query {query}: {str(e)}")
    
    return tweets_data

def main():
    # Initialize Twitter client
    client = setup_twitter_client()
    
    # Define search queries
    search_queries = [
        '(AI OR "artificial intelligence") (Kenya OR Nairobi) -is:retweet',
        '"digital transformation" (Kenya OR Nairobi) -is:retweet',
        '"machine learning" (Kenya OR Nairobi) -is:retweet',
        '(tech OR technology) (upskilling OR reskilling) (Kenya OR Nairobi) -is:retweet',
        'AI (startup OR innovation) (Kenya OR Nairobi) -is:retweet'
    ]
    
    # Collect tweets for each query
    all_tweets = []
    for query in search_queries:
        tweets = collect_tweets(client, query)
        all_tweets.extend(tweets)
    
    # Convert to DataFrame and remove duplicates
    df = pd.DataFrame(all_tweets)
    df = df.drop_duplicates(subset=['text'])
    
    # Save to CSV with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'data/twitter_data_{timestamp}.csv'
    df.to_csv(filename, index=False)
    logger.info(f"Saved {len(df)} unique tweets to {filename}")
    
    # Save raw data as backup
    with open(f'data/twitter_raw_{timestamp}.json', 'w') as f:
        json.dump(all_tweets, f)
    logger.info(f"Saved raw data backup to data/twitter_raw_{timestamp}.json")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}") 