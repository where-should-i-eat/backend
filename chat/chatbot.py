import dotenv
import openai
import os
from typing import List, Dict
from chat.utils import filter_text

dotenv.load_dotenv()
openai.api_key = os.environ.get("API_KEY")

def GPT_get_result(text_messages: List[Dict[str, str]], model="gpt-4", max_tokens=300):
    output = openai.ChatCompletion.create(
        model=model,
        messages=text_messages,
        max_tokens=max_tokens
        )
    output_text = output['choices'][0]['message']['content']
    return {"role": "assistant", "content": output_text}

def chatbot(messages_history: List[Dict[str, str]], location=""):
    initial_message = {
        "role": "user",
        "content": "You are a helpful assistant designed to help me choose a restaurant. You should ask a series of questions to learn my preferences so that you can suggest a tailored food place recommendation based on my preferences. Go ahead and introduce yourself as a helpful AI assistant designed to help me choose a restaurant and get started with asking the first question to determine my preferences.",
    }
    messages_history.insert(0, initial_message)

    location_message = {
        "role": "user",
        "content": f"These are coordinates of my current location: {location}. Use this to help recommend restaurants near me. DO NOT REMIND ME THAT I TOLD YOU THIS."
    }
    messages_history.insert(1, location_message)

    reminder_message = {
        "role": "assistant",
        "content": "I will not give direct recommendations. I will continue to ask you questions about your preferences, but I won't make a specific recommendation about any places. Even if I think I have enough information to give you a specific place, I WILL NOT GIVE YOU SPECIFIC RECOMMENDATIONS FOR THE REST OF THIS CONVERSATION!"
    }
    messages_history.insert(-1, reminder_message)
    messages_history.append({"role": "user", "content": "Each time you ask me for a preference, surround each option (such as cuisine, flavor, or food type) with a set of asterisks. To make this more visible to both you and I, insert an emoji at the end of these keywords (before the enclosing asterisk). Note that whenever I reply with a preference and you remind me of my preference, do not enclose my already chosen preference with asterisks. Only mark preferences which you are trying to learn with asterisks. DO NOT REMIND ME THAT I TOLD YOU TO ENCLOSE KEYWORDS IN ASTERISKS OR ANY FORMATTING GUIDELINES."})
    text_messages = filter_text(messages_history)
    result = GPT_get_result(text_messages)
    messages_history.pop(-1)
    messages_history.pop(-2) # get rid of reminder_message
    messages_history.append(result)

    messages_history.pop(1) # get rid of location_message
    messages_history.pop(0) # get rid of initial_message


    # print(messages_history)
    return messages_history