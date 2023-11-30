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
auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
twitter = tweepy.API(auth)

youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)

# Function to perform sentiment analysis
def sentiment_analysis(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Function to fetch and analyze data from Reddit
def fetch_reddit_data(topic):
    posts = []
    for submission in reddit.subreddit("all").search(topic, limit=10):
        post_data = {
            'title': submission.title,
            'score': submission.score,
            'date': str(submission.created_utc),
            'sentiment': sentiment_analysis(submission.title)
        }
        posts.append(post_data)
    return posts

# Function to fetch and analyze data from Twitter
def fetch_twitter_data(topic):
    tweets = []
    for tweet in tweepy.Cursor(twitter.search, q=topic, lang="en", result_type="recent").items(10):
        tweet_data = {
            'text': tweet.text,
            'favorites': tweet.favorite_count,
            'date': str(tweet.created_at),
            'sentiment': sentiment_analysis(tweet.text)
        }
        tweets.append(tweet_data)
    return tweets

# Function to fetch and analyze data from YouTube
def fetch_youtube_data(topic):
    videos = []
    request = youtube.search().list(q=topic, part="snippet", type="video", maxResults=10)
    response = request.execute()

    for item in response['items']:
        video_data = {
            'title': item['snippet']['title'],
            'date': item['snippet']['publishedAt'],
            # Sentiment analysis on video titles as a proxy
            'sentiment': sentiment_analysis(item['snippet']['title'])
        }
        videos.append(video_data)
    return videos

def main(topicName):
    topic = topicName
    reddit_data = fetch_reddit_data(topic)
    twitter_data = fetch_twitter_data(topic)
    youtube_data = fetch_youtube_data(topic)
    return reddit_data, twitter_data, youtube_data

# Example usage
if __name__ == "__main__":
    topicName = input("Enter a topic to analyze: ")
    data = main(topicName)
    print(data)
