import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

const DashboardPage = () => {
  const [stats, setStats] = useState({ domains: {}, resolved_feedback: 0 });
  const [selectedDomain, setSelectedDomain] = useState(null);
  const [unresolvedFeedback, setUnresolvedFeedback] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Fetch feedback statistics on load
  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/feedback-stats`);
      setStats(response.data);
    } catch (err) {
      setError("Failed to load feedback stats.");
      console.error(err);
    }
  };

  // Fetch unresolved feedback for a selected domain
  const fetchUnresolvedFeedback = async (domain) => {
    setLoading(true);
    setSelectedDomain(domain);
    try {
      const response = await axios.get(`${API_URL}/unresolved-feedback/${domain}`);
      setUnresolvedFeedback(response.data);
    } catch (err) {
      setError("Failed to load unresolved feedback.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Mark feedback as resolved
  const handleResolveFeedback = async (id) => {
    try {
      await axios.put(`${API_URL}/resolve-feedback/${id}`);
      setUnresolvedFeedback((prev) => prev.filter((fb) => fb.id !== id));
      fetchStats(); // Refresh stats
    } catch (err) {
      setError("Failed to resolve feedback.");
      console.error(err);
    }
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold text-yellow-500 mb-4">Dashboard</h1>

      {/* Display Feedback Stats */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="p-4 bg-white shadow-md rounded-lg">
          <h2 className="text-xl font-semibold">Feedback by Domain</h2>
          {Object.entries(stats.domains).map(([domain, count]) => (
            <div key={domain} className="flex justify-between border-b py-2">
              <span>{domain}</span>
              <span>{count}</span>
              <button
                onClick={() => fetchUnresolvedFeedback(domain)}
                className="text-blue-500 hover:underline"
              >
                View Details
              </button>
            </div>
          ))}
        </div>

        <div className="p-4 bg-white shadow-md rounded-lg">
          <h2 className="text-xl font-semibold">Resolved Feedback</h2>
          <p className="text-2xl font-bold">{stats.resolved_feedback}</p>
        </div>
      </div>

      {/* Display Unresolved Feedback */}
      {selectedDomain && (
        <div className="mt-6 p-4 bg-white shadow-md rounded-lg">
          <h2 className="text-xl font-semibold text-red-500">
            Unresolved Feedback for {selectedDomain}
          </h2>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <div>
              {unresolvedFeedback.length > 0 ? (
                unresolvedFeedback.map((feedback) => (
                  <div key={feedback.id} className="border-b py-2">
                    <p className="text-gray-700">📝 {feedback.text}</p>
                    <p className="text-gray-600">📜 Summary: {feedback.summary}</p>
                    <p className="text-gray-600">⭐ Rating: {feedback.rating}</p>
                    <button
                      onClick={() => handleResolveFeedback(feedback.id)}
                      className="bg-green-500 text-white px-4 py-1 rounded-lg mt-2"
                    >
                      Mark as Resolved
                    </button>
                  </div>
                ))
              ) : (
                <p>No unresolved feedback.</p>
              )}
            </div>
          )}
        </div>
      )}

      {/* Error Message */}
      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
};

export default DashboardPage;
