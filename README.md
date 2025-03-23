# Feedback Management System

## Project Objective
The objective of this project is to develop a **Feedback Management System** that allows users to submit feedback, automatically summarize it using AI, categorize it into different domains, and store it in a database. The system also provides functionalities to retrieve, analyze, and manage feedback efficiently.

## Tech Stack
- **Backend:** FastAPI, SQLite, LangChain, HuggingFace API, Pydantic
- **Frontend:** React, Axios, Tailwind CSS
- **Database:** SQLite
- **AI Model:** DeepSeek AI (HuggingFace)

## Functionalities
1. **Submit Feedback:** Users can enter feedback manually or via voice input.
2. **Summarization & Classification:** AI generates a summary, assigns a rating, and categorizes feedback.
3. **Storage in Database:** Feedback is stored with its summary, rating, and domain.
4. **Fetch Feedback Statistics:** Get a count of feedback per category and the number of resolved feedback.
5. **Retrieve Unresolved Feedback:** View pending feedback grouped by domain.
6. **Resolve Feedback:** Mark feedback as resolved once addressed.

## Setup and Run Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- SQLite
- HuggingFace API Key (for AI processing)

### Backend Setup
1. Clone the repository:
   ```sh
    https://github.com/PARTHIBAN-007/Swiggy-Intern
   cd Swiggy-Intern
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables in a `.env` file:
   ```env
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_key
   ```
5. Run the backend server:
   ```sh
   uvicorn main:app --reload
   ```
   The backend will run at `http://localhost:8000`

### Database Setup
1. Initialize the database and populate it with sample data:
   ```sh
   python db.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the React app:
   ```sh
   npm start
   ```
   The frontend will run at `http://localhost:3000`

## API Endpoints
- `POST /summarize` - Generate a summary, rating, and category for feedback.
- `POST /final-feedback` - Store feedback in the database.
- `GET /feedback-stats` - Retrieve statistics on stored feedback.
- `GET /unresolved-feedback/{domain}` - Fetch unresolved feedback by domain.
- `PUT /resolve-feedback/{feedback_id}` - Mark a feedback entry as resolved.
