import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Load environment variables
load_dotenv()

# Prefer the official GOOGLE_API_KEY
_api_key = os.environ.get("GOOGLE_API_KEY")

# Configure if available
if _api_key:
    genai.configure(api_key=_api_key)

def generate_itinerary(source: str, destination: str, start_date: str, end_date: str, 
                       adults: int, children: int, budget: str, interests: list) -> str:
    """Generate a travel itinerary using Google's Gemini model (v1 API)."""

    # --- 1. Calculate Days ---
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        no_of_days = (end_dt - start_dt).days + 1
        
        if no_of_days <= 0:
            raise ValueError("Return date must be after the travel date.")
    except ValueError as e:
        raise ValueError(f"Invalid date format or range: {e}")

    # --- 2. Build Prompt ---
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

    # --- 4. Call AI Model (FORCED CONFIGURATION) ---
    try:
        # Explicitly set generation config to avoid defaults
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }

        # Use the most stable model available globally
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config
        )
        
        response = model.generate_content(prompt)
        
        # Check if response was blocked safely
        if response.prompt_feedback and response.prompt_feedback.block_reason:
            raise ValueError(f"Blocked by safety filter: {response.prompt_feedback.block_reason}")

        text = getattr(response, "text", "")

        if not text:
            raise ValueError("Gemini API returned an empty response.")
            
        return text

    except Exception as exc:
        logging.exception("Gemini itinerary generation failed: %s", exc)
        # Raise the exception so app.py catches it and logs the detailed error
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
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return getattr(response, "text", "I'm sorry, I couldn't think of anything right now.")
    except Exception as exc:
        logging.exception("Gemini chat failed: %s", exc)
        return "I'm having trouble connecting to the server. Please try again later."