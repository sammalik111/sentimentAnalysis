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

        video_id = item['id']['videoId']

        try:
            # Fetch video statistics to get the number of likes
            video_stats_response = youtube.videos().list(
                part="statistics",
                id=video_id
            ).execute()

            # Check if video statistics are fetched successfully
            if 'items' in video_stats_response and video_stats_response['items']:
                likes = int(video_stats_response['items'][0]['statistics'].get('likeCount', '0'))
            else:
                likes = 0

            video_data = {
                'title': item['snippet']['title'],
                'upvotes': likes,  # Set upvotes count to likes
                'date': formatted_date,
                'sentiment': sentiment_analysis(item['snippet']['title']),
                'comments_sentiment': 0,  # Default value
            }

            # Attempt to fetch comments for the video
            comments_response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=20  # Adjustable number of comments
            ).execute()

            # Check if comments are fetched successfully
            if 'items' in comments_response and comments_response['items']:
                # Create a list of sentiment scores for each comment
                comment_sentiments = [sentiment_analysis(comment['snippet']['topLevelComment']['snippet']['textDisplay']) for comment in comments_response['items']]
                if comment_sentiments:
                    video_data['comments_sentiment'] = sum(comment_sentiments) / len(comment_sentiments)
            
            if video_data['comments_sentiment'] != 0:
                videos.append(video_data)

        except Exception as e:
            # Handle exceptions (e.g., comments are disabled)
            print(f"Error fetching data for video {video_id}: {e}")

        
    return videos


def calculate_comments_sentiment(tweet_data):
    sentiment = tweet_data['sentiment']
    upvotes = tweet_data['public_metrics']['like_count']
    reply_count = tweet_data['public_metrics']['reply_count']
    possibly_sensitive = tweet_data.get('possibly_sensitive', False)
    withheld = tweet_data.get('withheld', False)

    # Adjusting the formula to handle cases where likes and replies might be zero
    # Adding a small constant (e.g., 1) to avoid division by zero and to ensure some weight is given to sentiment
    comments_sentiment = sentiment * (upvotes + 1) * (reply_count + 1)
    
    # Adjust the comments_sentiment based on sensitivity and withholding
    if possibly_sensitive:
        comments_sentiment *= 0.9  # Reduces sentiment for sensitive content
    if withheld:
        comments_sentiment *= 0.8  # Further reduces sentiment for withheld content

    return comments_sentiment


def fetch_twitter_data(topic):
    base_url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {
        "Authorization": f"Bearer {config.TWITTER_BEARER_TOKEN}",
    }
    params = {
        "query": topic,
        "tweet.fields": "text,created_at,public_metrics,possibly_sensitive",
        "expansions": "author_id",
        "user.fields": "public_metrics",  # If you need user metrics
        "max_results": 100,
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            tweets = []

            for tweet in data.get("data", []):
                tweet_data = {
                    'title': tweet["text"],
                    'upvotes': tweet["public_metrics"]["like_count"],
                    'date': datetime.datetime.fromisoformat(tweet["created_at"]).strftime('%Y-%m-%d %H:%M:%S'),
                    'sentiment': sentiment_analysis(tweet["text"]),  
                    'public_metrics': tweet.get('public_metrics', {}),
                    'possibly_sensitive': tweet.get('possibly_sensitive', False),
                    'withheld': tweet.get('withheld', False),
                    'comments_sentiment': 0,  # Placeholder for now
                }
                tweet_data['comments_sentiment'] = calculate_comments_sentiment(tweet_data)
                if tweet_data['comments_sentiment'] != 0:
                    tweets.append(tweet_data)

            # sort tweets by timestamp with oldest being first
            tweets.sort(key=lambda tweet: tweet['date'])
            
            # Calculate comments sentiment for each tweet
            for tweet in tweets:
                tweet['comments_sentiment'] = calculate_comments_sentiment(tweet)
 
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


