from flask import Flask, jsonify, request
from flask_cors import CORS

from chat.chatbot import chatbot

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'message': 'Healthy!'})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages_history = data['messages']
    print(messages_history)
    messages_history = chatbot(messages_history)
    print(messages_history)
    return jsonify({'messages': messages_history})