import os
from dotenv import load_dotenv
load_dotenv()

from Agents.TextAnalyzerAgent import TextAnalyzerAgent
from Agents.RelevanceAgent import RelevanceAgent
from Agents.CategoryAgent import CategoryAgent
from Tools.csvWriterTool import csvWriterTool

from datasets import load_dataset

llm_config = {
    'config_list':
    [
        {'cache_seed': 42,
        'model': "gpt-4o-mini",
        'api_key': os.getenv("OPENAI_API_KEY")
        }
    ]
}

os.getenv('HF_TOKEN')
ds = load_dataset("s2w-ai/CoDA", split="train")
ds_filtered = ds.filter(lambda data: "Hacking" in data['__key__'])

for i in range(len(ds_filtered)):
    analysis = TextAnalyzerAgent(llm_config, ds_filtered[i])
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