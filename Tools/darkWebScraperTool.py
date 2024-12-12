import os

from requests_tor import RequestsTor
from bs4 import BeautifulSoup

# Tool designed to scrape a provided dark web page's text using a tor proxy connection
def darkWebScraperTool(url: str) -> str:
    request = RequestsTor(tor_ports=(9050,), tor_cport=9051, password=os.getenv("HASHED_CONTROL_PASSWORD"))
    response = request.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    else:
        return f'Failed to retrieve {url}'