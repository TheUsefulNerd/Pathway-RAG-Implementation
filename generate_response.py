from query_retrieval import news_retriever  # ✅ Import news_retriever
from pathway.xpacks.llm.llms import LiteLLMChat  # Using LiteLLMChat for a smaller model
import os

class NewsResponseGenerator:
    def __init__(self, news_retriever):
        # Initialize the LiteLLMChat model (smaller and more lightweight than larger models)
        self.llm = LiteLLMChat(model="gemini/gemini-pro", api_key=os.getenv("GEMINI_API_KEY"))
        self.retriever = news_retriever

    def generate_response(self, query):
        # Retrieve relevant news articles based on the query
        retrieved_articles = self.retriever.retrieve_news(query)
        
        # Format the retrieved articles into a readable string
        formatted_articles = "\n".join([f"Title: {article['text']}" for article in retrieved_articles])
        
        # Generate the prompt for the LLM
        prompt = f"Summarize the key market insights from these articles:\n{formatted_articles}"

        # Get the response from the model
        response = self.llm(prompt)
        return response

# ✅ Ensure news_retriever is passed correctly
news_response_gen = NewsResponseGenerator(news_retriever)

# Example usage
if __name__ == "__main__":
    query = "What is the latest in AI and finance?"
    response = news_response_gen.generate_response(query)
    print(response)
