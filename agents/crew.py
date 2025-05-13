
import os
from crewai import Agent, Task, Crew, Process
from agents.tools.stockdatatool import fetch_stock_data
from agents.tools.secscrapertool import fetch_sec_filings
from agents.tools.portfolioloader import index_portfolio_data
from agents.tools.retriever import query_portfolio_knowledge

from langchain_community.chat_models import ChatOllama
custom_llm = ChatOllama(model="ollama/mistral")
def build_crew_with_query(user_query: str) -> Crew:
    market = Agent(
        role="Market Analyst",
        goal="Gather stock data for user's portfolio",
        backstory="You analyze real-time stock metrics and performance using Yahoo Finance.",
        tools=[fetch_stock_data],
        verbose=True,
        memory=True,
        llm=custom_llm,
            context={"file_path": "/path/to/portfolio.json"}
    )

    sec = Agent(
        role="SEC Filing Analyst",
        goal="Summarize 10-K/10-Q filings",
        backstory="You scrape and analyze regulatory filings for risk and outlook.",
        tools=[fetch_sec_filings],
        verbose=True,
        memory=True,
        llm=custom_llm,
            context={"file_path": "/path/to/portfolio.json"}


    )

    indexer = Agent(
        role="Retriever",
        goal="Index all insights into a vector database",
        backstory="You handle RAG by embedding financial data for semantic search.",
        tools=[index_portfolio_data],
        verbose=True,
        memory=True,
            llm=custom_llm

    )

    reporter = Agent(
        role="Portfolio Reporter",
        goal="Generate reports and answer queries",
        backstory="You provide insight by querying knowledge using LLMs and embeddings.",
        tools=[query_portfolio_knowledge],
        verbose=True,
        memory=True,
            llm=custom_llm

    )

    # Define tasks
    market_task = Task(description="Fetch stock market data.", expected_output="Stock summaries", agent=market)
    sec_task = Task(description="Scrape and summarize SEC filings.", expected_output="SEC summaries", agent=sec)
    index_task = Task(description="Index all data for retrieval.", expected_output="Index complete", agent=indexer)
    report_task = Task(description="Answer user query or write a report.", expected_output="Final report", agent=reporter)

    return Crew(
        agents=[market, sec, indexer, reporter],
        tasks=[market_task, sec_task, index_task, report_task],
        process=Process.sequential
    )

