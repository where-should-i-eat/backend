import dotenv
import openai
import os
from typing import List, Dict

dotenv.load_dotenv()
openai.api_key = os.environ.get("API_KEY")

def chatbot(messages_history: List[Dict[str, str]], model="gpt-3.5-turbo", max_tokens=100):
    initial_message = {
        "role": "user",
        "content": "You are a helpful assistant designed to help me choose a restaurant. You should ask a series of questions to learn my preferences so that you can suggest a tailored food place recommendation based on my preferences. Go ahead and introduce yourself as a helpful AI assistant designed to help me choose a restaurant and get started with asking the first question to determine my preferences.",
    }
    
    messages_history.insert(0, initial_message)

    output = openai.ChatCompletion.create(
        model=model,
        messages=messages_history,
        max_tokens=max_tokens
        )
    output_text = output['choices'][0]['message']['content']
    messages_history += [{"role": "assistant", "content": output_text}]
    messages_history.pop(0)

    print(messages_history)


    return messages_history