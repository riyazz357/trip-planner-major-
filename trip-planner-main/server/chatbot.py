# import json
# import requests
# import tkinter as tk
# from tkinter import scrolledtext, messagebox
# import numpy as np
# from tensorflow import keras
# import pickle
# import re

# # OpenWeather API key and endpoint
# OPENWEATHER_API_KEY = "e2afbed5bf2ffd9aca5013ae32592340"  # Replace with your actual OpenWeather API key

# # Load necessary files (model, tokenizer, label encoder, intents)
# with open('csv.json') as file:
#     data = json.load(file)

# # Load trained model
# model = keras.models.load_model('chat_model.h5')

# # Load tokenizer object
# with open('tokenizer.pickle', 'rb') as handle:
#     tokenizer = pickle.load(handle)

# # Load label encoder object
# with open('label_encoder.pickle', 'rb') as enc:
#     lbl_encoder = pickle.load(enc)

# # Function to fetch travel recommendations from RapidAPI
# def get_travel_recommendations(location):
#     url = f"https://travel-advisor.p.rapidapi.com/locations/search"
#     querystring = {"query": location, "limit": "5", "offset": "0", "lang": "en_US", "currency": "USD"}
#     headers = {
#         "X-RapidAPI-Key": "094ee793a9msh94b7f6fa9f51542p12e65bjsn98e6ed0c75bd",  # Replace with your actual RapidAPI key
#         "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com",
#     }
#     response = requests.get(url, headers=headers, params=querystring)
#     if response.status_code == 200:
#         data = response.json()
#         results = data.get("data", [])
#         recommendations = "\n".join([item["result_object"]["name"] for item in results[:5]])
#         return recommendations if recommendations else "No recommendations found."
#     else:
#         return "Error fetching travel recommendations."

# # Function to fetch weather information for a location (using OpenWeather API)
# def get_weather(location):
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         weather_info = f"Weather in {location}:\n"
#         weather_info += f"Temperature: {data['main']['temp']}°C\n"
#         weather_info += f"Weather: {data['weather'][0]['description']}"
#         return weather_info
#     else:
#         return "Error fetching weather data."

# # Function to extract location from user input using regular expressions
# def extract_location(user_message):
#     # Match locations after keywords like 'travel to', 'weather in', 'recommend places for'
#     location_pattern = re.compile(r'(?:travel to|weather in|recommend places for|to|in)\s+([A-Za-z\s]+)')
#     match = location_pattern.search(user_message)
    
#     if match:
#         return match.group(1).strip()
#     else:
#         return None

# # Function to handle user input and bot response
# def get_response():
#     user_message = user_input.get()
#     if user_message.lower() == "quit":
#         root.quit()

#     # Display user's message
#     chat_history.config(state='normal')
#     user_label = tk.Label(chat_history, text=f"{user_message}", font=font_chat, fg="blue", anchor='w', padx=10, pady=5)
#     user_label.pack(anchor='e', padx=10, pady=5)  # Right-aligned for user
#     chat_history.yview(tk.END)
#     user_input.delete(0, tk.END)

#     # Handle travel-related queries
#     if "travel" in user_message.lower() or "recommend" in user_message.lower():
#         location = extract_location(user_message)
#         if location:
#             bot_response = get_travel_recommendations(location)
#         else:
#             bot_response = "Please specify a location for travel recommendations."
    
#     # Handle weather-related queries
#     elif "weather" in user_message.lower() or "forecast" in user_message.lower():
#         location = extract_location(user_message)
#         if location:
#             bot_response = get_weather(location)
#         else:
#             bot_response = "Please specify a location to get the weather information."

#     else:
#         # Use the TensorFlow model for other general queries
#         result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([user_message]), 
#                                                                              truncating='post', maxlen=20))
#         tag = lbl_encoder.inverse_transform([np.argmax(result)])

#         # Generate response based on the tag
#         for intent in data:
#             if intent['cleaned_query'] == user_message.lower():
#                 bot_response = intent['response']
#                 break
#         else:
#             bot_response = "Sorry, I don't understand your query. Try asking about travel or weather."

#     # Display bot's response
#     bot_label = tk.Label(chat_history, text=f"{bot_response}", font=font_chat, fg="green", anchor='w', padx=10, pady=5)
#     bot_label.pack(anchor='w', padx=10, pady=5)  # Left-aligned for chatbot
#     chat_history.yview(tk.END)
#     chat_history.config(state='disabled')

