# action_agent.py
# Action Agent: Generate H5 game HTML code and extract <html>...</html>
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import re

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_API_BASE")
deepseek_api_key = os.getenv("Deepseek_API_KEY")
deepseek_api_base = os.getenv("Deepseek_API_BASE")


def build_action_agent():
    llm = ChatOpenAI(
        openai_api_key=api_key,
        base_url=base_url,
        model="moonshot-v1-8k",
        # openai_api_key=deepseek_api_key,  # DeepSeek platform API Key
        # base_url=deepseek_api_base,  # DeepSeek official API address
        # model="deepseek-chat",  # Model name
        temperature=0.7
    )
    prompt = PromptTemplate(
        input_variables=["desc"],
        template="""
        You are a professional HTML game developer. Create a complete, functional H5 web mini-game based on the user's requirement.

        User requirement: {desc}

        CRITICAL REQUIREMENTS:
        1. You MUST output ONLY a complete HTML document
        2. The HTML must start with <!DOCTYPE html> and end with </html>
        3. Include all necessary CSS and JavaScript within the HTML file
        4. The game must be fully functional and runnable
        5. Include clear Start/End buttons, scoring system, and replay functionality
        6. Disable arrow key scrolling - arrow keys should only control the game
        7. Use bright colors and simple controls suitable for children with autism
        8. Make the game educational and engaging

        OUTPUT FORMAT:
        Start your response with <!DOCTYPE html> and end with </html>
        Do not include any explanations, comments, or markdown formatting outside the HTML code.
        The entire response should be valid HTML that can be saved as a .html file and run directly in a browser.

        IMPORTANT: Your response must be a complete HTML document. Do not include any text before <!DOCTYPE html> or after </html>.

        Example structure:
        <!DOCTYPE html>
        <html>
        <head>
            <title>Game Title</title>
            <style>/* CSS here */</style>
        </head>
        <body>
            <!-- Game content here -->
            <script>/* JavaScript here */</script>
        </body>
        </html>
        """
    )
    chain = prompt | llm
    return chain

def extract_html(text):
    # Automatically compatible with dict and AIMessage input
    if hasattr(text, 'content'):
        text = text.content
    if isinstance(text, dict):
        text = text.get("content") or text.get("text") or str(text)
    
    # First try to find complete HTML document
    match = re.search(r'<!DOCTYPE html>[\s\S]*?</html>', text, re.IGNORECASE)
    if match:
        return match.group(0)
    
    # If no DOCTYPE, try to find HTML document
    match = re.search(r'<html[\s\S]*?</html>', text, re.IGNORECASE)
    if match:
        return match.group(0)
    
    # If no complete HTML document, try to find HTML code blocks
    # Look for code blocks with HTML language specification
    match = re.search(r'```html\s*([\s\S]*?)```', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Look for code blocks without language specification
    match = re.search(r'```\s*([\s\S]*?)```', text, re.IGNORECASE)
    if match:
        code_content = match.group(1).strip()
        # Check if it contains HTML tags
        if re.search(r'<[^>]+>', code_content):
            return code_content
    
    # If still no match, return the entire text if it contains HTML tags
    if re.search(r'<[^>]+>', text):
        return text
    
    return None

if __name__ == "__main__":
    agent = build_action_agent()
    user_desc = "I want a Snake H5 mini-game"
    html_code = agent.invoke({"desc": user_desc})
    html_code = extract_html(html_code)
    print("Generated HTML code snippet:\n", html_code) 