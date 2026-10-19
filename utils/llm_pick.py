from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def pick_llm(level: str):
    """
    Picks the appropriate LLM based on the level of the question

    Args:
        level (str): The level of the question, can be 

    Returns:
        str: The name of the LLM to be used.
    """

    if level.lower() == "low":
        llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)
    elif level.lower() == "medium":
        llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)
    elif level.lower() == "high":
        llm = ChatGoogleGenerativeAI(model="gemini-3.1-pro-preview", temperature=0)
    else:
        raise ValueError(f"Unsupported level: {level}")

    return llm

