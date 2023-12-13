import grabData
import visualize

def calculate_sentiments_and_times(data):
    # Function to extract sentiment scores and corresponding times from data
    sentiment_time_pairs = []  # List to store pairs of sentiments and times

    for item in data:
        sentiment_time_pairs.append((item['comments_sentiment'], item['date']))

    # Sort the pairs by time
    sentiment_time_pairs.sort(key=lambda pair: pair[1])

    # Unzip the pairs into separate lists
    sentiments, times = zip(*sentiment_time_pairs)

    return list(sentiments), list(times)


def main():
    topics = ['Trump', 'Kanye', 'Bitcoin']

    dataForTopics = []

    # Gather data for each topic
    for topic in topics:
        dataForEachTopic = grabData.main(topic)  # Fetch data from Reddit and YouTube
        dataForTopics.append(dataForEachTopic)

    dataSentiments = []  # List to store sentiment data for all topics

    # Process each topic's data
    for i, topic_data in enumerate(dataForTopics, start=1):
        reddit_data, youtube_data, twitter_data = topic_data

        # Calculate sentiments and times for Reddit and YouTube data
        reddit_sentiments, reddit_sentiment_times = calculate_sentiments_and_times(reddit_data)
        youtube_sentiments, youtube_sentiment_times = calculate_sentiments_and_times(youtube_data)
        twitter_sentiments, twitter_sentiment_times = calculate_sentiments_and_times(twitter_data)

        # Calculate and store the average sentiment for each platform
        reddit_sentiment_average = sum(reddit_sentiments) / len(reddit_sentiments) if reddit_sentiments else 0
        youtube_sentiment_average = sum(youtube_sentiments) / len(youtube_sentiments) if youtube_sentiments else 0
        twitter_sentiment_average = sum(twitter_sentiments) / len(twitter_sentiments) if twitter_sentiments else 0

        # Aggregate sentiment data and times for visualization
        dataSentiments.append({
            'topic': topics[i - 1],
            'reddit_sentiments': reddit_sentiments,
            'reddit_sentiment_average': reddit_sentiment_average,
            'reddit_times': reddit_sentiment_times,
            'youtube_sentiments': youtube_sentiments,
            'youtube_sentiment_average': youtube_sentiment_average,
            'youtube_times': youtube_sentiment_times,
            'twitter_sentiments': twitter_sentiments,
            'twitter_sentiment_average': twitter_sentiment_average,
            'twitter_times': twitter_sentiment_times,
        })

    # Visualize the gathered data
    visualize.main(dataSentiments, topics)
    # print("done")

if __name__ == "__main__":
    main()
