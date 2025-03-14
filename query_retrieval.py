import json
import pathway as pw
import os
from pathway.xpacks.llm.splitters import TokenCountSplitter
from pathway.xpacks.llm.embedders import GeminiEmbedder  # Import GeminiEmbedder
from pathway.stdlib.indexing import BruteForceKnnFactory
from pathway.stdlib.indexing import TantivyBM25Factory
from config import NEWS_PATH
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class NewsRetriever:
    def __init__(self):
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("API key for Gemini not found in environment variables")
            
        # Initialize splitter and embedder
        self.splitter = TokenCountSplitter(min_tokens=50, max_tokens=300)
        self.embedder = GeminiEmbedder(model="models/text-embedding-004", api_key=gemini_api_key)
        
        # Load news data
        with open(NEWS_PATH, 'r', encoding='utf-8') as file:
            self.news_data = json.load(file)
        
        # Process articles
        self.documents = []
        for article in self.news_data:
            text = f"{article['title']} {article['summary']}"
            text_chunks = self.splitter(text)
            
            for chunk in text_chunks:
                embedding = self.embedder.embed(chunk)  # Generate embeddings for each chunk
                self.documents.append({
                    "text": chunk,
                    "embedding": embedding
                })
        
        # Initialize search indices
        self.bm25_index = TantivyBM25Factory(self.documents, column="text")
        self.knn_index = BruteForceKnnFactory(self.documents, column="embedding")

    def retrieve_news(self, query):
        query_embedding = self.embedder.embed(query)
        knn_results = self.knn_index.search(query_embedding, k=5)
        bm25_results = self.bm25_index.search(query, k=5)
        
        combined_results = {res['text']: res for res in knn_results + bm25_results}
        return list(combined_results.values())


# Example usage
news_retriever = NewsRetriever()

# Query example
query = "What is the latest in AI and finance?"
retrieved_articles = news_retriever.retrieve_news(query)

# Print the retrieved articles
for article in retrieved_articles:
    print(f"Title: {article['text']}")
    print(f"Similarity score: {article.get('score', 'N/A')}")
    print("-" * 80)
