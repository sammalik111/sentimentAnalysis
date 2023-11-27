import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def TimePlot(dates, scores):
    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, scores)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xlabel('Date')
    plt.ylabel('Sentiment Score')
    plt.title('Sentiment Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def histPlot(scores):
    plt.figure(figsize=(8, 6))
    plt.hist(scores, bins=20, color='blue', edgecolor='black')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Frequency')
    plt.title('Distribution of Sentiment Scores')
    plt.show()

def barPlot(topics, avg_sentiments):
    plt.figure(figsize=(8, 6))
    plt.bar(topics, avg_sentiments, color='green')
    plt.xlabel('Topics')
    plt.ylabel('Average Sentiment Score')
    plt.title('Average Sentiment Score by Topic')
    plt.show()

def main():
    # Example data
    data = ['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-04']
    sentiment_scores = [0.1, 0.2, 0.3, 0.4]
    topics = ['Topic1', 'Topic2', 'Topic3']
    average_sentiments = [0.1, 0.2, 0.3]
    
    # Example usage
    for i in range(3):
        if i == 0:
            TimePlot(data, sentiment_scores)
        elif i == 1:
            histPlot(sentiment_scores)
        elif i == 2:
            barPlot(topics, average_sentiments)

main()
