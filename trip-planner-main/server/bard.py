import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Prefer the official GOOGLE_API_KEY
_api_key = os.environ.get("GOOGLE_API_KEY")

# Configure if available; otherwise we'll handle gracefully at call time
if _api_key:
    genai.configure(api_key=_api_key)

def generate_itinerary(source: str, destination: str, start_date: str, end_date: str, 
                       adults: int, children: int, budget: str, interests: list) -> str:
    """Generate a travel itinerary using Google's Gemini model.

    Returns markdown formatted text suitable for rendering on the dashboard.
    Raises exceptions on failure so the caller knows something went wrong.
    """

    # --- 1. Calculate Days ---
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        no_of_days = (end_dt - start_dt).days + 1
        
        if no_of_days <= 0:
            raise ValueError("Return date must be after the travel date.")
    except ValueError as e:
        # Re-raise value errors about dates
        raise ValueError(f"Invalid date format or range: {e}")

    # --- 2. Build Prompt ---
    # Map budget to descriptive terms
    budget_map = {"low": "budget-friendly", "mid": "moderate/mid-range", "high": "luxury"}
    budget_desc = budget_map.get(budget, "standard")
    
    interests_str = ", ".join(interests) if interests else "general sightseeing"

    prompt = (
        f"You are an expert travel consultant specializing in {destination}. "
        f"Create a detailed {no_of_days}-day travel itinerary for a trip from {source} to {destination} "
        f"starting on {start_date} and ending on {end_date}. \n\n"
        f"**Traveler Details:**\n"
        f"- Party: {adults} Adults, {children} Children\n"
        f"- Budget Style: {budget_desc}\n"
        f"- Interests: {interests_str}\n\n"
        f"**Itinerary Requirements:**\n"
        f"1. **Daily Schedule:** Morning, Afternoon, and Evening activities. Include specific names of places.\n"
        f"2. **Dining:** Recommend specific restaurants (one budget, one mid-range/fine dining per day) that fit the location.\n"
        f"3. **Logistics:** Practical tips on local transport (metro, cab, walking).\n"
        f"4. **Budget Estimates:** Approximate daily costs in INR.\n"
        f"5. **Formatting:** Use clear Markdown with bold headings (## Day 1: ...), bullet points, and bold text for key attractions.\n\n"
        f"IMPORTANT: Do not repeat the user's question. Start directly with the itinerary title."
    )

    # --- 3. Validation ---
    if not _api_key:
        raise EnvironmentError("Missing Google API Key in environment variables.")

    # --- 4. Call AI Model ---
    try:
        # Use a stable model version
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(prompt)
        text = getattr(response, "text", "")

        if not text:
            # Raise an error if the model returns nothing (e.g., safety filter blocks it)
            raise ValueError("Gemini API returned an empty response.")
            
        return text

    except Exception as exc:
        # Log the detailed error for the developer
        logging.exception("Gemini itinerary generation failed: %s", exc)
        # Re-raise the exception so app.py catches it and returns a 500 error
        raise exc


def get_chat_recommendations(location: str) -> str:
    """
    Generates a high-quality, summarized travel recommendation for the chatbot.
    """
    prompt = (
        f"You are a helpful travel assistant. A user is asking about {location}. "
        f"Provide a brief, engaging summary of the top 3 must-see attractions. "
        f"Use markdown bullet points. Keep it under 150 words."
    )

    if not _api_key:
        return "I'm sorry, but I can't access my AI brain right now (API Key missing)."

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        text = getattr(response, "text", "")
        if not text: 
            return "I couldn't think of a good answer right now. Ask me again!"
        return text
    except Exception as exc:
        logging.exception("Gemini chat failed: %s", exc)
        return "I'm having trouble connecting to the server. Please try again later."