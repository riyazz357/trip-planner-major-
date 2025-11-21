import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
_api_key = os.environ.get("GOOGLE_API_KEY")

if _api_key:
    genai.configure(api_key=_api_key)

# accepts ALL the detailed inputs
def generate_itinerary(
    source: str, destination: str, start_date: str, end_date: str, 
    adults: int, children: int, budget: str, interests: list
) -> str:
    
    # 1. Calculate Days
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        no_of_days = (end_dt - start_dt).days + 1
        if no_of_days <= 0: return "Error: Return date must be after start date."
    except ValueError:
        return "Error: Invalid date format."

    # 2. Build Detailed Prompt
    prompt = (
        f"You are an expert travel consultant. Create a detailed {no_of_days}-day itinerary "
        f"for a trip from {source} to {destination} ({start_date} to {end_date}).\n"
        f"Travelers: {adults} Adults, {children} Children.\n"
        f"Budget: {budget} (Optimize costs in INR).\n"
        f"Interests: {', '.join(interests)}.\n\n"
        f"Include: Daily schedule (Morning, Afternoon, Evening), specific restaurants (1 budget, 1 mid-range), "
        f"transport tips, and daily cost estimates.\n"
        f"Format using clear Markdown with bold headings and bullet points."
    )

    if not _api_key: return "Missing Gemini API Key."

    try:
        # Use a stable model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return getattr(response, "text", "No response generated.")
    except Exception as e:
        logging.exception("Gemini Error: %s", e)
        return "Itinerary generation failed. Please check server logs."

def get_chat_recommendations(location: str) -> str:
    if not _api_key: return "AI Key missing."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Give 3 fun, brief things to do in {location}.")
        return response.text
    except Exception:
        return "Sorry, I couldn't connect to the AI right now."