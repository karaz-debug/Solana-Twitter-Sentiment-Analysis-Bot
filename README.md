# Solana Twitter Sentiment Analysis Bot

## 🚀 Project Overview

The **Solana Twitter Sentiment Analysis Bot** is an automated system designed to collect, filter, and analyze real-time tweets related to Solana (SOL). Utilizing Python and libraries such as `twkit`, `httpx`, and `nltk`, this bot aims to provide valuable insights into market sentiment by processing and categorizing tweets as positive, negative, or neutral. This project is currently in development, with ongoing enhancements to improve functionality and accuracy.

## 🔍 Features

- **Data Acquisition:**
  - **Real-Time Tweet Fetching:** Continuously retrieves tweets containing the keyword "Solana" using the `twkit` client.
  - **API Integration:** Connects to Twitter APIs via the `httpx` library for efficient data retrieval.

- **Data Filtering:**
  - **Content Filtering:** Excludes tweets containing specific keywords such as "telegram," "discount," "promo," "sale," "join," and "t.co" to ensure relevance.
  - **Automated Ignoring:** Implements logic to automatically filter out unwanted tweets based on predefined criteria.

- **Sentiment Analysis:**
  - **NLP Processing:** Utilizes NLTK's VADER sentiment analyzer to assess the sentiment of each tweet.
  - **Categorization:** Classifies tweets into Positive, Negative, or Neutral based on sentiment scores.

- **Data Logging:**
  - **CSV Storage:** Logs filtered tweets and their sentiment scores into a CSV file (`tweets.csv`) for easy access and analysis.
  - **Comprehensive Details:** Records tweet count, username, text, creation time, retweet count, favorite count, and reply count.

- **Error Handling:**
  - **Rate Limiting:** Manages API rate limits and handles exceptions to ensure uninterrupted data collection.
  - **Robust Logging:** Implements error logging to track and address issues during execution.

## 📊 Backtest Results

*Currently, backtesting is not applicable as the project focuses on real-time sentiment analysis. Future developments will include correlating sentiment data with Solana's market performance.*

## 🛠 Installation

### Prerequisites

- **Python 3.9+**
- **Git:** [Download Git](https://git-scm.com/downloads)
- **Twitter Developer Account:** [Apply Here](https://developer.twitter.com/en/apply-for-access)
- **API Credentials:**
  - **Twitter API Key and Secret**
  - **Bearer Token**