# # Initialize the Tkinter window
# root = tk.Tk()
# root.title("AI Travel Assistant")
# root.geometry("500x600")
# root.config(bg="#f5f5f5")

# # Set the font and styling
# font_header = ('Helvetica', 16, 'bold')
# font_chat = ('Helvetica', 12)
# font_input = ('Helvetica', 14)

# # Create a header label
# header_label = tk.Label(root, text="Welcome to Your Travel Assistant", font=font_header, bg="#4CAF50", fg="white", pady=10)
# header_label.pack(fill="x")

# # Create a scrolling text widget for the chat history
# chat_history = scrolledtext.ScrolledText(root, state='disabled', width=60, height=20, font=font_chat, bg="#f4f4f4", fg="#333333", wrap=tk.WORD, bd=2, relief="solid")
# chat_history.pack(padx=10, pady=10)

# # Create a text entry box for user input
# user_input = tk.Entry(root, width=60, font=font_input, bd=2, relief="solid", fg="#333333")
# user_input.pack(padx=10, pady=10)

# # Create a send button that calls the get_response function
# send_button = tk.Button(root, text="Send", width=20, font=('Helvetica', 12, 'bold'), fg="white", bg="#4CAF50", relief="solid", command=get_response)
# send_button.pack(pady=10)

# # Function to handle 'Quit' button
# def quit_chatbot():
#     if messagebox.askokcancel("Quit", "Do you want to exit the chatbot?"):
#         root.quit()

# # Add a quit button to exit the chatbot
# quit_button = tk.Button(root, text="Quit", width=20, font=('Helvetica', 12, 'bold'), fg="white", bg="#FF6347", relief="solid", command=quit_chatbot)
# quit_button.pack(pady=5)

# # Function to clear chat history
# def clear_chat():
#     chat_history.config(state='normal')
#     chat_history.delete(1.0, tk.END)
#     chat_history.config(state='disabled')

# # Add a clear button to reset the chat history
# clear_button = tk.Button(root, text="Clear", width=20, font=('Helvetica', 12, 'bold'), fg="white", bg="#FF4500", relief="solid", command=clear_chat)
# clear_button.pack(pady=5)

# # Add a help button to display common commands
# def show_help():
#     messagebox.showinfo("Help", "You can ask me about travel recommendations and weather.\nExamples:\n1. 'Travel to Paris'\n2. 'Weather in New York'\n3. 'Recommend places for sightseeing in Tokyo'")

# help_button = tk.Button(root, text="Help", width=20, font=('Helvetica', 12, 'bold'), fg="white", bg="#007BFF", relief="solid", command=show_help)
# help_button.pack(pady=5)

# # Start the Tkinter event loop
# root.mainloop()


import json
import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox
import numpy as np
from tensorflow import keras
import pickle
import re

# OpenWeather API key and endpoint
OPENWEATHER_API_KEY = "e2afbed5bf2ffd9aca5013ae32592340"  # Replace with your actual OpenWeather API key

# Load necessary files (model, tokenizer, label encoder, intents)
with open('csv.json') as file:
    data = json.load(file)

# Load trained model
model = keras.models.load_model('chat_model.h5')

# Load tokenizer object
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load label encoder object
with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

