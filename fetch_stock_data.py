import os
import yfinance as yf
import pandas as pd
import time
from config import DATA_PATH

def fetch_stock_data(ticker, interval="1m", duration=2):
    """Fetch real-time stock data for the given ticker and save to CSV."""
    
    # Ensure directory exists
    directory = os.path.dirname(DATA_PATH)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    print(f"📥 Fetching stock data for {ticker}...")

    end_time = time.time() + (duration * 60)  # Run for 'duration' minutes

    while time.time() < end_time:
        try:
            # Fetch stock data for the last 7 days with the given interval
            df = yf.download(ticker, period="7d", interval=interval)
            if df.empty:
                raise ValueError("No data retrieved from Yahoo Finance.")

            # Reset index to make 'Datetime' a column
            df.reset_index(inplace=True)

            # Rename columns correctly
            df.rename(columns={"Datetime": "timestamp", "Date": "timestamp"}, inplace=True)


            # Convert timestamp to string (Fix for Pathway)
            df["timestamp"] = df["timestamp"].astype(str)

            print(df.head())  # Debugging: Show sample data
            
            # Save to CSV (overwrite, no blank rows)
            df.to_csv(DATA_PATH, index=False, mode="w", encoding="utf-8")


            print(f"✅ Data saved for {ticker} at {DATA_PATH}")
            return  # Exit after successful fetch

        except Exception as e:
            print(f"❌ Error fetching stock data: {e}")
            time.sleep(10)  # Retry after 10 seconds if fetching fails