import React, { useState } from "react";
import axios from "axios";

const FeedbackPage = () => {
  const [feedback, setFeedback] = useState("");
  const [summary, setSummary] = useState("");
  const [rating, setRating] = useState("");
  const [domain, setDomain] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [listening, setListening] = useState(false);

  // Check for browser speech recognition support
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = SpeechRecognition ? new SpeechRecognition() : null;

  const handleVoiceInput = () => {
    if (!recognition) {
      alert("Speech Recognition not supported in this browser.");
      return;
    }

    recognition.lang = "en-US";
    recognition.start();
    setListening(true);

    recognition.onresult = (event) => {
      setFeedback(event.results[0][0].transcript);
      setListening(false);
    };

    recognition.onerror = () => {
      setListening(false);
      setError("Speech recognition error. Please try again.");
    };
  };

  // Function to summarize feedback
  const handleSummarize = async () => {
    if (!feedback.trim()) {
      setError("Please provide some feedback before summarizing.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await axios.post("http://localhost:8000/summarize", {
        text: feedback,
      });

      console.log("API Response:", response.data);

        setSummary(response.data.summary);  // Correct key
        setRating(response.data.rating);
        setDomain(response.data.domain);

    } catch (err) {
      console.error("Error:", err);
      setError("Failed to summarize feedback. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Function to submit final feedback to the database
  const handleFinalSubmit = async () => {
    if (!summary) {
      setError("Please generate a summary before uploading.");
      return;
    }

    setUploading(true);
    setError("");

    try {
      const response = await axios.post("http://localhost:8000/final-feedback", {
        text: feedback,
        summary: summary,
        rating: rating,
        domain: domain,
      });

      alert(response.data.message);
    } catch (err) {
      console.error("Error:", err);
      setError("Failed to submit feedback. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen flex flex-col items-center">
      <h1 className="text-3xl font-bold text-orange-500 mb-4">Provide Feedback</h1>

      {error && <p className="text-red-600">{error}</p>}

      <textarea
        value={feedback}
        onChange={(e) => setFeedback(e.target.value)}
        placeholder="Type your feedback or use voice input"
        className="border p-2 w-full max-w-lg mb-2 rounded-lg"
      />

      <div className="flex space-x-2">
        <button
          onClick={handleVoiceInput}
          className="bg-yellow-400 text-white px-4 py-2 rounded-lg"
        >
          {listening ? "Listening..." : "Use Voice Input"}
        </button>

        <button
          onClick={handleSummarize}
          className="bg-yellow-500 text-white px-4 py-2 rounded-lg"
          disabled={loading}
        >
          {loading ? "Summarizing..." : "Summarize"}
        </button>
      </div>

      {summary && (
        <div className="mt-4 p-4 bg-white shadow-md rounded-lg border-l-4 border-blue-500 w-full max-w-lg">
          <h2 className="text-xl font-semibold text-blue-500">Summary</h2>
          <textarea value={summary} className="border p-2 w-full mb-2 rounded-lg" readOnly />
          <p className="text-gray-600">Rating: {rating}</p>
          <p className="text-gray-600">Domain: <strong>{domain}</strong></p>

          <button
            onClick={handleFinalSubmit}
            className="bg-yellow-600 text-black px-4 py-2 rounded-lg mt-2"
            disabled={uploading}
          >
            {uploading ? "Uploading..." : "Upload Review"}
          </button>
        </div>
      )}
    </div>
  );
};

export default FeedbackPage;
