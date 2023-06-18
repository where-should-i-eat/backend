import openai
import dotenv
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import re
# from chat.chatbot import chatbot
from connect_gmap import get_restaurant_recommendations, add_to_coordinate
from typing import List, Dict

dotenv.load_dotenv()
openai.api_key = os.environ.get("API_KEY")


def extract_coordinate(text):
    address_pattern = r"(\d+\s+[\w\s]+,\s+[\w\s]+,\s+\w+)"
    addresses = []
    matches = re.findall(address_pattern, text)
    for match in matches:
        addresses.append(match)
    return [add_to_coordinate(a) for a in addresses]

def get_top5(messages_history, recommendations, model="gpt-3.5-turbo", max_tokens=100):
    # TODO reviews
    modified_recs = [r['name'] + "/" + f"rating: {r['rating']}" + "/" + f"distance: {r['distance']}" for r in recommendations]
    findmsg = f"Give me top 3 choices from this list of choices: {modified_recs}. Give me the name of the restaurant and the address"
    name_address = [r['name'] + ":" + r['address'] for r in recommendations]
    addressmsg = f"Tell me the exact address of the restaurant you just chose from this list {name_address}"

    messages_history += [{"role": "user", "content": findmsg}]

    output = openai.ChatCompletion.create(
        model=model,
        messages=messages_history,
        max_tokens=max_tokens
        )
    output_text1 = output['choices'][0]['message']['content']
    messages_history += [{"role": "assistant", "content": output_text1}]
    messages_history += [{"role": "user", "content": addressmsg}]

    output_text2 = output['choices'][0]['message']['content']
    messages_history += [{"role": "assistant", "content": output_text2}]
    print("coordinates:", extract_coordinate(output_text2))
    messages_history.pop(-2)
    messages_history.pop(-3)
    messages_history.pop(-4)

    return output_text2


def chatbot(messages_history: List[Dict[str, str]], model="gpt-3.5-turbo", max_tokens=400):
    initial_message = {
        "role": "user",
        "content": "You are a helpful assistant designed to help me choose a restaurant. You should ask a series of questions to learn my preferences so that you can suggest a tailored food place recommendation based on my preferences. Go ahead and introduce yourself as a helpful AI assistant designed to help me choose a restaurant and get started with asking the first question to determine my preferences.",
    }

    # print(messages_history)
    
    messages_history.insert(0, initial_message)

    output = openai.ChatCompletion.create(
        model=model,
        messages=messages_history,
        max_tokens=max_tokens
        )
    output_text = output['choices'][0]['message']['content']
    messages_history += [{"role": "assistant", "content": output_text}]
    messages_history.pop(0)

    return messages_history

mes_hist = chatbot([])
mes_hist.append({"role": "user", "content": "we want to get meat close to Berkeley campus"})
mes_hist = chatbot(mes_hist)

reco = get_restaurant_recommendations("meat food", (-122.257740, 37.868710))

output_text = get_top5(mes_hist, reco)
print(output_text)


