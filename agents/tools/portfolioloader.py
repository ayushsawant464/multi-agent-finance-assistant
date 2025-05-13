
import json
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from crewai.tools import tool
from langchain.embeddings import HuggingFaceEmbeddings

@tool("PortfolioIndexer")
def index_portfolio_data(_: str = None) -> str:
    """
    Loads and indexes portfolio.json into FAISS for retrieval.
    """
    with open("/path/to/portfolio.json", "r") as f:
        data = json.load(f)

    documents = []
    for item in data["portfolio"] + data["watchlist"]:
        doc_text = f"{item['name']} ({item['symbol']})\nSector: {item['sector']}\nQty: {item['quantity']}\nPrice: {item['average_buy_price']}"
        documents.append(Document(page_content=doc_text, metadata={"symbol": item["symbol"]}))
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    faiss_store = FAISS.from_documents(documents, embeddings)
    faiss_store.save_local("vector_store/portfolio_index")

    return "Portfolio data indexed successfully."
