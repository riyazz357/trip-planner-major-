// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { ToastContainer, toast } from "react-toastify";
// import axios from "axios";
// import "react-toastify/dist/ReactToastify.css";
// import "./generate.scss";

// const Generate = () => {
//   const [source, setSource] = useState("");
//   const [destination, setDestination] = useState("");
//   const [date, setDate] = useState("");
//   const [returnDate, setReturnDate] = useState("");
//   const [budget, setBudget] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [itinerary, setItinerary] = useState(null); // Updated state for itinerary
//   const navigate = useNavigate();

//   // Handle form submission
//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     if (!source || !destination || !date || !returnDate || !budget) {
//       toast.error("Please fill in all fields!");
//       return;
//     }

//     setLoading(true);

//     try {
//       // Send POST request to the backend to generate the itinerary
//       const response = await axios.post("http://localhost:5000/generate-itinerary", {
//         source,
//         destination,
//         start_date: date,
//         end_date: returnDate,
//         budget,
//       });

//       // Handle the response from the backend
//       setItinerary(response.data.itinerary); // Assuming response contains 'itinerary'
//       setLoading(false);
//       toast.success("Itinerary Generated Successfully!");
//     } catch (error) {
//       setLoading(false);
//       toast.error("Error generating itinerary. Please try again.");
//       console.error(error);
//     }
//   };

//   return (
//     <>
//       <div className="container">
//         <div className="form-container">
//           <h1 className="text-center mb-4">Generate Your Travel Itinerary</h1>
//           <form onSubmit={handleSubmit}>
//             <div className="form-group">
//               <label htmlFor="source">From</label>
//               <input
//                 type="text"
//                 className="form-control"
//                 id="source"
//                 placeholder="Enter your starting point"
//                 value={source}
//                 onChange={(e) => setSource(e.target.value)}
//                 required
//               />
//             </div>

//             <div className="form-group">
//               <label htmlFor="destination">To</label>
//               <input
//                 type="text"
//                 className="form-control"
//                 id="destination"
//                 placeholder="Enter your destination"
//                 value={destination}
//                 onChange={(e) => setDestination(e.target.value)}
//                 required
//               />
//             </div>

//             <div className="form-row">
//               <div className="col">
//                 <div className="form-group">
//                   <label htmlFor="date">Travel Date</label>
//                   <input
//                     type="date"
//                     className="form-control"
//                     id="date"
//                     value={date}
//                     onChange={(e) => setDate(e.target.value)}
//                     required
//                   />
//                 </div>
//               </div>

//               <div className="col">
//                 <div className="form-group">
//                   <label htmlFor="return">Return Date</label>
//                   <input
//                     type="date"
//                     className="form-control"
//                     id="return"
//                     value={returnDate}
//                     onChange={(e) => setReturnDate(e.target.value)}
//                     required
//                   />
//                 </div>
//               </div>
//             </div>

//             <div className="form-group">
//               <label htmlFor="budget">Budget</label>
//               <input
//                 type="number"
//                 className="form-control"
//                 id="budget"
//                 placeholder="Enter your budget"
//                 value={budget}
//                 onChange={(e) => setBudget(e.target.value)}
//                 required
//               />
//             </div>

//             <button
//               type="submit"
//               className="btn btn-primary btn-lg btn-block mt-3"
//               disabled={loading}
//             >
//               {loading ? "Generating..." : "Generate Itinerary"}
//             </button>
//           </form>
//         </div>

//         {loading && (
//           <img
//             src="https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif"
//             alt="Loading..."
//             className="loading-spinner"
//           />
//         )}

//         {/* Display generated itinerary if available */}
//         {itinerary && (
//           <div className="itinerary-result">
//             <h2>Your Personalized Itinerary</h2>
//             {itinerary.itinerary && itinerary.itinerary.length > 0 ? (
//               <div>
//                 {itinerary.itinerary.map((day, index) => (
//                   <div key={index} className="itinerary-day">
//                     <h3>{day.day}</h3>
//                     <ul>
//                       {day.activities.map((activity, idx) => (
//                         <li key={idx}>{activity.activity}</li>
//                       ))}
//                     </ul>
//                   </div>
//                 ))}
//               </div>
//             ) : (
//               <p>No itinerary available.</p>
//             )}
//           </div>
//         )}
//       </div>

//       <ToastContainer />
//     </>
//   );
// };

// export default Generate;
// import React from "react";
// import { ToastContainer } from "react-toastify";
// import "react-toastify/dist/ReactToastify.css";
// import "./generate.scss";

