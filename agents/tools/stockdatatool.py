
import yfinance as yf
from crewai.tools import tool
import json

@tool("StockDataFetcher")
def fetch_stock_data(_: str = None) -> str:
    """
    Fetch current market data for each stock in the user's portfolio and watchlist.
    Returns a summary string of all stock metrics.
    """

    with open("/path/to/portfolio.json", "r") as f:
        portfolio = json.load(f)

    summary = []
    symbols = [item["symbol"] for item in portfolio["portfolio"]] + [
        item["symbol"] for item in portfolio.get("watchlist", [])
    ]

    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            data = stock.info
            summary.append(
                f"{symbol} - {data.get('longName', 'N/A')}\n"
                f"Price: {data.get('regularMarketPrice', 'N/A')}, "
                f"PE Ratio: {data.get('trailingPE', 'N/A')}, "
                f"Market Cap: {data.get('marketCap', 'N/A')}\n"
            )
        except Exception as e:
            summary.append(f"{symbol} - Error fetching data: {e}")

    return "\n".join(summary)
