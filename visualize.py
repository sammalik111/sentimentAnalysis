import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

def save_data_to_text_file(filename, dataType, api, topic, data):
    with open(filename, 'a') as file:  # Use 'a' mode to append data
        # Add information about the API and topic at the beginning of the file
        file.write(f"{dataType} for {topic} using {api}\n")

        for item in data:
            file.write(f"{item}\n")
        file.write(f"------------\n")

def amplify_variation(scores, base=10):
    # Check if all scores are zeros
    if all(score == 0 for score in scores):
        return [0] * len(scores)  # Return a list of zeros

    # Normalize scores to range -1 to 1
    min_score, max_score = min(scores), max(scores)

    normalized_scores = []
    for score in scores:
        numerator = 2 * (score - min_score)
        denominator = (max_score - min_score)
        if denominator == 0:
            normalized_scores.append(-1)
        else:
            normalized_scores.append((numerator / denominator) - 1)

    # Apply logarithmic transformation with handling for -1
    amplified_scores = []
    for score in normalized_scores:
        if score == -1:
            amplified_scores.append(0)
        else:
            amplified_scores.append(np.log(score + 1) / np.log(base + 1) * 100)

    return amplified_scores

def TimePlot(dates, scores, title, save_to_file=None, api=None, topic=None):
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

    if save_to_file:
        save_data_to_text_file(save_to_file + '.txt', 'sentiments', api, topic, amplified_scores)  # Append data to a text file

def barPlot(topics, avg_sentiments, title, save_to_file=None, api=None, topic=None):
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    color_indices = np.arange(len(topics)) % len(colors)

    avg_sentiments = amplify_variation(avg_sentiments)

    plt.figure(figsize=(8, 6))
    # Plot each bar with a different color
    for i, (topic, sentiment) in enumerate(zip(topics, avg_sentiments)):
        color_index = color_indices[i]
        plt.bar(topic, sentiment, color=colors[color_index])
    plt.xlabel('Topics')
    plt.ylabel('Average Sentiment Score')
    plt.title(title)
    legend_labels = [plt.Rectangle((0, 0), 1, 1, color=colors[i]) for i in range(len(topics))]  # Create a legend with the colors
    plt.legend(legend_labels, topics)
    plt.show()

    if save_to_file:
        save_data_to_text_file(save_to_file + '.txt', 'averages', api, topic, avg_sentiments)  # Append data to a text file

def main(dataSentiments, topics):
    for i, topic in enumerate(topics):
        # Reddit Data Visualization
        reddit_data = dataSentiments[i]['reddit_sentiments']
        reddit_times = dataSentiments[i]['reddit_times']

        if reddit_data:
            TimePlot(reddit_times, reddit_data, f'Reddit Sentiments Over Time for {topic}', save_to_file='output', api='Reddit API', topic=topic)

        # YouTube Data Visualization
        youtube_data = dataSentiments[i]['youtube_sentiments']
        youtube_times = dataSentiments[i]['youtube_times']

        if youtube_data:
            TimePlot(youtube_times, youtube_data, f'YouTube Sentiments Over Time for {topic}', save_to_file='output', api='YouTube API', topic=topic)

        # Twitter Data Visualization
        twitter_data = dataSentiments[i]['twitter_sentiments']
        twitter_times = dataSentiments[i]['twitter_times']

        if twitter_data:
            TimePlot(twitter_times, twitter_data, f'Twitter Sentiments Over Time for {topic}', save_to_file='output', api='Twitter API', topic=topic)

    # Plot Average Sentiments Bar Chart
    reddit_avg_scores = [data['reddit_sentiment_average'] for data in dataSentiments]
    youtube_avg_scores = [data['youtube_sentiment_average'] for data in dataSentiments]
    twitter_avg_scores = [data['twitter_sentiment_average'] for data in dataSentiments]

    barPlot(topics, reddit_avg_scores, 'Average Reddit Sentiment Scores by Topic', save_to_file='output', api='Reddit API', topic='Average')
    barPlot(topics, youtube_avg_scores, 'Average YouTube Sentiment Scores by Topic', save_to_file='output', api='YouTube API', topic='Average')
    barPlot(topics, twitter_avg_scores, 'Average Twitter Sentiment Scores by Topic', save_to_file='output', api='Twitter API', topic='Average')
