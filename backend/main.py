from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from app.models import ErrorAnalysisRequest, ErrorAnalysisResponse, SavedError
from app.services.ai_service import AIService
from app.services.storage_service import StorageService
from app.database import create_db_and_tables, get_session
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="AI Error Log Analyzer", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
ai_service = AIService(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/analyze", response_model=ErrorAnalysisResponse)
async def analyze_error(
    request: ErrorAnalysisRequest,
    session: Session = Depends(get_session)
):
    try:
        # AI Analysis
        response = await ai_service.analyze_error(
            raw_error=request.raw_error,
            language=request.language
        )
        
        # Optional Storage
        if request.save_analysis:
            storage = StorageService(session)
            storage.save_error(response)
            
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=list[SavedError])
async def get_history(session: Session = Depends(get_session)):
    storage = StorageService(session)
    return storage.get_history()

@app.delete("/history")
async def clear_history(session: Session = Depends(get_session)):
    storage = StorageService(session)
    storage.clear_history()
    return {"status": "cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
