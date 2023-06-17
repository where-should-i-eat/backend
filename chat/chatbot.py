import dotenv
import openai
import os
from typing import List, Dict

dotenv.load_dotenv()
openai.api_key = os.environ.get("API_KEY")

def chatbot(messages_history: List[Dict[str, str]], model="gpt-3.5-turbo", max_tokens=100):

    output = openai.ChatCompletion.create(
        model=model,
        messages=messages_history,
        max_tokens=max_tokens
        )
    output_text = output['choices'][0]['message']['content']
    messages_history += [{"role": "assistant", "content": output_text}]

    return messages_history