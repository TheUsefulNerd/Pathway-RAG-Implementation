import streamlit as st
import pandas as pd
import os
import time
from fetch_stock_data import fetch_stock_data
from data_procesing import run_streaming
from config import OUTPUT_PATH, DATA_PATH

def show_home():
    st.title("📊 Real-Time Finance RAG System")
    
    ticker = st.text_input("Enter Stock Ticker:", value="AAPL")
    
    if st.button("Fetch & Process Data"):
        with st.spinner("Fetching latest stock data..."):
            fetch_stock_data(ticker)
        
        with st.spinner("Verifying stock data..."):
            for _ in range(15):  
                if os.path.exists(DATA_PATH) and os.stat(DATA_PATH).st_size > 0:
                    st.success("✅ Stock data saved!")
                    break
                time.sleep(2)
            else:
                st.error("❌ Data fetching failed!")
                st.stop()

        with st.spinner("Processing stock data..."):
            run_streaming()
        
        with st.spinner("Verifying processed data..."):
            for _ in range(15):
                if os.path.exists(OUTPUT_PATH) and os.stat(OUTPUT_PATH).st_size > 0:
                    st.success("✅ Data processing completed!")
                    break
                time.sleep(2)
            else:
                st.error("❌ Data processing failed!")
                st.stop()
        
        st.subheader("🔹 Processed Financial Data")
        try:
            df = pd.read_csv(OUTPUT_PATH)
            if df.empty:
                st.error("❌ Processed data is empty!")
            else:
                st.dataframe(df)
        except FileNotFoundError:
            st.error("❌ Processed data file not found!")