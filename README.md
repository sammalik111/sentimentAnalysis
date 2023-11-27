# Sentiment Analysis Tool

## Overview
This tool performs sentiment analysis on social media posts from Reddit, Twitter, and YouTube. It's designed to help in identifying emerging trends and monitoring brand reputation by analyzing posts and tweets relevant to specified topics.

## Features
- **Data Retrieval**: Fetch posts and tweets from Reddit, Twitter, and YouTube APIs based on key topics.
- **Sentiment Analysis**: Apply sentiment analysis to determine the sentiment of each post and tweet. Optionally uses Michael Reeve's sentiment analysis model.
- **Popularity Metrics**: Extracts and records the popularity of each post and tweet.
- **Timestamps**: Captures the date and time of each post and tweet.

## Getting Started

### Prerequisites
- Python 3.x
- PRAW (Python Reddit API Wrapper)
- Tweepy (Twitter for Python)
- Google API Python Client
- TextBlob

### Installation
Clone the repository and install the required packages:
```bash
git clone [repository-url]
cd [repository-name]
pip install praw tweepy google-api-python-client textblob
