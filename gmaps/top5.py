import openai
import dotenv
import os

import re
# from chat.chatbot import chatbot
from gmaps.connect_gmap import get_restaurant_recommendations, add_to_coordinate, get_name
from typing import List, Dict

dotenv.load_dotenv()
openai.api_key = os.environ.get("API_KEY")


def extract_coordinate(recom, text):
    address_pattern = r"(\d+\s+[\w\s]+,\s+[\w\s]+,\s+\w+)"
    name_pattern = r'@([^@]+)@'
    names = []
    addresses = []
    matches = re.findall(address_pattern, text)
    for match in matches:
        addresses.append(match)
    matches = re.findall(name_pattern, text)
    for match in matches:
        names.append(match)
    # return [[add_to_coordinate(a), a, get_name(add_to_coordinate(a))] for a in addresses]

    return [[add_to_coordinate(addresses[idx]), addresses[idx], names[idx]] for idx in list(range(min(len(names), len(addresses))))]

def extract_text_between_at_signs(text):
    pattern = r'@([^@]+)@'
    matches = re.findall(pattern, text)
    return matches

def get_top5(messages_history, recom, model="gpt-3.5-turbo", max_tokens=100):
    # TODO reviews
    modified_recs = [recom[r]['name'] + "/" + f"rating: {recom[r]['rating']}" + "/" + f"distance: {recom[r]['distance']}" for r in recom.keys()]
    findmsg = f"Give me top 3 choices from this list of choices: {modified_recs}. Give me the name of the restaurant (enclosed in @ symbols) and the address"
    name_address = [recom[r]['name'] + ":" + recom[r]['address'] for r in recom]
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
    # print("coordinates:", extract_coordinate(output_text2))
    messages_history.pop(-2)
    messages_history.pop(-3)
    messages_history.pop(-4)

    return output_text2, extract_coordinate(recom, output_text2)


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

# def encode():
    
