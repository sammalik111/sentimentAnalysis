import praw
import tweepy
import googleapiclient.discovery
from textblob import TextBlob
import config  # Importing the config file
import datetime
import requests

# Initialize API clients using credentials from config.py
reddit = praw.Reddit(client_id=config.REDDIT_CLIENT_ID,
                     client_secret=config.REDDIT_CLIENT_SECRET,
                     user_agent=config.REDDIT_USER_AGENT)


youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)


# Function to perform sentiment analysis
def sentiment_analysis(text):
    analysis = TextBlob(text)  
    # Map sentiment score from -1 to 1 to a 0-100 scale
    sentiment_score = (analysis.sentiment.polarity)
    return sentiment_score

# Function to fetch and analyze data from Reddit
def fetch_reddit_data(topic):
    posts = []
    for submission in reddit.subreddit("all").search(topic, limit=20):
        post_data = {
            'title': submission.title,
            'upvotes': submission.score,
            # Convert to readable date-time format
            'date': datetime.datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            'sentiment': sentiment_analysis(submission.title),
            'comments_sentiment': 0,  # Placeholder for now
        }
        
        # Analyze sentiment of the first 100 comments
        submission.comments.replace_more(limit=0)  # Ensure all comments are loaded
        comment_sentiments = [sentiment_analysis(comment.body) for comment in submission.comments[:20]]
        post_data['comments_sentiment'] = sum(comment_sentiments) / max(len(comment_sentiments), 1)
        
        posts.append(post_data)
    return posts

# Function to fetch and analyze data from YouTube
def fetch_youtube_data(topic):
    videos = []
    request = youtube.search().list(q=topic, part="snippet", type="video", maxResults=20)
    response = request.execute()

    for item in response['items']:
        # Convert YouTube date format to match Reddit's format
        youtube_date = item['snippet'].get('publishedAt', 'Unknown date')
        formatted_date = datetime.datetime.fromisoformat(youtube_date.rstrip('Z')).strftime('%Y-%m-%d %H:%M:%S')

        video_data = {
            'title': item['snippet']['title'],
            'date': formatted_date,
            'sentiment': sentiment_analysis(item['snippet']['title']),
            'comments_sentiment': 0,  # Default value
        }
        
        video_id = item['id']['videoId']

        try:
            # Attempt to fetch comments for the video
            comments_response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=20  # Adjustable number of comments
            ).execute()

            # Check if comments are fetched successfully
            if 'items' in comments_response and comments_response['items']:
                # Create a list of sentiment scores for each comments
                comment_sentiments = [sentiment_analysis(comment['snippet']['topLevelComment']['snippet']['textDisplay']) for comment in comments_response['items']]
                if comment_sentiments:
                    video_data['comments_sentiment'] = sum(comment_sentiments) / len(comment_sentiments)

        except Exception as e:
            # Handle exceptions (e.g., comments are disabled)
            print(f"Error fetching comments for video {video_id}: {e}")

        videos.append(video_data)
    return videos

def fetch_twitter_data(topic):
    base_url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {
        "Authorization": f"Bearer {config.TWITTER_BEARER_TOKEN}",
    }
    params = {
        "query": topic,
        "tweet.fields": "text,created_at",
        "max_results": 20,
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            tweets = []

            for tweet in data.get("data", []):
                tweet_data = {
                    'text': tweet["text"],
                    'date': datetime.datetime.fromisoformat(tweet["created_at"]).strftime('%Y-%m-%d %H:%M:%S'),
                    'sentiment': sentiment_analysis(tweet["text"]),  
                    'comments_sentiment': 0,  # Default value
                }
                # Fetch mentions of this tweet by its ID
                tweet_id = tweet["id"]
                mentions_url = f"https://api.twitter.com/2/tweets/{tweet_id}/mentions"
                mentions_response = requests.get(mentions_url, headers=headers, params={"max_results": 20})

                if mentions_response.status_code == 200:
                    mentions_data = mentions_response.json()
                    reply_sum = 0
                    reply_count = len(mentions_data.get("data", []))
                    
                    for mention in mentions_data.get("data", []):
                        reply_sum += sentiment_analysis(mention["text"])
                    
                    if reply_count > 0:
                        tweet_data['comments_sentiment'] = reply_sum / reply_count

                tweets.append(tweet_data)

            return tweets
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")
            return []

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    

def main(topicName):
    topic = topicName
    twitter_data = fetch_twitter_data(topic)
    reddit_data = fetch_reddit_data(topic)
    youtube_data = fetch_youtube_data(topic)
    
    dataForthisTopic = [reddit_data, youtube_data, twitter_data]
    return dataForthisTopic
