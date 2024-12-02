from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
 
def TextAnalyzerAgent(llm_config, dataset):
    translator = AssistantAgent(
        name="Translator",
        system_message=
        """
        ROLE:
        You are a translator agent proficient in converting text from any language into English.

        TASKS:
        You will be provided with a DatasetDict object containing three features: '__key__', '__url__', and 'txt'. Your task is to translate the text in the 'txt' field into English while leaving the other features unchanged.

            1. Translation Guidelines:
                - If the text in 'txt' is already in English, return the DatasetDict object unchanged.
                - If the text is not in English, translate it into English and update the 'txt' field accordingly.
            
            2. Restrictions:
                - Do not modify the structure or any other features ('__key__', '__url__') of the DatasetDict object.
                - Do not perform any additional tasks beyond the translation.
        
            3. Completion:
                - Once complete, return the updated DatasetDict object, whether changes were made or not.
                - You will only run once. Do not repeat or request further tasks.
        """,
        llm_config=llm_config
    )
    text_analyzer = AssistantAgent(
        name="TextAnalyzer",
        system_message=
        """
        ROLE:
        You are an expert in analyzing text to determine its structure and nature in relation to online content, specifically focusing on whether it resembles a forum post, blog post, or article.
        
        TASK:
        You will receive a DictionaryDict object from another AI agent with three features: '__key__', '__url__', and 'txt'. Your job is to analyze the text in the 'txt' field and provide a detailed examination of the following:

            1. Conversational Structure (Forum Post/Thread):
                - Analyze whether the text shows back-and-forth interaction between MULTIPLE people, resembling a discussion or conversation. Posts with no responses or what appears to be just one person interacting with his or herself is not relevant and does not fit under this category.
                - Look for responses or references to other posts within the text, typical of a forum thread.
                - Note that the presence of a forum-like structure (such as a list of threads) does not automatically qualify the text as a forum post. There must be clear conversational exchanges.
                - Note that some forum posts/threads may contain ads within the website, however this does NOT immediately make it irrelevant. As long as the PRIMARY content fits the specifications outlined above, it is relevant to us.
        
            2. Consistent Narrative (Blog Post/Article):
                - Determine whether the text follows a consistent and cohesive narrative, such as that of a blog post or news article.
                - Explore whether it presents a specific topic, typically related to cybersecurity, or provides information or instructions on the subject matter.
                - Pay attention to any comments under the text as indicators of engagement, but recognize that a front page showing multiple blog/article links is not relevant.
                - Note that some blog post and articles may contain ads within the website, however this does NOT immediately make it irrelevant. As long as the PRIMARY content fits the specifications outlined above, it is relevant to us.
        
            3. Specific Product/Service
                - Any text that indicates a specific malware or hack for the reader to download, purchase, or recieve a service for is relevant for us to capture.
                - The download is only relevant if it is cyberthreat-related and poses harm (basic software that does not pose any harm are not relevant)
                - These downloads typically include a specific entity and type of hack (e.g. 'password cracker', 'account hacker', 'ransomware')
                - Make note of the entities involved and type of hack/malware
                - Only specific services that target singular entities are helpful to us. Many service offerings will be very general or offer a variety of services for a variety of entitites. These are too general and does not provide us with enough specific information, so are irrelevant.

            4. Irrelevant Content:
                - Content that is PRIMARILY advertisements or marketing material does not belong to the categories of forum, blog, or article.
                - If there is a specific malware/hack being offered to the reader, this is NOT considered irrelevant. It is considered irrelevant if there is no specificity and general/variety of services are being offered.
                - Remember, a forum, blog, or article may contain text that appears to be ads, however if the specifications considered to be 'Relevant' are still present, it is NOT considered irrelevant.
                - Content that appears as if someone or a group is offering a service would not belong to the categories of forum, blog, or article. However, a specific software, malware, hack download would still be relevant as it offers us novel information and typically comes from a forum post from a user.
                - Broken text that appears to have no cohesion or consistent narrative is irrelevant.
                - Explain in your analysis why the text may be irrelevant if it does not fit the other specifications.
        
        ANALYSIS OUTPUT:
            - In your analysis, detail the specific structural or thematic elements found in the text that suggest a resemblance to a forum post, blog post, or article.
            - Even if the text fits the 'Irrelevant Content' category, explain why you find it irrelevant to ensure any future AI agents can classify it as such.
            - Provide a thorough examination of the content's characteristics (e.g., signs of conversation, singular narrative, or irrelevant material) to inform other AI agents.
        
        RULES:
            - You will perform your task once and return the __key__ value along with your full analysis of the text.
            - Do not skip any texts. Always return an appropriate response to pass onto the next agent.
            - If you have already examined a text in the past, do not repeat the analysis for that key.
            - Do not classify the text directly. Your task is only to analyze its resemblance to the categories mentioned.
            - Do not ask for additional tasks, inputs, or repeats of the analysis.
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

    gc = GroupChat(agents=[user,translator, text_analyzer], messages=[], allow_repeat_speaker=False, max_round=3)
    gcm = GroupChatManager(groupchat=gc, llm_config=llm_config)

    user.initiate_chat(
        recipient=gcm,
        message=f"""
        Translate the text from the DatasetDict object at the end of this message if it is not already in English.
        \nDATASETDICT OBJECT:
        \n{dataset}
        """,
        summary_method="last_msg"
    )

    analysis = gcm.groupchat.messages[-1]["content"]
    
    return analysis