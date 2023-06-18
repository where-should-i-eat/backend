import openai
import dotenv
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
# from chat.chatbot import chatbot
from connect_gmap import get_restaurant_recommendations
from typing import List, Dict

dotenv.load_dotenv()
openai.api_key = os.environ.get("API_KEY")


def get_top5(messages_history, recommendations, model="gpt-3.5-turbo", max_tokens=100):
    # TODO: figure out distance, reviews
    modified_recs = [{'name': r['name'], 'rating': r['rating'], 'location': r['address']} for r in recommendations]
    message = f"Help me now to determine the top 5 choices from this list of choices: {modified_recs}."

    messages_history += [{"role": "user", "content": message}]

    output = openai.ChatCompletion.create(
        model=model,
        messages=messages_history,
        max_tokens=max_tokens
        )
    output_text = output['choices'][0]['message']['content']
    messages_history += [{"role": "assistant", "content": output_text}]
    messages_history.pop(-2)

    return output_text


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

    # print(messages_history)


    return messages_history

mes_hist = chatbot([])
mes_hist.append({"role": "user", "content": "we want to get meat close to Berkeley campus"})
mes_hist = chatbot(mes_hist)

reco = get_restaurant_recommendations("meat food", -122.257740, 37.868710)

output_text = get_top5(mes_hist, reco)
print(output_text)