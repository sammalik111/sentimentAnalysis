import topicAnalysis

def main():
    # Ask the user to input their three favorite topics
    topics = []
    data = []
    for i in range(1, 4):
        topic = input(f"Enter favorite topic {i}: ")
        topics.append(topic)

    # Basic Analysis: Just print the topics and their lengths
    print("\nYour Favorite Topics:")
    for topic in topics:
        dataForATopic = topicAnalysis.main(topic)
        data.append(dataForATopic)
        print(f"- {topic} (Length: {len(topic)} characters)")
        print(data)

    # Add more analysis as needed

if __name__ == "__main__":
    main()
