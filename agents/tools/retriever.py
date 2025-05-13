from langchain.schema import HumanMessage
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from crewai.tools import tool
from langchain_community.chat_models import ChatOllama
from langchain.embeddings import HuggingFaceEmbeddings

custom_llm = ChatOllama(model="ollama/mistral")

@tool("RetrieverQuery")
def query_portfolio_knowledge(query: str) -> str:
    """
    Queries the FAISS index with a semantic prompt and returns relevant chunks.
    TODO: store previous data using metadata for example date/month/year to give quantitative analysis
    """

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local("vector_store/portfolio_index", embedding_model)
    # db = FAISS.load_local("vector_store/portfolio_index", OpenAIEmbeddings())
    results = db.similarity_search(query, k=5)
    context = "\n\n".join([doc.page_content for doc in results])
    prompt = (
        f"You are a financial assistant and answer relative to past outcomes, present situations and future predictions. Based on the following context, answer the user's query:\n\n"
        f"Context:\n{context}\n\n"
        f"User's Question: {query}"
    )
    response = custom_llm([HumanMessage(content=prompt)])

    return response.content
