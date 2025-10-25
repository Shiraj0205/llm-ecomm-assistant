import os
from langchain_astradb import AstraDBVectorStore
from typing import List
from langchain_core.documents import Document
from utils.model_loader import ModelLoader
from utils.config_loader import load_config
from dotenv import load_dotenv

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter
from evaluation.ragas_eval import evaluate_context_precision, evaluate_response_relevancy

class Retriever:
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
            ## Maximal Marginal Relevance (MMR) Retriever
            mmr_retriever = self.vector_store.as_retriever(
                search_type="mmr", 
                search_kwargs={
                    "k": top_k,
                    "fetch_k": 20,
                    "lambda_mult": 0.7,
                    "score_threshold": 0.6
                    })
            
            ## Alternative: Similarity Search Retriever
            # retriever = self.vector_store.as_retriever(
            #     search_type="similarity",
            #     search_kwargs={"k": top_k}
            # )

            print("Retriever loaded successfully.")

            # Advanced: Contextual Compression Retriever
            # llm = self.model.load_llm()
            # compressor = LLMChainFilter.from_llm(llm=llm, threshold=0.5)

            # self.retriever = ContextualCompressionRetriever(
            #     base_compressor=compressor,
            #     base_retriever=mmr_retriever
            # )

            #return self.retriever

            return mmr_retriever

    def call_retriever(self, user_query: str) -> List[Document]:
        """
        Call the retriever with a query."""
        retriever = self.load_retriever()
        results = retriever.invoke(user_query)
        return results


if __name__ == "__main__":
    retriever = Retriever()
    #user_query = "What are the best products for outdoor activities?"
    user_query = "Can you suggest good budget iPhone under 1,00,00 INR?"
    #user_query = "What is the price of Apple watch 10?"

    # Mock Response to test evaluation
    mock_response = "Iphone 16 plus, iphone 16, iphone 15 are best phones under 1,00,000 INR."

    retriever.load_retriever()
    results = retriever.call_retriever(user_query)


    # def _format_docs(docs) -> str:
    #     if not docs:
    #         return "No relevant documents found."
    #     formatted_chunks = []
    #     for d in docs:
    #         meta = d.metadata or {}
    #         formatted = (
    #             f"Title: {meta.get('product_title', 'N/A')}\n"
    #             f"Price: {meta.get('price', 'N/A')}\n"
    #             f"Rating: {meta.get('rating', 'N/A')}\n"
    #             f"Reviews:\n{d.page_content.strip()}"
    #         )
    #         formatted_chunks.append(formatted)
    #     return "\n\n---\n\n".join(formatted_chunks)

    retrieved_contexts = [doc.page_content for doc in results]

    context_score = evaluate_context_precision(user_query, mock_response, retrieved_contexts)
    relevancy_score = evaluate_response_relevancy(user_query, mock_response, retrieved_contexts)

    # print("Evaluating retrieved contexts...")
    # context_precision = context_score(user_query, "Sample response", retrieved_contexts)
    # relevancy = relevancy_score(user_query, "Sample response", retrieved_contexts)

    print(f"Context Precision Score: {context_score}")
    print(f"Relevancy Score: {relevancy_score}")


    print(retrieved_contexts)