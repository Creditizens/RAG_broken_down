from typing import Optional


# we do our custom prompts and not using langchain classes here
def agent_conversation_tool_prompt(context: str, mood: str, query: str) -> str:
    return f"""Using tools available answer to user query: {query}.
    With this mood: {mood}.
    Amswer only from this: {context}.
    If the context is not enough to provide answer, answer that the context was unsufficient
    to provide a quality answer. If no tool is relevantto be used for the user query
    or tool return nothing, use only the context to provide an answer
    if relevant otherwise say that you do not have enough information to answer.
    Important: answer using only nicely human readable markdown structured way.
    """

def agent_structured_response_prompt(context: str, mood: str, query: str) -> str:
    return f"""Analyze the initial query: {query}; and the given context: {context};
    then use tools available to provide an answer with {mood} mood,
    following strictly only the structured ouput desired format schema.
    """


