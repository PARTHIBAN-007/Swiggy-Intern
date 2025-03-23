import React from "react";
import { BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Dashboard from "./Dashboard"; // Ensure correct path
import FeedbackPage from "./FeedbackPage"; // Ensure correct path

function App() {
  return (
    <Router>
      <div className="p-4 flex justify-between items-center bg-yellow-500 text-white">
        <h1 className="text-lg font-bold">Swiggy</h1>
      </div>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/feedback" element={<FeedbackPage />} />
      </Routes>
    </Router>
  );
}

export default App;