// const Generate = () => {
//   // Redirect to the specified URL when the button is clicked
//   const handleRedirect = () => {
//     window.location.href = "http://127.0.0.1:5001/";
//   };

//   return (
//     <>
//       <div className="container">
//         <div className="form-container text-center">
//           <h1 className="mb-4">Generate Your Travel Itinerary</h1>
//           <button
//             type="button"
//             className="btn btn-primary btn-lg"
//             onClick={handleRedirect}
//           >
//             Generate
//           </button>
//         </div>
//       </div>
//       <ToastContainer />
//     </>
//   );
// };

// export default Generate;

/*
import React from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./generate.scss";

const Generate = () => {
  // Redirect to the specified URL when the button is clicked
  const handleRedirect = () => {
    window.location.href = "https://ai-travel-itinerary-generator-wvuw.onrender.com";
  };

  return (
    <>
      <div className="container">
        <div className="form-container text-center">
          <h1 className="mb-4">Generate Your Travel Itinerary</h1>
          <p className="mb-4">
            Plan your next trip with ease! Just click the button below to get
            a personalized travel itinerary based on your preferences. You'll
            receive recommendations for the best places to visit, where to stay,
            and things to do.
          </p>
          <button
            type="button"
            className="btn btn-primary btn-lg"
            onClick={handleRedirect}
          >
            Generate
          </button>
        </div>
      </div>
      <ToastContainer />
    </>
  );
};

export default Generate;
*/




// import React, { useState } from "react";
// import { toast } from "react-toastify";
// import { generateItinerary } from "../../services/gemini"; // Ensure this path is correct
// import "react-toastify/dist/ReactToastify.css";
// import "./generate.scss"; 

// const Generate = () => {
//   const [formData, setFormData] = useState({
//     source: "",
//     destination: "",
//     start_date: "",
//     end_date: "",
//     adults: 1,
//     children: 0,
//     budget: "mid",
//     interests: [],
//   });

//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setFormData((prev) => ({ ...prev, [name]: value }));
//   };

//   const handleInterestChange = (e) => {
//     const { value, checked } = e.target;
//     setFormData((prev) => {
//       if (checked) {
//         return { ...prev, interests: [...prev.interests, value] };
//       } else {
//         return { ...prev, interests: prev.interests.filter((i) => i !== value) };
//       }
//     });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setLoading(true);
//     setResult(null);

//     try {
//       // 1. Call the Gemini Service directly
//       const itineraryHtml = await generateItinerary(formData);
      
//       // 2. Set the result state with just the plan
//       setResult({ plan_html: itineraryHtml });
//       toast.success("Itinerary generated successfully!");
      
//     } catch (error) {
//       console.error("Generation Error:", error);
//       toast.error("Failed to generate plan. Please check your API Key.");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="container generate-page">
//       <div className="form-container">
//         <h2 className="text-center mb-4">Plan Your Trip</h2>
        
//         <form onSubmit={handleSubmit}>
//           {/* --- Form Fields (Same as before) --- */}
//           <div className="row mb-3">
//             <div className="col-md-6">
//               <label className="form-label">From</label>
//               <input type="text" className="form-control" name="source" value={formData.source} onChange={handleChange} required placeholder="e.g. Mumbai" />
//             </div>
//             <div className="col-md-6">
//               <label className="form-label">To</label>
//               <input type="text" className="form-control" name="destination" value={formData.destination} onChange={handleChange} required placeholder="e.g. Paris" />
//             </div>
//           </div>

//           <div className="row mb-3">
//             <div className="col-md-6">
//               <label className="form-label">Start Date</label>
//               <input type="date" className="form-control" name="start_date" value={formData.start_date} onChange={handleChange} required />
//             </div>
//             <div className="col-md-6">
//               <label className="form-label">End Date</label>
//               <input type="date" className="form-control" name="end_date" value={formData.end_date} onChange={handleChange} required />
//             </div>
//           </div>

//           <div className="row mb-3">
//             <div className="col-md-4">
//               <label className="form-label">Adults</label>
//               <input type="number" className="form-control" name="adults" min="1" value={formData.adults} onChange={handleChange} />
//             </div>
//             <div className="col-md-4">
//               <label className="form-label">Children</label>
//               <input type="number" className="form-control" name="children" min="0" value={formData.children} onChange={handleChange} />
//             </div>
//             <div className="col-md-4">
//               <label className="form-label">Budget</label>
//               <select className="form-select" name="budget" value={formData.budget} onChange={handleChange}>
//                 <option value="low">Budget-Friendly</option>
//                 <option value="mid">Mid-Range</option>
//                 <option value="high">Luxury</option>
//               </select>
//             </div>
//           </div>

