
import requests
from bs4 import BeautifulSoup
from crewai.tools import tool
import json
from typing import List

@tool("SECFilingSummary")
def fetch_sec_filings(portfolio: List[str] = None) -> str:
    """
    Searches SEC EDGAR for recent filings (10-K, 10-Q) for each portfolio company.
    Returns basic summaries.
    """

    with open("/path/to/portfolio.json", "r") as f:
        portfolio = json.load(f)

    base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=10-"
    headers = {"User-Agent": "finance-agent/1.0"}

    summaries = []
    for item in portfolio["portfolio"]:
        query_name = item["name"].split()[0]
        try:
            response = requests.get(base_url.format(query_name), headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            link = soup.find("a", string="Documents")
            if link:
                summaries.append(f"{item['symbol']} – Found recent filing: {link['href']}")
            else:
                summaries.append(f"{item['symbol']} – No recent filings found")
        except Exception as e:
            summaries.append(f"{item['symbol']} – Error: {e}")

    return "\n".join(summaries)
