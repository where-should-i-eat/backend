from flask import Flask, jsonify, request
from flask_cors import CORS
from chat.chatbot import chatbot
from chat.stopping import end_conversation
from gmaps.connect_gmap import get_restaurant_recommendations
from gmaps.top5 import get_top5

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
    end, google_maps_query = end_conversation(messages_history)
    if end:
        recommendations = get_restaurant_recommendations(google_maps_query, location) # is location the right format?
        top3 = get_top5(messages_history, recommendations)
        print(top3)
        # top3 will return a list of the chosen recommendations
        return jsonify(...) # I'm not sure exactly what format this should b in
    else:
        messages_history = chatbot(messages_history)
        return jsonify({'messages': messages_history})