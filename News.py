import streamlit as st
import os
from generate_response import NewsResponseGenerator  # Ensure this imports NewsResponseGenerator
from query_retrieval import news_retriever  # Ensure this imports news_retriever correctly
from config import NEWS_PATH

# Initialize the NewsIngestion and NewsResponseGenerator
news_ingestion = news_retriever()  # This handles fetching and storing the news
news_response_gen = NewsResponseGenerator(news_ingestion)

def show_news():
    st.title("📰 Global Financial News")

    # Button to fetch the latest finance news
    if st.button("Fetch Latest Finance News"):
        with st.spinner("Fetching latest finance news..."):
            # Fetch the latest news and store it
            news_data = news_ingestion.fetch_and_store_news()
        
        if news_data:
            st.success(f"✅ Fetched {len(news_data)} articles.")
            for article in news_data:
                # Display each article's title and details
                st.markdown(f"### 📰 {article['title']}")
                st.write(f"**🕒 Published:** {article['published_at']}")
                st.write(f"**📢 Summary:** {article['summary']}")
                st.markdown("---")
        else:
            st.error("❌ Failed to fetch news!")

    # Search for relevant news articles based on user query
    st.subheader("🔍 Search for Relevant News")
    query = st.text_input("Enter a query to find relevant articles:")
    
    # Button to find relevant articles
    if st.button("Find Relevant News"):
        if not os.path.exists(NEWS_PATH):
            st.error("❌ News data not found! Fetch news first.")
        else:
            with st.spinner("Finding relevant articles..."):
                # Use the generate_response method to get a response based on the query
                response = news_response_gen.generate_response(query)
            
            if response:
                st.success("✅ Found relevant news!")
                st.write(response)
            else:
                st.error("❌ No relevant articles found!")

