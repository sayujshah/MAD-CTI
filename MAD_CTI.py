import os
from dotenv import load_dotenv
load_dotenv()

from autogen import AssistantAgent, ConversableAgent, GroupChat, GroupChatManager, register_function
from DarkWebScraper import DarkWebScraper

from datasets import load_dataset
import pandas as pd

# Login using e.g. `huggingface-cli login` to access this dataset
os.getenv('HF_TOKEN')
ds = load_dataset("s2w-ai/CoDA", split="train")
ds_snippet = ds[0:5]
      
llm_config = {
    'config_list':
    [
        {'seed': 42,
        'model': "gpt-4o-mini",
        'api_key': os.getenv("OPENAI_API_KEY")
        }
    ]
}

assistant1 = AssistantAgent(
    name="Dark_Web_Text_Scraper",
    system_message=
    """
    You are a scraper agent that reads through text found on the dark web and cleans them to ensure they are easy to comprehendable for other agents.
    You will be provided with a DatasetDict object that has the following features: '__key__', '__url__', and 'txt'.
    Your job is to clean the texts found in the 'txt' feature by extracting only the most relevant aspects of the text.
    Leave the rest of the structure of the DatasetDict object alone. Output the DatasetDict object with the cleaned 'txt' values to the next agent.
    """,
    llm_config=llm_config

)

assistant2 = AssistantAgent(
    name="Text_Context_Classifier",
    system_message=
    """
    You will take in a DatasetDict object containing keys, URLs, and dark-web-related text.
    Your job is to analyze each text and determine whether they have to do with a dark web forum conversation.
    You will return a list of the URLs for each text and their associated classification: 'Forum' or 'Not Forum',
    where 'Forum' means you think the context of the text is part of a dark web forum conversation and 'Not Forum' is when it does not have to do with a forum conversation.
    Note that if the text looks like a listing of forum posts, this does NOT count as part of the 'Forum' classification. We are only interested in individual forum postings themselves.
    """,
    llm_config=llm_config
)

user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER"
)

groupchat = GroupChat(agents=[assistant1, assistant2, user_proxy], messages=[], max_round=12)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

chat_result = user_proxy.initiate_chat(
    manager, message=
    f"""
    Pass the DatasetDict object at the end of this message onto the Dark_Web_Text_Scraper agent.
    You will take the outputs of the Dark Web Text Scraper agent and pass it onto the Text_Context_Classifier agent.
    When the Text_Context_Classifier agent is complete with its task, it will output a list of URLs and their classification ('Forum' or 'Not Forum').
    Output this list within the terminal in a easy-to-read format, along with the word 'TERMINATE' at the end of the list.
    Use the following DatasetDict object to complete your specified project: {ds_snippet}.
    """
)