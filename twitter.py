import httpx
from twkit import client
from datetime import datetime
import csv
import time
from random import randint
import dontshare as d

# Monkey patch (may not be needed, but included for compatibility)
def patch_client(*args, **kwargs):
    kwargs['proxy'] = None
    return httpx.Client(*args, **kwargs)

httpx.Client = patch_client

# Configuration
USERNAME = d.username
EMAIL = d.email
PASSWORD = d.password
QUERY = "Solana"  # You can change this to any search query
MINIMUM_TWEETS = 500
SEARCH_STYLE = "latest"  # Can be "latest" or "top"
IGNORE_LIST = ["telegram", "discount", "promo", "sale", "join", "t.co"]

# Function to get tweets
def get_tweets(tweets):
    if tweets is None:
        print(f"Time is {datetime.now()}: Getting next tweets")
        time.sleep(randint(2, 6))
        tweets = client.search_tweet(query=QUERY, product=SEARCH_STYLE)
    else:
        print(f"Time is {datetime.now()}: Getting next tweets")
        time.sleep(randint(2, 6))
        tweets = tweets.next()
    return tweets

# Function to check if a tweet should be ignored
def should_ignore_tweet(text):
    return any(word.lower() in text.lower() for word in IGNORE_LIST)

# Main script
def main():
    # Load cookies (assumes you've already logged in and saved cookies)
    client.load_cookies("cookies.json")

    tweet_count = 0
    tweets = None

    with open("tweets.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["tweet_count", "username", "text", "created_at", "retweet_count", "favorite_count", "reply_count"])

        while tweet_count < MINIMUM_TWEETS:
            try:
                tweets = get_tweets(tweets)

                if not tweets:
                    print(f"Time is {datetime.now()}: No tweets found")
                    break

                for tweet in tweets:
                    if should_ignore_tweet(tweet.text):
                        continue

                    tweet_count += 1
                    tweet_data = [
                        tweet_count,
                        tweet.user.name,
                        tweet.text,
                        tweet.created_at,
                        tweet.retweet_count,
                        tweet.favorite_count,
                        tweet.reply_count
                    ]

                    print(tweet_data)
                    writer.writerow(tweet_data)

                    print(f"Time is {datetime.now()}: Tweet count is {tweet_count}")

                    if tweet_count >= MINIMUM_TWEETS:
                        break

            except client.TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                print(f"Time is {datetime.now()}: Rate limit exceeded")
                wait_time = rate_limit_reset - datetime.now()
                print(f"Waiting {wait_time}")
                time.sleep(wait_time.total_seconds())
                continue

if __name__ == "__main__":
    main()

# Note: Before running this script for the first time, you need to log in and save cookies:
# client.login(auth_info_1=USERNAME, auth_info_2=EMAIL, password=PASSWORD)
# client.save_cookies("cookies.json")























# # solana_sentiment.py

# import sys
# import asyncio
# import tweepy
# import pandas as pd
# import re
# from nltk.sentiment import SentimentIntensityAnalyzer
# import nltk
# from datetime import datetime
# from urllib.parse import urlparse
# import os

# # Download VADER lexicon if not already downloaded
# nltk.download('vader_lexicon')

# # Import credentials from config.py
# from config import BEARER_TOKEN

# # Initialize Tweepy client
# client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

# # Define search query
# # - 'Solana' keyword
# # - Exclude retweets and replies for cleaner data
# # - Specify language as English
# query = "Solana -is:retweet -is:reply lang:en"

# # Initialize VADER sentiment analyzer
# sia = SentimentIntensityAnalyzer()

# def filter_tweets(tweet):
#     """
#     Filters out tweets that contain unwanted content such as links, discount offers, Telegram invites, etc.
#     """
#     # Define unwanted patterns
#     unwanted_patterns = [
#         r'http\S+',            # URLs
#         r'RT @\w+:',           # Retweets (already excluded, but added for safety)
#         r'\bdiscount\b',
#         r'\bTelegram\b',
#         r'\btelegrams\b',
#         r'\bpromo\b',
#         r'\bcoupon\b',
#         r'\bsale\b',
#         r'\bwin\b',
#         r'\bbuy now\b',
#         r'\bfree\b'
#     ]
    
#     # Combine patterns into a single regex
#     pattern = re.compile('|'.join(unwanted_patterns), re.IGNORECASE)
    
#     # Check if tweet text matches any unwanted pattern
#     if pattern.search(tweet):
#         return False
#     return True

# def analyze_sentiment(text):
#     """
#     Analyzes the sentiment of a given text and returns positive, negative, or neutral.
#     """
#     scores = sia.polarity_scores(text)
#     compound = scores['compound']
#     if compound >= 0.05:
#         return 'Positive'
#     elif compound <= -0.05:
#         return 'Negative'
#     else:
#         return 'Neutral'

# def fetch_and_process_tweets(max_tweets=100):
#     """
#     Fetches tweets based on the query, filters them, analyzes sentiment, and returns a DataFrame.
#     """
#     # Fetch tweets
#     tweets = client.search_recent_tweets(query=query, max_results=100, tweet_fields=['created_at', 'lang', 'text'])
    
#     # Check if tweets are found
#     if not tweets.data:
#         print("No tweets found.")
#         return pd.DataFrame()
    
#     # Create a DataFrame
#     df = pd.DataFrame([tweet.text for tweet in tweets.data], columns=['Tweet'])
    
#     # Apply filtering
#     df['IsFiltered'] = df['Tweet'].apply(filter_tweets)
#     df = df[df['IsFiltered'] == True].drop('IsFiltered', axis=1)
    
#     # Analyze sentiment
#     df['Sentiment'] = df['Tweet'].apply(analyze_sentiment)
    
#     # Add timestamp
#     df['Time_Collected'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     return df

# if __name__ == "__main__":
#     # Define output CSV file
#     output_file = 'solana_tweets_sentiment.csv'
    
#     # Check if CSV file exists; if not, create it with headers
#     if not os.path.exists(output_file):
#         with open(output_file, "w", newline='', encoding='utf-8') as file:
#             writer = pd.DataFrame(columns=["Tweet", "Sentiment", "Time_Collected"]).to_csv(file, index=False)
    
#     # Fetch and process tweets
#     df_tweets = fetch_and_process_tweets(max_tweets=100)
    
#     if not df_tweets.empty:
#         # Append to CSV
#         df_tweets.to_csv(output_file, mode='a', index=False, header=False)
#         print(f"Fetched and analyzed {len(df_tweets)} tweets.")
#         print(df_tweets)
#     else:
#         print("No new tweets to process.")
