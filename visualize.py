import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

def amplify_variation(scores, base=10):
    # Normalize scores to range -1 to 1
    min_score, max_score = min(scores), max(scores)
    normalized_scores = [(2 * (score - min_score) / (max_score - min_score) - 1) for score in scores]
    
    # Apply logarithmic transformation
    amplified_scores = [np.log(score + 1) / np.log(base + 1) * 100 for score in normalized_scores]    
    return amplified_scores


def TimePlot(dates, scores, title):
    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in dates]

    # Amplify variations in scores
    amplified_scores = amplify_variation(scores)

    plt.figure(figsize=(10, 6))
    plt.plot(dates, amplified_scores, marker='o')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xlabel('Date')
    plt.ylabel('Amplified Sentiment Score')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def histPlot(scores, color, title):
    plt.figure(figsize=(8, 6))
    plt.hist(scores, bins=20, color=color, edgecolor='black', alpha=0.7)
    plt.xlabel('Sentiment Score')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.show()

def barPlot(topics, avg_sentiments, title):
    plt.figure(figsize=(8, 6))
    plt.bar(topics, avg_sentiments, color='green')
    plt.xlabel('Topics')
    plt.ylabel('Average Sentiment Score')
    plt.title(title)
    plt.show()

def main(dataSentiments, topics):
    for i, topic in enumerate(topics):
        # Reddit Data Visualization
        reddit_data = dataSentiments[i]['reddit_sentiments']
        reddit_times = dataSentiments[i]['reddit_times']

        if reddit_data:
            TimePlot(reddit_times, reddit_data, f'Reddit Sentiments Over Time for {topic}')
            # histPlot(reddit_data, 'blue', f'Reddit Sentiment Distribution for {topic}')
        
        # YouTube Data Visualization
        youtube_data = dataSentiments[i]['youtube_sentiments']
        youtube_times = dataSentiments[i]['youtube_times']

        if youtube_data:
            TimePlot(youtube_times, youtube_data, f'YouTube Sentiments Over Time for {topic}')
            # histPlot(youtube_data, 'red', f'YouTube Sentiment Distribution for {topic}')
            
            
        # Twitter Data Visualization
        twitter_data = dataSentiments[i]['twitter_sentiments']
        twitter_times = dataSentiments[i]['twitter_times']

        if twitter_data:
            TimePlot(twitter_times, twitter_data, f'Twitter Sentiments Over Time for {topic}')
            # histPlot(youtube_data, 'red', f'YouTube Sentiment Distribution for {topic}')


    # Plot Average Sentiments Bar Chart
    reddit_avg_scores = [data['reddit_sentiment_average'] for data in dataSentiments]
    youtube_avg_scores = [data['youtube_sentiment_average'] for data in dataSentiments]
    twitter_avg_scores = [data['twitter_sentiment_average'] for data in dataSentiments]

    barPlot(topics, reddit_avg_scores, 'Average Reddit Sentiment Scores by Topic')
    barPlot(topics, youtube_avg_scores, 'Average YouTube Sentiment Scores by Topic')
    barPlot(topics, twitter_avg_scores, 'Average Twitter Sentiment Scores by Topic')
