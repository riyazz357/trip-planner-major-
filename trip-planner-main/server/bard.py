import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

# Load environment variables
load_dotenv()
_api_key = os.environ.get("GOOGLE_API_KEY")

if _api_key:
    genai.configure(api_key=_api_key)

def generate_itinerary(source, destination, start_date, end_date, adults, children, budget, interests):
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        no_of_days = (end_dt - start_dt).days + 1
        if no_of_days <= 0: raise ValueError("Return date must be after start date.")
    except ValueError as e:
        raise ValueError(f"Invalid date: {e}")

    budget_map = {"low": "budget-friendly", "mid": "moderate", "high": "luxury"}
    budget_desc = budget_map.get(budget, "standard")
    interests_str = ", ".join(interests) if interests else "general sightseeing"

    prompt = (
        f"Create a detailed {no_of_days}-day itinerary for a trip from {source} to {destination} "
        f"for {adults} adults and {children} children. Budget: {budget_desc}. Interests: {interests_str}. "
        f"Include daily schedules (morning, afternoon, evening), specific restaurants, transport tips, and costs in INR. "
        f"Format with Markdown headings and bullet points. Do not repeat this prompt."
    )

    if not _api_key: raise EnvironmentError("Missing Google API Key.")

    try:
        # FIX: Use the 'gemini-pro' model which is the most widely compatible
        # If this fails, we will catch it below.
        model = genai.GenerativeModel("gemini-pro")
        
        # Generate content
        response = model.generate_content(prompt)
        
        if not response.text:
            raise ValueError("Empty response from AI.")
            
        return response.text

    except Exception as exc:
        logging.exception("Gemini Error: %s", exc)
        # If gemini-pro fails, try the older legacy model as a final fallback
        try:
            logging.info("Retrying with gemini-1.0-pro...")
            model = genai.GenerativeModel("gemini-1.0-pro")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e2:
             raise exc # Raise the original error if fallback also fails