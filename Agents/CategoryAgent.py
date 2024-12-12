from autogen import AssistantAgent, UserProxyAgent

# Agent designed to classify relevant tasks as having to do with "Hack," "Malware," or "Vulnerability" based on the anlaysis provided by the Text Analyzer Agent
def CategoryAgent(llm_config, analysis):
    category_agent = AssistantAgent(
        name="CategoryAgent",
        system_message=
        f"""
        ROLE:
        You are an expert in interpreting analysis of a dark web text to determine the category that best classifies the text.

        TASKS:
            1. Category Labeling:
            Assign one of the following categories based on the content described in the analysis:
                - Hack: The text details hacking methods or techniques. This typically involves account hacking, password cracking, DDOS attacks, phishing, SQL injection, etc.
                - Malware: The text discusses malware in software, systems, or programs. This may typically be ransomware, viruses, spyware, trojans, keyloggers, etc.
                - Vulnerability: The text describes a vulnerability that can be exploited in a system. This usually involves descriptions of bugs and exploits within software, organizations, or computers that can be taken advantage of.
            2. Output Format:
                - Return the __key__ and the appropriate category determined (either 'Hack', 'Malware', or 'Vulnerability') in a CSV-friendly format.
        
        RULES:
            - Do not skip any texts. Always return an appropriate response to pass onto the next agent.
            - If you have already labeled a text in the past, do not repeat the label for that key.
            - Perform your task once and do not request further tasks or input.
            - Do not repeat your task or analysis.
            - Return only the __key__ and the classification labels as requested. No other characters should be included in your output.
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

    # Initiate agent by feeding analysis from Text Analyzer Agent
    chat = user.initiate_chat(category_agent,
                message = f"""
                Based on the following analysis of a darkweb page extract, determine the category ('Hack', 'Malware', or 'Vulnerability') that best describes the underlying text.
                \nANALYSIS:
                \n{analysis}
                """, max_turns=1)
    
    # Extract the __key__ and classification label from the agent output
    results = chat.summary.split(",")
    
    return results