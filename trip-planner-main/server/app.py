import os
import json
import pickle
import random
import traceback
import nltk
import numpy as np
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import your AI logic
import bard 

# --- 1. Configuration & Setup ---
load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)
# Enable CORS for all domains
CORS(app, resources={r"/*": {"origins": "*"}})

# --- 2. Global Variables for Lazy Loading ---
chat_model = None
words = None
classes = None
knowledge_base = None
lemmatizer = None

# --- 3. Helper Functions ---

# Lazy Load Chatbot Resources
def load_chatbot_resources():
    global chat_model, words, classes, knowledge_base, lemmatizer
    
    if chat_model is not None:
        return

    print("⏳ Loading Chatbot AI models (TensorFlow & NLTK)...")
    
    from nltk.stem import WordNetLemmatizer
    from tensorflow import keras

    # Ensure NLTK data exists
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('tokenizers/punkt_tab')
        nltk.data.find('corpora/wordnet')
        nltk.data.find('corpora/omw-1.4')
    except LookupError:
        print("⬇️ Downloading missing NLTK data...")
        nltk.download('punkt')
        nltk.download('punkt_tab')
        nltk.download('wordnet')
        nltk.download('omw-1.4')

    lemmatizer = WordNetLemmatizer()
    
    try:
        chat_model = keras.models.load_model('chat_model.h5')
        with open('words.pickle', 'rb') as f:
            words = pickle.load(f)
        with open('classes.pickle', 'rb') as f:
            classes = pickle.load(f)
        
        knowledge_base = []
        # Load Knowledge Base
        try:
            with open('intents.json') as file:
                knowledge_base.extend(json.load(file)['intents'])
        except FileNotFoundError:
            print("⚠️ intents.json not found.")

        try:
            with open('csv.json') as file:
                for item in json.load(file):
                    knowledge_base.append({
                        "tag": item['cleaned_query'].lower().replace(' ', '_') + "_info",
                        "patterns": [item['cleaned_query']],
                        "responses": [item['response']]
                    })
        except FileNotFoundError:
             print("⚠️ csv.json not found.")
             
        print("✅ Chatbot resources loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading chatbot files: {e}")
        traceback.print_exc()


# ==========================================
#               CHATBOT ROUTE
# ==========================================

@app.route('/chat', methods=['POST'])
def chat():
    # Load resources only when chat is used
    load_chatbot_resources()
    
    if not chat_model:
        return jsonify({"reply": "Chatbot is initializing or failed to load. Please check server logs."})

    data = request.get_json()
    user_message = data.get("message")
    
    if not user_message:
        return jsonify({"reply": "Please send a message."})

    # Local Helper Functions
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

    # Predict
    try:
        bow = bag_of_words(user_message, words)
        res = chat_model.predict(np.array([bow]), verbose=0)[0]
        
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        
        predicted_tag = classes[results[0][0]] if results else None
        bot_response = ""

        if predicted_tag:
            # If the AI predicts the user wants a recommendation, use Google Gemini
            if predicted_tag == 'destination_recommendation':
                 try:
                     bot_response = bard.get_chat_recommendations(user_message)
                 except AttributeError:
                     bot_response = "I recommend visiting the city center!"
            else:
                # Otherwise, check the local files
                for intent in knowledge_base:
                    if intent['tag'] == predicted_tag:
                        bot_response = random.choice(intent['responses'])
                        break
        
        if not bot_response:
            bot_response = "Sorry, I don't quite understand. Could you please rephrase?"

        return jsonify({"reply": bot_response})
        
    except Exception as e:
        print(f"Chatbot Error: {e}")
        traceback.print_exc()
        return jsonify({"reply": "I'm having a brain freeze. Please try again."})


# --- Server Start ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)