import { GoogleGenerativeAI } from "@google/generative-ai";

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
      1. Return ONLY valid HTML code. Do NOT use markdown blocks.
      2. Use <h2> for Day titles (e.g., "Day 1: Arrival").
      3. Use <ul> for activity lists.
      4. Use <strong> for emphasis.
      
      EXPENSES SECTION:
      At the very end, create a separate section titled "<h2>Estimated Expenses (INR)</h2>".
      Create an HTML <table> with the following columns: Category (Food, Transport, Activities, Misc), Estimated Daily Cost, and Total Trip Cost.
      Sum it up at the bottom.
    `;

    const model = genai.getGenerativeModel({ model: "gemini-2.0-flash" });
    const result = await model.generateContent(prompt);
    const response = await result.response;
    let text = response.text();
    
    // Cleanup markdown if present
    text = text.replace(/```html/g, '').replace(/```/g, '');
    
    return text;
    
  } catch (error) {
    console.error("Gemini Error:", error);
    throw error;
  }
};