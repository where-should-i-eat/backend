from flask import Flask, jsonify, request
from flask_cors import CORS
from chat.chatbot import chatbot
from chat.stopping import end_conversation
from gmaps.connect_gmap import get_restaurant_recommendations
from gmaps.top5 import converter

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'message': 'Healthy!'})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    print(data['location'])
    location = data['location']
    messages_history = data['messages']
    cnt = 0
    for message in messages_history:
        if message["role"] == "user":
            cnt += 1
    if cnt >= 3:
        end, google_maps_query = end_conversation(messages_history, location)
        print("google_maps_query", google_maps_query)
    
    if end:
        recommendations = get_restaurant_recommendations(google_maps_query, location) # is location the right format?
        print("recommendations", recommendations)
        top3 = converter(messages_history, recommendations, location)
        print('top3', top3)
        # top3 will return a list of the chosen recommendations
        # append top3 to messages_history
        messages_history += top3
    else:
        messages_history = chatbot(messages_history, location=location)
    return jsonify({'messages': messages_history})