# Function to fetch travel recommendations from RapidAPI
def get_travel_recommendations(location):
    url = f"https://travel-advisor.p.rapidapi.com/locations/search"
    querystring = {"query": location, "limit": "5", "offset": "0", "lang": "en_US", "currency": "USD"}
    headers = {
        "X-RapidAPI-Key": "094ee793a9msh94b7f6fa9f51542p12e65bjsn98e6ed0c75bd",  # Replace with your actual RapidAPI key
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        results = data.get("data", [])
        recommendations = "\n".join([item["result_object"]["name"] for item in results[:5]])
        return recommendations if recommendations else "No recommendations found."
    else:
        return "Error fetching travel recommendations."

# Function to fetch weather information for a location (using OpenWeather API)
def get_weather(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = f"Weather in {location}:\n"
        weather_info += f"Temperature: {data['main']['temp']}\u00b0C\n"
        weather_info += f"Weather: {data['weather'][0]['description']}"
        return weather_info
    else:
        return "Error fetching weather data."

# Function to extract location from user input using regular expressions
def extract_location(user_message):
    location_pattern = re.compile(r'(?:travel to|weather in|recommend places for|to|in)\s+([A-Za-z\s]+)')
    match = location_pattern.search(user_message)
    
    if match:
        return match.group(1).strip()
    else:
        return None

# Function to handle user input and bot response
def get_response():
    user_message = user_input.get()
    if user_message.lower() == "quit":
        root.quit()

    # Display user's message
    chat_history.config(state='normal')
    chat_history.insert(tk.END, f"You: {user_message}\n")
    chat_history.yview(tk.END)
    user_input.delete(0, tk.END)

    # Handle travel-related queries
    if "travel" in user_message.lower() or "recommend" in user_message.lower():
        location = extract_location(user_message)
        if location:
            bot_response = get_travel_recommendations(location)
        else:
            bot_response = "Please specify a location for travel recommendations."
    
    # Handle weather-related queries
    elif "weather" in user_message.lower() or "forecast" in user_message.lower():
        location = extract_location(user_message)
        if location:
            bot_response = get_weather(location)
        else:
            bot_response = "Please specify a location to get the weather information."

    else:
        # Use the TensorFlow model for other general queries
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([user_message]), 
                                                                             truncating='post', maxlen=20))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])

        # Generate response based on the tag
        for intent in data:
            if intent['cleaned_query'] == user_message.lower():
                bot_response = intent['response']
                break
        else:
            bot_response = "Sorry, I don't understand your query. Try asking about travel or weather."

    # Display bot's response
    chat_history.insert(tk.END, f"Bot: {bot_response}\n")
    chat_history.yview(tk.END)
    chat_history.config(state='disabled')

# Initialize the Tkinter window
root = tk.Tk()
root.title("AI Travel Assistant")
root.geometry("600x700")
root.config(bg="#f5f5f5")

# Set the font and styling
font_header = ('Helvetica', 16, 'bold')
font_chat = ('Helvetica', 12)
font_input = ('Helvetica', 14)

# Create a header label
header_label = tk.Label(root, text="Welcome to Your Travel Assistant", font=font_header, bg="#4CAF50", fg="white", pady=10)
header_label.pack(fill="x")

# Create a scrolling text widget for the chat history
chat_history = scrolledtext.ScrolledText(root, state='disabled', width=60, height=20, font=font_chat, bg="#f4f4f4", fg="#333333", wrap=tk.WORD, bd=2, relief="solid")
chat_history.pack(padx=10, pady=10, fill="both", expand=True)

# Create a text entry box for user input
user_input = tk.Entry(root, width=60, font=font_input, bd=2, relief="solid", fg="#333333")
user_input.pack(padx=10, pady=10, fill="x")

# Create a send button that calls the get_response function
send_button = tk.Button(root, text="Send", width=20, font=('Helvetica', 12, 'bold'), fg="white", bg="#4CAF50", relief="solid", command=get_response)
send_button.pack(pady=10)

# Function to handle 'Quit' button
def quit_chatbot():
    if messagebox.askokcancel("Quit", "Do you want to exit the chatbot?"):
        root.quit()

# Add a quit button to exit the chatbot
quit_button = tk.Button(root, text="Quit", width=20, font=('Helvetica', 12, 'bold'), fg="white", bg="#FF6347", relief="solid", command=quit_chatbot)
quit_button.pack(pady=5)

# Function to clear chat history
def clear_chat():
    chat_history.config(state='normal')
    chat_history.delete(1.0, tk.END)
    chat_history.config(state='disabled')

# Add a clear button to reset the chat history
clear_button = tk.Button(root, text="Clear", width=20, font=('Helvetica', 12, 'bold'), fg="white", bg="#FF4500", relief="solid", command=clear_chat)
clear_button.pack(pady=5)

# Add a help button to display common commands
def show_help():
    messagebox.showinfo("Help", "You can ask me about travel recommendations and weather.\nExamples:\n1. 'Travel to Paris'\n2. 'Weather in New York'\n3. 'Recommend places for sightseeing in Tokyo'")

help_button = tk.Button(root, text="Help", width=20, font=('Helvetica', 12, 'bold'), fg="white", bg="#007BFF", relief="solid", command=show_help)
help_button.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()

