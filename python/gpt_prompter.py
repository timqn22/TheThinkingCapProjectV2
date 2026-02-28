from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env into os.environ

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def gpt_prompter(prompt: str):
    print(prompt)
    
    if isinstance(prompt, list):
        prompt = prompt[0]

    prompt = str(prompt)
    print(prompt)
    
    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt
    )
    
    return str(response.output_text)
