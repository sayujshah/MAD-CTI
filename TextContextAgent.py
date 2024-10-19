from autogen import ConversableAgent, GroupChat, GroupChatManager, UserProxyAgent
 
def TextContextAgent(llm_config, dataset):
    # Agent that translates each text from the dataset to English, if needed
    translator = ConversableAgent(
        name="Translator",
        system_message=
        """
        You are a translator agent that is proficient in converting any language into English.
        You will be provided a DatasetDict object with the following features: '__key__', '__url__', and 'txt'.
        Without changing the structure of the DatasetDict object, you will convert each text within the 'txt' feature into English.
        If the text is already English, move onto the next piece of text. You will never make changes to any other features in the DatasetDict object.
        When complete, you will return the updated/translated DatasetDict object (even if no changes were made), along with the word '$$$TERMINATE$$$'.
        """,
        llm_config=llm_config
    )
    # Agent to analyze whether the text is from a forum post/conversation by conducting structural analysis of the texts
    text_analyzer = ConversableAgent(
        name="TextAnalyzer",
        system_message=
        """
        You are an expert in analyzing text to identify forum-like content.
        You will intake a DictionaryDict object from another AI agent with the following features: '__key__', '__url__', and 'txt'.
        For each of the texts, you will determine if there is a clear conversational structure that resembles a dark forum post/thread/conversation.
        Even if the text resembles that of a forum website, it does NOT necessarily mean it is a specific thread or post.
        For example, the front page of a forum website may include a list of multiple threads, but would not fall under the category of a specific forum post.
        A forum post would include a back-and-forth between multiple posters, likely replying to one another and referencing each other along with a new comment.
        Once your are done with your analysis, return the '__key__' value and your corresponding analysis for each of the texts, along with the word '$$$TERMINATE$$$' at the end of your summary list.
        """,
        llm_config=llm_config
    )
    # Agent that reads the analysis of the TextAnalyzer agent and comes up with a final classification on whether the text is from a forum post/conversation
    decision_agent = ConversableAgent(
        name="DecisionAgent",
        system_message=
        """You are an expert at ingesting analysis from another AI agent and coming up with a final decision/classification.
        For each '__key__'-analysis pairing provided by the other AI agent, you will read the analysis and decide if the agent thinks the texts they analyzed are from a dark web forum and if they are from a specific forum post/conversation.
        For context, the agent read from a dataset of texts from dark web websites. You should not need to read these texts to make your determination since the analysis of these texts were already done for you.
        Based on the analyses, if you determine the text came from a dark web post/thread, apply the label 'Forum' and 'Not Forum' if otherwise.
        When you have your results, return each text's '__key__' value and its associated classification label, along with the word '$$$TERMINATE$$$' at the end.
        Do NOT ask for any additional tasks, analysis, texts, etc.
        """,
        llm_config=llm_config
    )
    # User proxy agent
    user = UserProxyAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "$$$TERMINATE$$$" in msg["content"],
        human_input_mode="NEVER",
        code_execution_config=False,
        max_consecutive_auto_reply=10
    )

    # Descriptions of each agent fed to other agents for background of their respective role
    translator.description = "A translator agent that is proficient in converting any language into English"
    text_analyzer.description = "A specialist in identifying structured dark web forum conversation patterns"
    decision_agent.description = "An expert at ingesting analysis from other AI agents and coming up with a final decision/classification"
    
    # Set up a GroupChat for the agents to interact. Specify which specific agents can follow another.
    groupchat = GroupChat(
        agents=[user, translator, text_analyzer, decision_agent],
        speaker_selection_method='auto',
        messages=[],
        send_introductions=True,
        speaker_transitions_type='allowed',
        allowed_or_disallowed_speaker_transitions = {
            user: [translator, text_analyzer, decision_agent],
            translator: [text_analyzer],
            text_analyzer: [decision_agent],
            decision_agent: [user]
        }
    )
    # GroupChatManager to manage the flow of conversation
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config
    )
    
    # Initial chat sent to manager agent
    user.initiate_chat(recipient=manager, message=
                       f"""
                        Translate each of the texts from the DatasetDict object at the end of this message if it is not already in English.
                        \nDATASETDICT OBJECT:
                        \n{dataset}
                        """,
                        summary_method="reflection_with_llm",
                        )