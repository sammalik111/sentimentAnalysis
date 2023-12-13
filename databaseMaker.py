import sqlite3


# Function to fetch data from the database for a specific topic and API
def fetch_data_from_database(topic, api_name):
    conn = sqlite3.connect('database.db')  # Replace 'your_database.db' with your database file name
    cursor = conn.cursor()

    # Form the table name based on the topic and API name
    table_name = f"{topic}_{api_name}"

    # Fetch data from the specified table
    cursor.execute(f'SELECT title, upvotes, date, sentiment, comments_sentiment FROM {table_name}')
    rows = cursor.fetchall()

    # Convert the fetched data into a list of dictionaries
    data = []
    for row in rows:
        item = {
            'title': row[0],
            'upvotes': row[1],
            'date': row[2],
            'sentiment': row[3],
            'comments_sentiment': row[4]
        }
        data.append(item)

    conn.close()
    
    return data


# Function to create and insert data into a table
def create_and_insert_table(data, topic, api_name):
    conn = sqlite3.connect('database.db')  # Replace 'your_database.db' with your desired database file name
    cursor = conn.cursor()

    # Create a table for the topic and API if it doesn't exist
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {topic}_{api_name} (
            title TEXT PRIMARY KEY,  -- Unique constraint on title
            upvotes INTEGER,
            date TEXT,
            sentiment REAL,
            comments_sentiment REAL
        )
    '''
    cursor.execute(create_table_query)

    # Insert data into the table, ignoring duplicates
    for item in data:
        try:
            cursor.execute(f'''
                INSERT OR IGNORE INTO {topic}_{api_name} (title, upvotes, date, sentiment, comments_sentiment)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                item['title'],
                item['upvotes'],
                item['date'],
                item['sentiment'],
                item['comments_sentiment']
            ))
        except sqlite3.IntegrityError as e:
            # Handle any potential integrity errors (e.g., duplicate title)
            print(f"Integrity error: {e}")

    conn.commit()
    conn.close()

def main(topics, dataForTopics):
    # Assuming dataForTopics is a list of dictionaries for each topic, where each topic contains Reddit, Twitter, and YouTube data
        
    for i, topic in enumerate(topics):
        reddit_data = dataForTopics[i][0]
        youtube_data = dataForTopics[i][1]
        twitter_data = dataForTopics[i][2]

        create_and_insert_table(reddit_data, topic, 'reddit')
        create_and_insert_table(twitter_data, topic, 'twitter')
        create_and_insert_table(youtube_data, topic, 'youtube')
