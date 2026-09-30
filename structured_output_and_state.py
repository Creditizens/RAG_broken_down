from pydantic import BaseModel, Field
from typing import Literal, List
from typing_extensions import TypedDict


class AgentResponseFormat(BaseModel):
    """responding with policy part and response part resulting of that same policy"""
    policy: str = Field(description="the policy rule that justifies the answer otherwise '' if no answer in given context")
    response: str = Field(description="answer to the user based on context given otherwise informthat the context was insufficient to make an opinion.")
