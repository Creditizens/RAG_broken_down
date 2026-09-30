from langchain_core.tools import tool
from typing import Optional, List


# we define a tool using the decorator `@tool`
@tool
def get_policy_ruling() -> str:
    """Get the policy rules for Mangakissa Shibuya Lv5."""
    return f"""
      MangaKissa Rules:
      - You can't leave the drinking area dirty, please clean after yourself
      - Drinks and ice cream are all free
      - You can't wath Naruto anymore
      - We remind you that walking around lookinf for people is not allowed, it is not a dating place
      - Be quiet and respect other people peace
    """

tools = [get_policy_ruling,]
def get_tools() -> List:
    return tools
