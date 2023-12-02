import grabData
import visualize

def calculate_sentiments_and_times(data):
    # Function to extract sentiment scores and corresponding times from data
    sentiments = []  # List to store individual sentiments
    times = []  # List to store times of sentiments

    for item in data:
        sentiments.append(item['comments_sentiment'])  # Append sentiment score
        times.append(item['date'])  # Append times of each comment
    
    return sentiments, times

def main():
    topics = ['kanye', 'kittens', 'Murder']

    dataForTopics = []

    # Gather data for each topic
    for topic in topics:
        dataForEachTopic = grabData.main(topic)  # Fetch data from Reddit and YouTube
        dataForTopics.append(dataForEachTopic)

    dataSentiments = []  # List to store sentiment data for all topics

    # Process each topic's data
    for i, topic_data in enumerate(dataForTopics, start=1):
        reddit_data, youtube_data = topic_data

        # Calculate sentiments and times for Reddit and YouTube data
        reddit_sentiments, reddit_sentiment_times = calculate_sentiments_and_times(reddit_data)
        youtube_sentiments, youtube_sentiment_times = calculate_sentiments_and_times(youtube_data)

        # Calculate and store the average sentiment for each platform
        reddit_sentiment_average = sum(reddit_sentiments) / len(reddit_sentiments) if reddit_sentiments else 0
        youtube_sentiment_average = sum(youtube_sentiments) / len(youtube_sentiments) if youtube_sentiments else 0

        # Aggregate sentiment data and times for visualization
        dataSentiments.append({
            'topic': topics[i - 1],
            'reddit_sentiments': reddit_sentiments,
            'youtube_sentiments': youtube_sentiments,
            'reddit_times': reddit_sentiment_times,
            'youtube_times': youtube_sentiment_times, 
            'reddit_sentiment_average': reddit_sentiment_average,
            'youtube_sentiment_average': youtube_sentiment_average,
        })

    # Visualize the gathered data
    visualize.main(dataSentiments, topics)
    print("done")

if __name__ == "__main__":
    main()
