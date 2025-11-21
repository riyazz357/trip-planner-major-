import os
import json
import pickle
import random
import datetime
import requests
import bcrypt
import mistune
import numpy as np
import traceback # Added for detailed error logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Import your AI logic
import bard 

# --- 1. Configuration & Setup ---
load_dotenv()
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)
# Enable CORS for all domains (easiest for debugging)
CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = SECRET_KEY or "dev_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- 2. Global Variables for Lazy Loading ---
chat_model = None
words = None
classes = None
knowledge_base = None
lemmatizer = None

# --- 3. Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.String(200))

    def __init__(self, name, email, password, bio=None):
        self.name = name
        self.email = email
        self.bio = bio
        self.password = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode("utf8")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf8"), self.password.encode("utf8"))

with app.app_context():
    db.create_all()

# --- 4. Helper Functions ---

# Weather Helper
def get_weather_data(api_key, location, start_date, end_date):
    if not api_key:
        print("⚠️ Weather API Key missing")
        return None
    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?unitGroup=metric&include=days&key={api_key}&contentType=json"
    try:
        print(f"☁️ Fetching weather for {location}...")
        response = requests.get(base_url, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Weather API Error: {e}")
        return None

# Lazy Load Chatbot Resources
def load_chatbot_resources():
    global chat_model, words, classes, knowledge_base, lemmatizer
    
    if chat_model is not None:
        return

    print("⏳ Loading Chatbot AI models (TensorFlow & NLTK)...")
    
    import nltk
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
        with open('intents.json') as file:
            knowledge_base.extend(json.load(file)['intents'])
        with open('csv.json') as file:
            for item in json.load(file):
                knowledge_base.append({
                    "tag": item['cleaned_query'].lower().replace(' ', '_') + "_info",
                    "patterns": [item['cleaned_query']],
                    "responses": [item['response']]
                })
        print("✅ Chatbot resources loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading chatbot files: {e}")


# ==========================================
#               API ROUTES
# ==========================================

# --- 1. Itinerary Generation Route (With Debug Logs) ---
@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary_api():
    print("🟢 RECEIVED REQUEST: /generate_itinerary")
    
    try:
        data = request.get_json()
        print(f"📝 Request Data: {data}")

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
            adults = 1
            children = 0

        if not all([source, destination, start_date, end_date]):
            print("❌ Validation Failed: Missing required fields")
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # Date Validation
        try:
            start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            if end_dt < start_dt:
                return jsonify({"status": "error", "message": "Return date cannot be before start date"}), 400
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid date format"}), 400

        # Get Weather
        print("⏳ Calling Weather API...")
        weather_data = get_weather_data(WEATHER_API_KEY, destination, start_date, end_date)
        if not weather_data:
            print("⚠️ Weather data failed, using empty fallback.")
            weather_data = {"resolvedAddress": destination, "days": []}
        else:
            print("✅ Weather API Success")

        # Generate Itinerary using Bard/Gemini
        print("⏳ Calling Gemini API (bard.py)...")
        plan_markdown = bard.generate_itinerary(
            source=source,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            adults=adults,
            children=children,
            budget=budget,
            interests=interests
        )
        print(f"✅ Gemini API Response Received (Length: {len(plan_markdown)})")
        
        # Convert markdown to HTML
        plan_html = mistune.html(plan_markdown)

        return jsonify({
            "status": "success",
            "plan_html": plan_html,
            "weather_data": weather_data
        })

    except Exception as e:
        print(f"🔴 CRITICAL ERROR in /generate_itinerary: {e}")
        # Print the full traceback to logs so we know EXACTLY where it crashed
        traceback.print_exc()
        return jsonify({"status": "error", "message": f"Server Error: {str(e)}"}), 500


# --- 2. Chatbot Route ---
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

    # Local Helper Functions to access loaded resources
    import nltk
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
            if predicted_tag == 'destination_recommendation':
                 try:
                     bot_response = bard.get_chat_recommendations(user_message)
                 except AttributeError:
                     bot_response = "I recommend visiting the city center!"
            else:
                for intent in knowledge_base:
                    if intent['tag'] == predicted_tag:
                        bot_response = random.choice(intent['responses'])
                        break
        
        if not bot_response:
            bot_response = "Sorry, I don't quite understand. Could you please rephrase?"

        return jsonify({"reply": bot_response})
        
    except Exception as e:
        print(f"Chatbot Error: {e}")
        return jsonify({"reply": "I'm having a brain freeze. Please try again."})


# --- 3. Auth Routes ---
@app.route("/api/users/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        bio = data.get("bio", "")

        if not all([name, email, password]):
            return jsonify({"message": "Please fill all fields"}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400

        new_user = User(name=name, email=email, password=password, bio=bio)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "bio": new_user.bio
        }), 201
    except Exception as e:
        print(f"Register Error: {e}")
        return jsonify({"message": "Server Error"}), 500

@app.route("/api/users/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            return jsonify({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "bio": user.bio
            }), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Login Error: {e}")
        return jsonify({"message": "Server Error"}), 500

@app.route("/api/users/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200


# --- Server Start ---
if __name__ == "__main__":
    # Use Render's PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)