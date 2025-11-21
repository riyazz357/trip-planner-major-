import json
import pickle
import random
import nltk
import re
import requests
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow import keras
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- 1. Load All Necessary Files ---
lemmatizer = WordNetLemmatizer()
model = keras.models.load_model('chat_model.h5')
with open('words.pickle', 'rb') as f:
    words = pickle.load(f)
with open('classes.pickle', 'rb') as f:
    classes = pickle.load(f)

knowledge_base = []
with open('intents.json') as file:
    intents_data = json.load(file)['intents']
    knowledge_base.extend(intents_data)

with open('csv.json') as file:
    csv_data = json.load(file)
    for item in csv_data:
        knowledge_base.append({
            "tag": item['cleaned_query'].lower().replace(' ', '_') + "_info",
            "patterns": [item['cleaned_query']],
            "responses": [item['response']]
        })

# --- 2. Initialize Flask App ---
app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "*"}}) # Enable Cross-Origin Resource Sharing

# --- 3. Define Helper Functions ---
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def extract_location(user_message):
    """Extracts a location from a user's message."""
    # This pattern looks for a location name following common prepositions
    pattern = r'(?:in|for|of|to)\s+([A-Z][a-zA-Z\s]+)'
    match = re.search(pattern, user_message)
    if match:
        return match.group(1).strip()
    return None

def get_weather_data(location):
    """Calls the OpenWeather API."""
    api_key ="e2afbed5bf2ffd9aca5013ae32592340" # Make sure to set this in .env
    if not api_key: return "Weather API key not configured."
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (f"The weather in {location}:\n"
                    f"- Temperature: {data['main']['temp']}°C\n"
                    f"- Condition: {data['weather'][0]['description']}")
        else:
            return "Sorry, I couldn't find weather data for that location."
    except Exception:
        return "Error connecting to the weather service."

def predict_class(sentence):
    bow = bag_of_words(sentence, words)
    res = model.predict(np.array([bow]), verbose=0)[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    if results:
        return classes[results[0][0]]
    return None

# --- 4. Create the /chat API Endpoint ---
# In app.py, replace your old @app.route('/chat') with this one

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "Please send a message."})

    # Step 1: ALWAYS get the AI's prediction first
    predicted_tag = predict_class(user_message)
    bot_response = ""

    # Step 2: ACT based on the predicted tag
    if predicted_tag == 'get_weather':
        location = extract_location(user_message)
        bot_response = get_weather_data(location) if location else "Of course! Which city's weather are you interested in?"
    
    elif predicted_tag == 'get_travel_recommendations':
        # Here you would call your travel API function
        location = extract_location(user_message)
        bot_response = f"Finding recommendations for {location}..." if location else "Certainly! Which place would you like recommendations for?"

    else:
        # Step 3: If not an API call, search the local knowledge base
        if predicted_tag:
            for intent in knowledge_base:
                if intent['tag'] == predicted_tag:
                    bot_response = random.choice(intent['responses'])
                    break
    
    # Final fallback message
    if not bot_response:
        bot_response = "Sorry, I don't quite understand. Could you please rephrase?"

    return jsonify({"reply": bot_response})
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000)) # Default to 10000 for Render
    app.run(host='0.0.0.0', port=port)