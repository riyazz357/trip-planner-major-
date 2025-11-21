import { GoogleGenerativeAI } from "@google/generative-ai";

// ⚠️ IMPORTANT: Put your actual API Key here for now to get it working.
// Later, you can move it to a .env file (REACT_APP_GOOGLE_API_KEY).
const API_KEY = "AIzaSyCNomlpTnDJ2_yNjloTWDK5EevjRvJUTfg"; 

const genAI = new GoogleGenerativeAI(API_KEY);

export const generateItinerary = async (formData) => {
  try {
    // 1. Calculate Days
    const start = new Date(formData.start_date);
    const end = new Date(formData.end_date);
    const diffTime = Math.abs(end - start);
    const days = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1; 

    // 2. Build Prompt
    const prompt = `
      Act as an expert travel planner. Create a detailed ${days}-day itinerary for a trip to ${formData.destination} from ${formData.source}.
      Travelers: ${formData.adults} Adults, ${formData.children} Children.
      Budget: ${formData.budget}.
      Interests: ${formData.interests.join(', ')}.
      
      Format the response in HTML (use <h2> for days, <ul> for lists, <b> for highlights).
      Do not use markdown blocks. Just pure HTML content div structure.
    `;

    // 3. Call Gemini
    const model = genAI.getGenerativeModel({ model: "gemini-pro" });
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    
    return text;
    
  } catch (error) {
    console.error("Gemini Error:", error);
    throw error;
  }
};