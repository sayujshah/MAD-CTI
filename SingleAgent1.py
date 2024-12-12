from autogen import AssistantAgent, UserProxyAgent, register_function
from csvWriterTool import csvWriterTool

import os
from dotenv import load_dotenv
load_dotenv()

from datasets import load_dataset

from time import time
 
def ThreatClassificationAgent(llm_config, dataset):
    assistant = AssistantAgent(
        name="ThreatClassificationAgent",
        system_message=
        f"""
        ROLE:
        You are an expert at intaking a piece of cyberthreat-related text, translating it to English (if needed), analyzing it, determining its relevany, and identifying the type of cyberthreat that is being discussed in the text.
        
        TASKS:
        1. Translation Guidelines:
            - If the text in the 'txt' key of the DatasetDict object is not in English, translate it.
            - Do not modify the structure or any other features ('__key__', '__url__') of the DatasetDict object.
        
        2. Text Analysis:
            a. Conversational Structure (Forum Post/Thread):
                - Analyze whether the text shows back-and-forth interaction between MULTIPLE people, resembling a discussion or conversation. Posts with no responses or what appears to be just one person interacting with his or herself is not relevant and does not fit under this category.
                - Look for responses or references to other posts within the text, typical of a forum thread.
                - Note that the presence of a forum-like structure (such as a list of threads) does not automatically qualify the text as a forum post. There must be clear conversational exchanges.
                - Note that some forum posts/threads may contain ads within the website, however this does NOT immediately make it irrelevant. As long as the PRIMARY content fits the specifications outlined above, it is relevant to us.
            b. Consistent Narrative (Blog Post/Article):
                - Determine whether the text follows a consistent and cohesive narrative, such as that of a blog post or news article.
                - Explore whether it presents a specific topic, typically related to cybersecurity, or provides information or instructions on the subject matter.
                - Pay attention to any comments under the text as indicators of engagement, but recognize that a front page showing multiple blog/article links is not relevant.
                - Note that some blog post and articles may contain ads within the website, however this does NOT immediately make it irrelevant. As long as the PRIMARY content fits the specifications outlined above, it is relevant to us.
            c. Specific Product/Service
                - Any text that indicates a specific malware or hack for the reader to download, purchase, or recieve a service for is relevant for us to capture.
                - The download is only relevant if it is cyberthreat-related and poses harm (basic software that does not pose any harm are not relevant)
                - These downloads typically include a specific entity and type of hack (e.g. 'password cracker', 'account hacker', 'ransomware')
                - Make note of the entities involved and type of hack/malware
                - Only specific services that target singular entities are helpful to us. Many service offerings will be very general or offer a variety of services for a variety of entitites. These are too general and does not provide us with enough specific information, so are irrelevant.
            d. Irrelevant Content:
                - Content that is PRIMARILY advertisements or marketing material does not belong to the categories of forum, blog, or article.
                - If there is a specific malware/hack being offered to the reader, this is NOT considered irrelevant. It is considered irrelevant if there is no specificity and general/variety of services are being offered.
                - Remember, a forum, blog, or article may contain text that appears to be ads, however if the specifications considered to be 'Relevant' are still present, it is NOT considered irrelevant.
                - Content that appears as if someone or a group is offering a service would not belong to the categories of forum, blog, or article. However, a specific software, malware, hack download would still be relevant as it offers us novel information and typically comes from a forum post from a user.
                - Broken text that appears to have no cohesion or consistent narrative is irrelevant.

        3. Relevance Determination:
            a. Relevancy Guidelines:
                - Forum Post: Must show a clear conversation between MULTIPLE people, such as replies and references to each other's posts. Lists of forum threads without conversation are not relevant. A forum post with no responses or what appears to be just one person interacting with his or herself is not relevant.
                - Blog Post/Article: Should describe a specific topic, often related to cybersecurity, with a clear, consistent narrative.
                - Downloads: Includes a specific software, malware, or hack download submitted to a user base from a poster (typically on a forum or blog). The download is only relevant if it is cyberthreat-related and poses harm (basic software that does not pose any harm are not relevant)
                - Specific Product/Service: A specific service being offered is considered relevant if it is a hack, malware, or vulnerabliity toward a singular entity. General hacking services with little specificity are not relevant.
            b. Irrelevancy Guidelines:
                - Advertisements, listings of posts/pages, or incohesive broken up text without meaningful content do not qualify as relevant and should be labeled 'Not Relevant'.
                - Any non-cybersecurity/cyberthreat-related content should be labeled 'Not Relevant'.
                - General hacking service offerings that offer a variety of services targeting a variety of entitties with little specificity should be labeled 'Not Relevant'.
                - If the analysis indicates ANY of these to be true, the text should be labeled as 'Not Relevant'.
        
        4. Category Labeling:
            Assign one of the following categories based on the your analysis of the text:
                - Hack: The text details hacking methods or techniques. This typically involves account hacking, password cracking, DDOS attacks, phishing, SQL injection, etc.
                - Malware: The text discusses malware in software, systems, or programs. This may typically be ransomware, viruses, spyware, trojans, keyloggers, etc.
                - Vulnerability: The text describes a vulnerability that can be exploited in a system. This usually involves descriptions of bugs and exploits within software, organizations, or computers than can be taken advantage of.
                - N/A: If the text was found to be 'Not Relevant', set the category label to 'N/A'
        
        OUTPUT:
            - Once all tasks have been completed and you have both the relevancy and category labels, return the __key__, relevancy label ('Relevant' or 'Not Relevant'), and the appropriate category determined (either 'Hack', 'Malware', 'Vulnerability', or 'N/A') in a CSV-friendly format.

        RULES:
            - Perform your tasks once and do not request further tasks or input.
            - Return only the __key__ and the classification labels as requested.
        """,
        llm_config=llm_config
    )
    user = UserProxyAgent(
        name="User",
        llm_config=llm_config,
        is_termination_msg=lambda msg: msg.get("content") is not None and "$$$TERMINATE$$$" in msg["content"],
        human_input_mode="NEVER",
        code_execution_config=False,
        max_consecutive_auto_reply=1
    )

    chat = user.initiate_chat(assistant,
                message = f"""
                Translate the text from the DatasetDict object at the end of this message if it is not already in English, analyze it, determine its relevancy, and the type of cyberthreat that is being discussed within the text.
                Return the text's key, Relevancy Label, and Category Label in a CSV-friendly format.
                \nDATASETDICT OBJECT:
                \n{dataset}
                """, max_turns=1)
    chat_result = chat.summary.split(",")
    
    return chat_result

llm_config = {
    'config_list':
    [
        {'cache_seed': 38,
        'model': "gpt-4o-mini",
        'api_key': os.getenv("OPENAI_API_KEY")
        }
    ]
}

os.getenv('HF_TOKEN')
ds = load_dataset("s2w-ai/CoDA", split="train")
ds_filtered = ds.filter(lambda data: "Hacking" in data['__key__'])

start = time()
for i in range(len(ds_filtered)):
    out = ThreatClassificationAgent(llm_config, ds_filtered[i])
    csvWriterTool([out])
 
end = time()
print(end-start)