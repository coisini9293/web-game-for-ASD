# decision_agent.py
# Decision Agent: Always generate an H5 game
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_API_BASE")

def build_decision_agent():
    llm = ChatOpenAI(
        openai_api_key=api_key,
        base_url=base_url,
        model="moonshot-v1-8k",
        temperature=0.7
    )
    prompt = PromptTemplate(
        input_variables=["type"],
        template="""Based on the user's requirement, always respond with "GENERATE_H5_GAME" to create a relevant H5 game.

User requirement type: {type}

Response: GENERATE_H5_GAME"""
    )
    chain = prompt | llm
    return chain    

if __name__ == "__main__":
    agent = build_decision_agent()
    type = "Web Game"
    result = agent.invoke({"type": type})
    print(f"Decision Agent result: {result}") 