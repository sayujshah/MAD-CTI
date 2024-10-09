import os
import autogen

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

urls_test = [
    'http://ransomwr3tsydeii4q43vazm7wofla5ujdajquitomtd47cxjtfgwyyd.onion',
    'http://xssforumv3isucukbxhdhwz67hoa5e2voakcfkuieq4ch257vsburuid.onion/'
        ]