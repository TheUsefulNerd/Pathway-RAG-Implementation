import requests
import json
import os
import time
from config import NEWS_PATH

API_KEY = '1eec0f64bc8a415280c5c8e14d3ae846'  # Replace with your API Key

class NewsIngestion:
    def __init__(self):
        self.api_url = "https://newsapi.org/v2/everything"
        self.params = {
            "q": "stock OR market OR finance",  # Searching for finance-related news
            "language": "en",
            "apiKey": API_KEY
        }

    def fetch_news_from_api(self):
        """
        Fetch news data from the API and return the parsed JSON.
        """
        try:
            response = requests.get(self.api_url, params=self.params)
            response.raise_for_status()  # Automatically raise an exception for bad status
            return response.json().get("articles", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return []

    def process_news(self, news_data):
        """
        Process fetched news data into a list of dictionaries (JSON).
        """
        processed_news = []
        for article in news_data:
            try:
                # Parse the datetime string into a Python datetime object
                published_at = article["publishedAt"]
                
                # Create a news article as a dictionary
                processed_article = {
                    "title": article["title"],
                    "summary": article.get("description", ""),
                    "published_at": published_at
                }
                processed_news.append(processed_article)
            except ValueError as e:
                print(f"Error parsing datetime: {e}")
                continue
        return processed_news

    def save_news_to_file(self, news_data):
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(NEWS_PATH), exist_ok=True)  # create the directory if it doesn't exist

            # Save the data to the file
            with open(NEWS_PATH, 'w', encoding='utf-8') as f:
                json.dump(news_data, f, ensure_ascii=False, indent=4)
            print(f"News data saved to {NEWS_PATH}")
        except Exception as e:
            print(f"Error saving news data to file: {e}")

    def fetch_and_store_news(self):
        """
        Fetch and store news data as a list of dictionaries (JSON).
        """
        news_data = self.fetch_news_from_api()
        if news_data:
            processed_news = self.process_news(news_data)
            self.save_news_to_file(processed_news)  # Save data to the file
            return processed_news
        else:
            return []

    def start_streaming(self, interval=60):
        """
        Continuously fetch news at a specified interval.
        """
        while True:
            news_data = self.fetch_and_store_news()
            if news_data:
                print(f"Fetched {len(news_data)} articles.")
            else:
                print("No new articles to fetch.")
            time.sleep(interval)

# Create the NewsIngestion instance
news_ingestor = NewsIngestion()

if __name__ == "__main__":
    news_ingestor.start_streaming()  # Start the streaming process