//           <div className="mb-3">
//             <label className="form-label">Interests</label>
//             <div className="d-flex gap-3 flex-wrap">
//               {["Adventure", "Culture", "Food", "Relaxation"].map((interest) => (
//                 <div className="form-check" key={interest}>
//                   <input className="form-check-input" type="checkbox" value={interest} onChange={handleInterestChange} id={`check-${interest}`} />
//                   <label className="form-check-label" htmlFor={`check-${interest}`}>{interest}</label>
//                 </div>
//               ))}
//             </div>
//           </div>

//           <div className="text-center">
//             <button type="submit" className="btn btn-primary btn-lg" disabled={loading}>
//               {loading ? "Generating..." : "Generate Itinerary"}
//             </button>
//           </div>
//         </form>
//       </div>

//       {/* --- RESULTS SECTION --- */}
//       {result && (
//         <div className="result-container mt-5">
//           <h3 className="text-center mb-4">Your Trip to {formData.destination}</h3>
          
//           {/* Removed Weather Section for now to prevent crashes */}
//           {/* Add it back here if you implement a separate weather API call */}

//           <div className="card">
//             <div className="card-body itinerary-body">
//               {/* Render the HTML directly */}
//               <div dangerouslySetInnerHTML={{ __html: result.plan_html }} />
//             </div>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default Generate;

//  '''
import React, { useState } from "react";
import { toast } from "react-toastify";
import ReactQuill from 'react-quill'; // 1. Import Editor
import 'react-quill/dist/quill.snow.css'; // 1. Import Editor Styles
import { generateItinerary } from "../../services/gemini";
import { getWeather } from "../../services/weather";
import "react-toastify/dist/ReactToastify.css";
import "./generate.scss"; 

