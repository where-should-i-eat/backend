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

    reminder_message = {
        "role": "user",
        "content": "Under no circumstances are you allowed to make direct recommendations. Continue asking me questions about my preferences, but DO NOT make a specific recommendation about any places. Even if you think you have enough information to give me a specific place, DO NOT DO GIVE ME SPECIFIC RECOMMENDATIONS FOR THE REST OF THIS CONVERSATION!"
    }
    messages_history.insert(-1, reminder_message)
    final_prompt = "Very important to use italics with important keywords with asterisks"
    messages_history.append({"role": "user", "content": final_prompt})
    text_messages = filter_text(messages_history)
    result = GPT_get_result(text_messages)
    messages_history.pop(-1)
    messages_history.pop(-2) # get rid of reminder_message
    messages_history.append(result)

    messages_history.pop(0) # get rid of initial_message

    # print(messages_history)
    return messages_history