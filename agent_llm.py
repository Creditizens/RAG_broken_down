from typing import Literal, Optional
from langchain.agents import create_agent
from langchain_core.tools import tool
from tools import get_tools
from structured_output_and_state import AgentResponseFormat
from prompts import agent_conversation_tool_prompt, agent_structured_response_prompt
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


# get the tools
tools = get_tools()

def call_agent(
    context: str,
    query: str,
    tools: list,
    agent_mode: Literal["converse_tool", "structured_response"],
    mood: str,
    structured_output: Optional(BaseModel),
) -> dict:

    if agent_mode == "structured_response":
        try:
            prompt = agent_structured_response_prompt(context, mood, query)
        except Exception as e:
            return {
                "error": f"An error occured while trying to create the system prompt (structured response): {e}"
            }
        print("\nPrompt (structured response): \n", prompt)
        agent = create_agent(
            # model="ollama:ministral-3-3b-8192",
            model="ollama:qwen3-4b-8192",
            system_prompt=prompt,
            response_format=structured_output,
        )
    elif agent_mode == "converse_tool":
        try:
            prompt = agent_conversation_tool_prompt(context, mood, query),
        except Exception as e:
            return {
                "error": "An error occured while trying to create system prompt (converse tool): {e}"
            }
        print("\nPrompt (converse and tools): \n", prompt)
        agent = create_agent(
            # model="ollama:ministral-3-3b-8192",
            model="ollama:qwen3-4b-8192",
            tools=tools,
            system_prompt=prompt,
        )
    else:
        return {
            "error": """
                An error occured while trying to determine the agent mode `converse_tool` or `structured_response`.
            """
        }

    # now we are all prepared we can invoke
    try:
        result = agent.invoke({
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
    except Exception as e:
        return {
            "error": f"An error occured while trying to invoke agent: {e}"
        }

    # return the result that be paresed later 
    return result


# if __name__ == "__main__":
#     tools = get_tools()
#     agent_mode = "structured_response"
#     response = call_agent(
#         "Shibuya Mangakissa",
#         "What are the rules of your Mangakissa?",
#         tools,
#         agent_mode,
#         "angry",
#         AgentResponseFormat,
#     )
#     if agent_mode == "converse_tool":
#         print("\nResponse content only (converse_tool): \n", response["messages"][-1].content)
#     elif agent_mode == "structured_response":
#         print("\nResponse content only (structured_response): \n", response["structured_response"])
#     else:
#         print("\nSet `agent_mode` to either `converse_tool` or `structured_response`\n")