const Generate = () => {
  const [view, setView] = useState('start'); 
  
  // This state will hold the Editable HTML content
  const [editableContent, setEditableContent] = useState(""); 
  
  const [formData, setFormData] = useState({
    source: "", destination: "", start_date: "", end_date: "",
    adults: 1, children: 0, budget: "mid", interests: [],
  });
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(false);

  // ... (Keep handleChange, handleInterestChange, handleStartClick, handleReset) ...
  // (Re-paste them from previous code if needed)
  const handleChange = (e) => {
      const { name, value } = e.target;
      setFormData((prev) => ({ ...prev, [name]: value }));
  };
  const handleInterestChange = (e) => {
    const { value, checked } = e.target;
    setFormData((prev) => {
      if (checked) return { ...prev, interests: [...prev.interests, value] };
      return { ...prev, interests: prev.interests.filter((i) => i !== value) };
    });
  };
  const handleStartClick = () => setView('form');
  const handleReset = () => { setView('start'); setEditableContent(""); setWeatherData(null); };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const [itineraryHtml, weather] = await Promise.all([
        generateItinerary(formData),
        getWeather(formData.destination, formData.start_date, formData.end_date)
      ]);
      
      // 2. Set the content into the Editor State
      setEditableContent(itineraryHtml);
      setWeatherData(weather);
      
      setView('result');
      toast.success("Trip planned successfully!");

    } catch (error) {
      console.error("Error:", error);
      toast.error("Something went wrong. Please check your connection.");
    } finally {
      setLoading(false);
    }
  };

  // Function to handle saving the edited plan (e.g., print or save to DB later)
  const handleSaveOrPrint = () => {
      window.print();
  };

  return (
    <div className="container generate-page">
      
      {/* VIEW 1 & 2 (Start & Form) - SAME AS BEFORE */}
      {view === 'start' && (
          <div className="start-container text-center">
            <h1 className="display-4 mb-4">Plan Your Dream Trip</h1>
            <p className="lead mb-5">Get a personalized itinerary powered by AI.</p>
            <button className="btn btn-primary btn-lg px-5" onClick={handleStartClick}>Start Planning</button>
          </div>
      )}

      {view === 'form' && (
        <div className="form-container fade-in">
             {/* ... (Keep your existing form code here exactly as is) ... */}
             <h2 className="text-center mb-4">Trip Details</h2>
             <form onSubmit={handleSubmit}>
                 <div className="row mb-3">
                    <div className="col-md-6">
                    <label className="form-label">From</label>
                    <input type="text" className="form-control" name="source" value={formData.source} onChange={handleChange} required />
                    </div>
                    <div className="col-md-6">
                    <label className="form-label">To</label>
                    <input type="text" className="form-control" name="destination" value={formData.destination} onChange={handleChange} required />
                    </div>
                </div>
                <div className="row mb-3">
                    <div className="col-md-6">
                    <label className="form-label">Start Date</label>
                    <input type="date" className="form-control" name="start_date" value={formData.start_date} onChange={handleChange} required />
                    </div>
                    <div className="col-md-6">
                    <label className="form-label">End Date</label>
                    <input type="date" className="form-control" name="end_date" value={formData.end_date} onChange={handleChange} required />
                    </div>
                </div>
                 <div className="row mb-3">
                    <div className="col-md-4">
                    <label className="form-label">Adults</label>
                    <input type="number" className="form-control" name="adults" min="1" value={formData.adults} onChange={handleChange} />
                    </div>
                    <div className="col-md-4">
                    <label className="form-label">Children</label>
                    <input type="number" className="form-control" name="children" min="0" value={formData.children} onChange={handleChange} />
                    </div>
                    <div className="col-md-4">
                    <label className="form-label">Budget</label>
                    <select className="form-select" name="budget" value={formData.budget} onChange={handleChange}>
                        <option value="low">Budget-Friendly</option>
                        <option value="mid">Mid-Range</option>
                        <option value="high">Luxury</option>
                    </select>
                    </div>
                </div>
                <div className="mb-3">
                    <label className="form-label">Interests</label>
                    <div className="d-flex gap-3 flex-wrap">
                    {["Adventure", "Culture", "Food", "Relaxation"].map((interest) => (
                        <div className="form-check" key={interest}>
                        <input className="form-check-input" type="checkbox" value={interest} onChange={handleInterestChange} id={`check-${interest}`} />
                        <label className="form-check-label" htmlFor={`check-${interest}`}>{interest}</label>
                        </div>
                    ))}
                    </div>
                </div>
                 <div className="text-center mt-4">
                    <button type="submit" className="btn btn-primary btn-lg" disabled={loading}>
                        {loading ? "Generating..." : "Generate Itinerary"}
                    </button>
                 </div>
             </form>
        </div>
      )}


      {/* VIEW 3: RESULT SCREEN (Editable) */}
      {view === 'result' && (
        <div className="result-container fade-in">
          <div className="d-flex justify-content-between align-items-center mb-4">
            <h3>Your Trip to {formData.destination}</h3>
            <button className="btn btn-outline-primary" onClick={handleReset}>Plan Another Trip</button>
          </div>
          
          {/* Weather Section */}
          {weatherData && weatherData.days && (
            <div className="card mb-4 shadow-sm">
              <div className="card-header bg-info text-white">
                <h5 className="mb-0">Weather Forecast</h5>
              </div>
              <div className="card-body">
                <div className="d-flex flex-row overflow-auto pb-2" style={{ gap: '15px' }}>
                  {weatherData.days.slice(0, 5).map((day, index) => (
                    <div key={index} className="text-center p-2 border rounded" style={{ minWidth: '120px', background: '#f8f9fa' }}>
                      <div style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>{day.datetime}</div>
                      <div className="my-2" style={{ fontSize: '1.5rem' }}>{Math.round(day.tempmax)}°C</div>
                      <div className="text-muted" style={{ fontSize: '0.85rem' }}>{day.conditions}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* --- EDITABLE ITINERARY SECTION --- */}
          <div className="card shadow-sm">
            <div className="card-header bg-white">
                <h5 className="mb-0">Itinerary & Expenses (Editable)</h5>
            </div>
            <div className="card-body p-0">
              {/* React Quill Editor */}
              <ReactQuill 
                theme="snow" 
                value={editableContent} 
                onChange={setEditableContent}
                modules={{
                    toolbar: [
                        [{ 'header': [1, 2, false] }],
                        ['bold', 'italic', 'underline'],
                        [{'list': 'ordered'}, {'list': 'bullet'}],
                        ['clean']
                    ],
                }}
              />
            </div>
          </div>
          
          <div className="text-center mt-4">
             <button className="btn btn-success btn-lg" onClick={handleSaveOrPrint}>Print / Save as PDF</button>
          </div>
        </div>
      )}

    </div>
  );
};

export default Generate;