import os
import json
import pickle
import random
import datetime
import requests
import bcrypt
import mistune
import numpy as np
from dotenv import load_dotenv
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import bard # Imports your logic from above

load_dotenv()
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # Allow React to connect
app.secret_key = SECRET_KEY or "dev_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- LAZY LOADING FOR CHATBOT (Prevents Memory Crash) ---
chat_resources = None
def load_chat_resources():
    global chat_resources
    if chat_resources: return chat_resources
    
    print("⏳ Loading AI Models...")
    import nltk
    from nltk.stem import WordNetLemmatizer
    from tensorflow import keras
    
    # Download NLTK data
    for res in ['punkt', 'punkt_tab', 'wordnet', 'omw-1.4']:
        try: nltk.data.find(f'tokenizers/{res}' if 'punkt' in res else f'corpora/{res}')
        except LookupError: nltk.download(res)

    chat_resources = {
        'model': keras.models.load_model('chat_model.h5'),
        'words': pickle.load(open('words.pickle', 'rb')),
        'classes': pickle.load(open('classes.pickle', 'rb')),
        'lemmatizer': WordNetLemmatizer()
    }
    
    # Load Knowledge Base
    kb = []
    kb.extend(json.load(open('intents.json'))['intents'])
    for item in json.load(open('csv.json')):
        kb.append({
            "tag": item['cleaned_query'].lower().replace(' ', '_') + "_info",
            "patterns": [item['cleaned_query']],
            "responses": [item['response']]
        })
    chat_resources['kb'] = kb
    return chat_resources

# --- User Model ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.String(200))

    def __init__(self, name, email, password, bio=""):
        self.name = name
        self.email = email
        self.bio = bio
        self.password = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode("utf8")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf8"), self.password.encode("utf8"))

with app.app_context():
    db.create_all()

# --- HELPER: Weather ---
def get_weather_data(location, start, end):
    if not WEATHER_API_KEY: return None
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start}/{end}?unitGroup=metric&include=days&key={WEATHER_API_KEY}&contentType=json"
    try:
        return requests.get(url, timeout=15).json()
    except:
        return None

# ================= API ROUTES =================

# 1. ITINERARY GENERATION (React JSON API)
@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary_api():
    data = request.get_json()
    
    # Get all fields
    source = data.get("source")
    destination = data.get("destination")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    budget = data.get("budget")
    interests = data.get("interests", [])
    
    try:
        adults = int(data.get("adults", 1))
        children = int(data.get("children", 0))
    except:
        adults, children = 1, 0

    # Get Weather
    weather = get_weather_data(destination, start_date, end_date) or {"days": []}

    # Generate Plan
    markdown_plan = bard.generate_itinerary(
        source, destination, start_date, end_date, 
        adults, children, budget, interests
    )
    
    return jsonify({
        "status": "success",
        "plan_html": mistune.html(markdown_plan), # Convert to HTML for React
        "weather_data": weather
    })

# 2. CHATBOT (Uses Lazy Loading)
@app.route('/chat', methods=['POST'])
def chat():
    res = load_chat_resources()
    msg = request.get_json().get("message", "")
    
    # Prediction logic
    import nltk # Import locally to use loaded lemmatizer
    sentence_words = nltk.word_tokenize(msg)
    sentence_words = [res['lemmatizer'].lemmatize(w.lower()) for w in sentence_words]
    
    bag = [1 if w in sentence_words else 0 for w in res['words']]
    pred = res['model'].predict(np.array([bag]), verbose=0)[0]
    
    # Filter results
    results = [[i, r] for i, r in enumerate(pred) if r > 0.25]
    results.sort(key=lambda x: x[1], reverse=True)
    
    tag = res['classes'][results[0][0]] if results else None
    response = "I'm not sure I understand."

    if tag:
        if tag == 'destination_recommendation':
            response = bard.get_chat_recommendations(msg)
        else:
            for i in res['kb']:
                if i['tag'] == tag:
                    response = random.choice(i['responses'])
                    break
                    
    return jsonify({"reply": response})

# 3. AUTH ROUTES
@app.route("/api/users/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "User exists"}), 400
    
    new_user = User(data['name'], data['email'], data['password'], data.get('bio'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id, "name": new_user.name}), 201

@app.route("/api/users/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        session['user_id'] = user.id
        return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)