import dotenv
import openai
import os
from typing import List, Dict
from chatbot import *

dotenv.load_dotenv()
openai.api_key = os.environ.get("API_KEY")

def test_chatbot(model="gpt-3.5-turbo", max_tokens=100):
    end = False
    messages_history = chatbot([])
    while not end:
        print(messages_history[-1]["content"])
        user_input = input()
        messages_history.append({"role": "user", "content": user_input})
        messages_history = chatbot(messages_history)
        end = end_conversation(messages_history, model=model, max_tokens=max_tokens)

def end_conversation(messages_history, model="gpt-4", max_tokens=100):
    """
    Returns True iff the conversation has sufficient information to create a GoogleMaps API query and pick desired restaurants.

    Note that in testing, this function works a lot better using GPT-4.
    """
    check_end_message = "If I were going to use the information you've given me about my preferences to query the GoogleMaps API, would I have given you enough information? The necessary information I would need include my location, food preferences, price range, etc. RETURN TRUE IF I HAVE GIVEN ENOUGH INFORMATION, OTHERWISE RETURN FALSE. SAY NOTHING ELSE."

    messages_history.append({"role": "user", "content": check_end_message})

    output = openai.ChatCompletion.create(
        model=model,
        messages=messages_history,
        max_tokens=max_tokens
        )
    output_text = output['choices'][0]['message']['content']
    messages_history.pop()

    end = "true" in output_text.lower()
    return end

test_chatbot(model="gpt-4")