from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from projects root .env
load_dotenv()

# Add the CrewAI project src to sys.path
# Current path is project/backend, crew logic is in project/topic_summary/src
base_path = Path(__file__).resolve().parent.parent
src_path = base_path / "topic_summary" / "src"
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from topic_summary.crew import TopicSummaryCrew

app = FastAPI()

# Enable CORS for React frontend (usually runs on port 5173 or 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KickoffRequest(BaseModel):
    topic: str

@app.get("/")
def read_root():
    return {"message": "AI Topic Summary Crew API is running"}

@app.post("/kickoff")
async def kickoff_crew(request: KickoffRequest):
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("SERPER_API_KEY"):
        raise HTTPException(status_code=500, detail="API Keys not configured in backend .env")
    
    try:
        inputs = {"topic": request.topic}
        result = TopicSummaryCrew().crew().kickoff(inputs=inputs)
        return {
            "status": "success",
            "result": result.raw,
            "topic": request.topic
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
