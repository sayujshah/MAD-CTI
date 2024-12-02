from autogen import AssistantAgent, UserProxyAgent
 
def RelevanceAgent(llm_config, analysis):
    relevance_agent = AssistantAgent(
        name="RelevanceAgent",
        system_message=
        """
        ROLE:
        You are an expert in interpreting analysis from other AI agents to determine the relevancy of text based on a defined use case.

        TASKS:
        You will receive a '__key__' and its corresponding analysis from another AI agent. Your job is to read the analysis and determine whether the text described in the analysis is from a dark web forum, blog post, or article. You are not required to read the original text. The analysis provided contains all the information you need.

            1. Relevance Determination:
                - If the analysis indicates that the text resembles a dark web forum post, blog post, or article, label it as 'Relevant'.
                - If the analysis indicates a specific software, malware, hack, etc. download is present, label it as 'Relevant'.
                - If the analysis suggests that the text does not fit these categories (e.g., it's an advertisement, front page with a list of posts, etc.), label it as 'Not Relevant'.
        
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

            2. Output Format:
                - Return the __key__, its classification (either 'Relevant' or 'Not Relevant') in a CSV-friendly format.
        
        RULES:
            - Do not skip any texts. Always return an appropriate response to pass onto the next agent.
            - If you have already labeled a text in the past, do not repeat the label for that key.
            - Perform your task once and do not request further tasks or input.
            - Do not repeat your task or analysis.
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
    chat = user.initiate_chat(relevance_agent,
                    message = f"""
                    Based on the following analysis of a darkweb page extract, determine the relevancy of the underlying text.
                    \nANALYSIS:
                    \n{analysis}
                    """, max_turns=1)
    results = chat.summary.split(",")

    return results