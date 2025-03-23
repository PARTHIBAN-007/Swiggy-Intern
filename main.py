import sqlite3
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("feedback.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    summary TEXT,
    rating INTEGER,
    domain TEXT,
    resolved INTEGER DEFAULT 0
)
""")
conn.commit()

class FeedbackRequest(BaseModel):
    text: str

class FinalFeedbackRequest(BaseModel):
    text: str
    summary: str
    rating: int
    domain: str

class SummaryParser(BaseModel):
    summary: str
    rating: int
    domain: str

parser = PydanticOutputParser(pydantic_object=SummaryParser)

prompt_template = PromptTemplate(
    input_variables=["content"],
    template="""
    Summarize the feedback and classify it into one of the following domains:
    - "Delivery Experience"
    - "Food Quality"
    - "Customer Service"
    - "App Usability"
    - "Other"

    Provide a feedback rating from 1 to 10 based on positivity.
    Return JSON with:
    - summary
    - rating
    - domain
    Content: {content}
    Output in JSON format.
    """
)

@app.post("/summarize")
async def summarize_feedback(request: Request):
    body = await request.json()
    user_content = body.get("text", "")

    if not user_content:
        raise HTTPException(status_code=400, detail="Feedback content is required")

    repo_id = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
    llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain.run(content=user_content)

    parsed_output = parser.parse(response)
    print(parsed_output)
    return {
        "summary": parsed_output.summary,
        "rating": parsed_output.rating,
        "domain": parsed_output.domain,
    }

@app.post("/final-feedback")
async def upload_data(feedback: FinalFeedbackRequest):
    cursor.execute(
        "INSERT INTO feedback (text, summary, rating, domain, resolved) VALUES (?, ?, ?, ?, 0)",
        (feedback.text, feedback.summary, feedback.rating, feedback.domain)
    )
    conn.commit()
    return {"message": "Feedback stored successfully"}

@app.get("/feedback-stats")
async def feedback_stats():
    cursor.execute("SELECT domain, COUNT(*) FROM feedback GROUP BY domain")
    domain_stats = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM feedback WHERE resolved = 1")
    resolved_count = cursor.fetchone()[0]

    return {"domains": dict(domain_stats), "resolved_feedback": resolved_count}

@app.get("/unresolved-feedback/{domain}")
async def unresolved_feedback(domain: str):
    cursor.execute(
        "SELECT id, text, summary, rating FROM feedback WHERE domain = ? AND resolved = 0",
        (domain,)
    )
    reviews = cursor.fetchall()

    return [{"id": r[0], "text": r[1], "summary": r[2], "rating": r[3]} for r in reviews]

@app.put("/resolve-feedback/{feedback_id}")
async def resolve_feedback(feedback_id: int):
    cursor.execute("UPDATE feedback SET resolved = 1 WHERE id = ?", (feedback_id,))
    conn.commit()
    return {"message": "Feedback marked as resolved"}
