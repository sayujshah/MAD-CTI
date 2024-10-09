import os
from autogen import ConversableAgent

from requests_tor import RequestsTor
from bs4 import BeautifulSoup

llm_config = {
    'config_list':
    [
        {
        'model': "gpt-4o-mini",
        'api_key': os.getenv("OPENAI_API_KEY"),
        'api_rate_limit': 60.0
        }
    ]
}

def DarkWebScraper(urls: list) -> str:
    for url in urls:
        request = RequestsTor(tor_ports=(9050,), tor_cport=9051, password=os.getenv("HASHED_CONTROL_PASSWORD"))
        response = request.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            '''
            links = soup.find_all('a')
            for link in links:
                print(link.get('href'))
            '''
            return soup.get_text()
        else:
            return f'Failed to retrieve {url}'

assistant = ConversableAgent(
    name="Dark Web Scraper",
    system_message="You are a scraper agent that crawls a provided list of dark web URLs and extract its contents.",
    llm_config=llm_config,
)

user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# Register the tool signature with the assistant agent.
assistant.register_for_llm(name="DarkWebScraper", description="A dark web scraper/crawler")(DarkWebScraper)

# Register the tool function with the user proxy agent.
user_proxy.register_for_execution(name="DarkWebScraper")(DarkWebScraper)

urls_test = [
    'http://ransomwr3tsydeii4q43vazm7wofla5ujdajquitomtd47cxjtfgwyyd.onion',
    'http://xssforumv3isucukbxhdhwz67hoa5e2voakcfkuieq4ch257vsburuid.onion/'
        ]