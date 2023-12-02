# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# from datetime import datetime

# def TimePlot(dates, scores):
#     # Convert string dates to datetime objects
#     dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

#     plt.figure(figsize=(10, 6))
#     plt.plot(dates, scores)
#     plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#     plt.xlabel('Date')
#     plt.ylabel('Sentiment Score')
#     plt.title('Sentiment Over Time')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()

# def histPlot(scores, colors):
#     plt.figure(figsize=(8, 6))
#     for i, score_set in enumerate(scores):
#         plt.hist(score_set, bins=20, color=colors[i], edgecolor='black', alpha=0.5, label=f'Topic {i+1}')
#     plt.xlabel('Sentiment Score')
#     plt.ylabel('Frequency')
#     plt.title('Distribution of Sentiment Scores')
#     plt.legend()
#     plt.show()


# def barPlot(topics, avg_sentiments):
#     plt.figure(figsize=(8, 6))
#     plt.bar(topics, avg_sentiments, color='green')
#     plt.xlabel('Topics')
#     plt.ylabel('Average Sentiment Score')
#     plt.title('Average Sentiment Score by Topic')
#     plt.show()

# def main(dataSentiments, topics, reddit_sentiment_averages, youtube_sentiment_averages):
#     # Extract Reddit and YouTube sentiment scores for all topics
#     reddit_scores = [item['reddit_sentiments'] for item in dataSentiments]
#     youtube_scores = [item['youtube_sentiments'] for item in dataSentiments]
    
#     # Specify colors for each dataset
#     reddit_colors = ['blue', 'red', 'green']  # You can adjust these colors as needed
#     youtube_colors = ['purple', 'orange', 'cyan']  # You can adjust these colors as needed
    
#     # Plot histograms for Reddit and YouTube sentiment scores with respective colors
#     histPlot(reddit_scores, reddit_colors)
#     histPlot(youtube_scores, youtube_colors)
    
#     # Plot bar charts for average Reddit and YouTube sentiment scores
#     barPlot(topics, reddit_sentiment_averages)
#     barPlot(topics, youtube_sentiment_averages)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def TimePlot(dates, scores, title):
    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in dates]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, scores, marker='o')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xlabel('Date')
    plt.ylabel('Sentiment Score')
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
        reddit_avg = dataSentiments[i]['reddit_sentiment_average']

        if reddit_data:
            TimePlot(reddit_times, reddit_data, f'Reddit Sentiments Over Time for {topic}')
            histPlot(reddit_data, 'blue', f'Reddit Sentiment Distribution for {topic}')
        
        # YouTube Data Visualization
        youtube_data = dataSentiments[i]['youtube_sentiments']
        youtube_times = dataSentiments[i]['youtube_times']
        youtube_avg = dataSentiments[i]['youtube_sentiment_average']

        if youtube_data:
            TimePlot(youtube_times, youtube_data, f'YouTube Sentiments Over Time for {topic}')
            histPlot(youtube_data, 'red', f'YouTube Sentiment Distribution for {topic}')

    # Plot Average Sentiments Bar Chart
    reddit_avg_scores = [data['reddit_sentiment_average'] for data in dataSentiments]
    youtube_avg_scores = [data['youtube_sentiment_average'] for data in dataSentiments]

    barPlot(topics, reddit_avg_scores, 'Average Reddit Sentiment Scores by Topic')
    barPlot(topics, youtube_avg_scores, 'Average YouTube Sentiment Scores by Topic')
