import os
from dotenv import load_dotenv
load_dotenv()

from Agents.TextAnalyzerAgent import TextAnalyzerAgent
from Agents.RelevanceAgent import RelevanceAgent
from Agents.CategoryAgent import CategoryAgent
from Tools.csvWriterTool import csvWriterTool
from Tools.darkWebScraperTool import darkWebScraperTool

# Configure LLM setup
llm_config = {
    'config_list':
    [
        {'cache_seed': 42,
        'model': "gpt-4o-mini",
        'api_key': os.getenv("OPENAI_API_KEY")
        }
    ]
}

# Request user to input a valid .onion link to run analysis against
while True:
    try:
        onion_link = input('Input .onion link: ')
        if ".onion" not in onion_link:
            raise ValueError
        break
    except ValueError:
        print("Invalid URL. Make sure you are inputting a dark web .onion URL only.")

# Scrape the provided URL's text
text = darkWebScraperTool(onion_link)
ds = {"__key__": onion_link, "txt": text}

# Multi-agent workflow
analysis = TextAnalyzerAgent(llm_config, ds)
relevancy_results = RelevanceAgent(llm_config, analysis)
key = relevancy_results[0]
label1 = relevancy_results[1]
if "Not Relevant" in label1:
    label1 = "Not Relevant"
    label2 = "N/A"
else:
    category_results = CategoryAgent(llm_config, analysis)
    label1 = "Relevant"
    label2 = category_results[1]
csvWriterTool([[key,label1,label2]])