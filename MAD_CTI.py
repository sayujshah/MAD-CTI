import os
from dotenv import load_dotenv
load_dotenv()

from autogen import ConversableAgent, register_function
from DarkWebScraper import DarkWebScraper

llm_config = {
    'config_list':
    [
        {'seed': 42,
        'model': "gpt-4o-mini",
        'api_key': os.getenv("OPENAI_API_KEY")
        }
    ]
}

assistant = ConversableAgent(
    name="Dark Web Scraper",
    system_message="You are a scraper agent that crawls a provided list of dark web URLs and extract its contents.",
    llm_config=llm_config
)

user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER"
)

register_function(
    DarkWebScraper,
    caller=assistant,
    executor=user_proxy,
    name="DarkWebScraper",
    description="A dark web scraper/crawler"
)

urls_test = [
    'http://ransomwr3tsydeii4q43vazm7wofla5ujdajquitomtd47cxjtfgwyyd.onion',
    'http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/post/c12ec91069be2b9ef93b' # Ransomware post
        ]

chat_result = user_proxy.initiate_chat(assistant, message=f"Scrape through each .onion URL within {urls_test} and extract the website's contents. Output each URL's extracted content within the terminal.")