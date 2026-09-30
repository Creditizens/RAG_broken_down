import os
from typing import List
from pydantic import BaseModel
from langchain_core.documents import Document
from load_and_create_chunks import load_and_chunk_document
from embeddings_retrieval import (
    vectorstore,
    create_document_from_chunks,
    embed_vectors,
    context_retriever
)
from agent_llm import call_agent
from tools import get_tools
from structured_output_and_state import AgentResponseFormat
from dotenv import load_dotenv


load_dotenv()

DOCUMENT_PATH = os.environ.get("DOCUMENT_PATH")
SEPARATOR = os.environ.get("SEPARATOR")
TOP_K = os.environ.get("TOP_K")
MOOD = os.environ.get("MOOD")

# load data | split data | create `Documents`
# normally might need some try/except but we keep this file simple
document_text_chunks: List[str] = load_and_chunk_document(DOCUMENT_PATH, SEPARATOR)
documents: List[Document] = create_document_from_chunks(document_text_chunks, DOCUMENT_PATH)

# create embedding and store
embed_vectors(documents, vectorstore)

# create a retriever with TOP_K
query = input("\nWhat is your query?: \n")

# custom error 
class RetrievalError(Exception):
    """Raised when the RAF retrieval pipeline fails or returns an error."""
    pass

try:
    context_retrieved: dict[str, List[str]] = context_retriever(
        query.strip(),
        vectorstore,
        TOP_K
    )
    # then we organize it by capturing the keys
    if context_retrieved["error"]:
        raise RetrievalError(f"Context returned with an error: {context_retrieved['error']}")
    else:
        context: str = f"Context: {';'.join(context_retrieved['context'])}. Sources: {';'.join(context_retrieved['sources'])}"
except Exception as e:
    print(f"An error occured while trying to retrieve context: {e}")
    raise RetrievalError(f"Retrieval Exception (error): {e}")


# need first to call agent with the structured output so mode "structured_response"
# then get the content and pass it the next agent
tools = get_tools()

structured_response: dict = call_agent(
    context,
    query,
    tools,
    "structured_response",
    MOOD,
    AgentResponseFormat
)
print(
    "\nStrucured Response = policy - response: \n",
    "\nPOLICY: ", structured_response["structured_response"].policy,
    "\nRESPONSE: ", structured_response["structured_response"].response
)

# Here maybe you can add a Validator step 
# TODO: #foyou!

# we keep going with next agent for the final response using the structured output
# we format the context
new_context: str = f"{context}; {structured_response['structured_response']}"
conversational_tool_response = call_agent(
    new_context,
    query,
    tools,
    "converse_tool",
    MOOD,
    AgentResponseFormat
)
print("\nConversational response: \n", conversational_tool_response["messages"][-1].content)




