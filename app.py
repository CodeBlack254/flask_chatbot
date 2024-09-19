from flask import Flask, request, jsonify # type: ignore
import json
import random

app = Flask(__name__)

# Load training data from JSON file
with open('training_data.json') as f:
    training_data = json.load(f)

# Create a pattern-response dictionary
pattern_response_map = {}
for intent in training_data['intents']:
    for pattern in intent['patterns']:
        pattern_response_map[pattern.lower()] = intent['responses']

def get_response(user_input):
    user_input = user_input.lower()
    if user_input in pattern_response_map:
        return random.choice(pattern_response_map[user_input])
    return jsonify({'response': 'I\'m sorry, I didn\'t understand that.'})

@app.route('/chat', methods=['POST'])

def chat():
    try:
        user_input = request.json['message']
        bot_response = get_response(user_input)
        return jsonify({'response': bot_response})
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/')
def home():
    return jsonify({'response': 'Chatbot API is running. Use the /chat endpoint to interact with it.'})

if __name__ == '__main__':
    app.run(debug=True)
