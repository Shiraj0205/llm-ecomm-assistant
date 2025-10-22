import os
from langchain_astradb import AstraDBVectorStore
from typing import List
from langchain_core.documents import Document
from utils.model_loader import ModelLoader
from utils.config_loader import load_config
from dotenv import load_dotenv


class RetrieverClass:
    """
    Retriever class to handle document retrieval from AstraDB using vector embeddings.
    """

    def __init__(self):
        """
        Initialize the Retriever with a data source."""
        self.model = ModelLoader()
        self.config = load_config()
        self._load_env_variables()
        self.vector_store = None
        self.retriever = None

    def _load_env_variables(self):
        """
        Load and validate required environment variables."""
        load_dotenv()
        required_vars = ["GOOGLE_API_KEY", "ASTRA_DB_API_ENDPOINT", "ASTRA_DB_APPLICATION_TOKEN", "ASTRA_DB_KEYSPACE"]
        missing_vars = [var for var in required_vars if os.getenv(var) is None]

        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")
        
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.db_api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
        self.db_application_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        self.db_keyspace = os.getenv("ASTRA_DB_KEYSPACE")

    def load_retriever(self):
        """
        Load and initialize the retriever component."""
        if not self.vector_store:
            collection_name = self.config["astra_db"]["collection_name"]
            self.vector_store = AstraDBVectorStore(
                embedding=self.model.load_embeddings(),
                collection_name=collection_name,
                api_endpoint=self.db_api_endpoint,
                token=self.db_application_token,
                namespace=self.db_keyspace
            )
        
        top_k = self.config["retriever"]["top_k"] if "retriever" in self.config else 5
        if not self.retriever:
            retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": top_k})
            print("Retriever loaded successfully.")
            return retriever

    def call_retriever(self, user_query: str) -> List[Document]:
        """
        Call the retriever with a query."""
        retriever = self.load_retriever()
        results = retriever.invoke(user_query)
        return results


if __name__ == "__main__":
    retriever = RetrieverClass()
    #user_query = "What are the best products for outdoor activities?"
    user_query = "Can you suggest good budget iPhone under 1,00,00 INR?"
    retriever.load_retriever()
    results = retriever.call_retriever(user_query)
    print(results)