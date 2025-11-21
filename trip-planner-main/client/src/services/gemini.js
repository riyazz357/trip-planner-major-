// src/services/gemini.js
import { GoogleGenerativeAI } from "@google/generative-ai";

// Ideally use an environment variable here
const API_KEY = "AIzaSyCNomlpTnDJ2_yNjloTWDK5EevjRvJUTfg"; 
const genAI = new GoogleGenerativeAI(API_KEY);

export const generateItinerary = async (formData) => {
  try {
    const start = new Date(formData.start_date);
    const end = new Date(formData.end_date);
    const diffTime = Math.abs(end - start);
    const days = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1; 

    const prompt = `
      Act as an expert travel planner. Create a detailed ${days}-day itinerary for a trip to ${formData.destination} from ${formData.source}.
      Travelers: ${formData.adults} Adults, ${formData.children} Children.
      Budget: ${formData.budget}.
      Interests: ${formData.interests.join(', ')}.
      
      CRITICAL FORMATTING INSTRUCTIONS:
      1. Return ONLY valid HTML code. 
      2. Do NOT wrap the output in markdown code blocks (like '''html or ''').
      3. Use <h2> for Day titles, <ul> for lists, and <strong> for emphasis.
      4. Use Bootstrap classes if possible (e.g., class="mb-3").
      5. Do not include <html>, <head>, or <body> tags. Just the content divs.
    `;

    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });
    const result = await model.generateContent(prompt);
    const response = await result.response;
    let text = response.text();
    
    // CLEANUP: Just in case the AI still adds markdown blocks, remove them manually
    text = text.replace(/```html/g, '').replace(/```/g, '');
    
    return text;
    
  } catch (error) {
    console.error("Gemini Error:", error);
    throw error;
  }
};