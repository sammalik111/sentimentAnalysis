import praw
import tweepy
import googleapiclient.discovery
from textblob import TextBlob
import config  # Importing the config file

# Initialize API clients using credentials from config.py
reddit = praw.Reddit(client_id=config.REDDIT_CLIENT_ID,
                     client_secret=config.REDDIT_CLIENT_SECRET,
                     user_agent=config.REDDIT_USER_AGENT)

auth = tweepy.OAuthHandler(config.TWITTER_API_KEY, config.TWITTER_API_SECRET_KEY)
auth.set_access_token(config.TWITTER_BEARER_TOKEN, config.TWITTER_BEARER_TOKEN)
twitter = tweepy.API(auth)

youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)

# Rest of the script remains the same...
