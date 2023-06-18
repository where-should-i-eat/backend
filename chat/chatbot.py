import dotenv
import openai
import os
from typing import List, Dict
from chat.utils import filter_text

dotenv.load_dotenv()
openai.api_key = os.environ.get("API_KEY")

def GPT_get_result(text_messages: List[Dict[str, str]], model="gpt-3.5-turbo", max_tokens=100):
    output = openai.ChatCompletion.create(
        model=model,
        messages=text_messages,
        max_tokens=max_tokens
        )
    output_text = output['choices'][0]['message']['content']
    return {"role": "assistant", "content": output_text}

def chatbot(messages_history: List[Dict[str, str]]):
    initial_message = {
        "role": "user",
        "content": "You are a helpful assistant designed to help me choose a restaurant. You should ask a series of questions to learn my preferences so that you can suggest a tailored food place recommendation based on my preferences. Go ahead and introduce yourself as a helpful AI assistant designed to help me choose a restaurant and get started with asking the first question to determine my preferences.",
    }
    messages_history.insert(0, initial_message)

    text_messages = filter_text(messages_history)
    result = GPT_get_result(text_messages)
    messages_history.append(result)

    messages_history.pop(0)

    print(messages_history)
    return messages_history