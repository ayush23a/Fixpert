from typing import List, Optional
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField
from uuid import UUID, uuid4
from datetime import datetime

class ErrorAnalysisRequest(BaseModel):
    raw_error: str = Field(..., description="The raw error log or stack trace text")
    language: Optional[str] = Field(None, description="Programming language (e.g., Python, TypeScript)")
    context: Optional[str] = Field(None, description="Additional context from the user")
    save_analysis: bool = Field(False, description="Whether to save this analysis to history (User Opt-in)")
    api_key: Optional[str] = Field(None, description="API key for authentication or tracking")

class RootCauseHypothesis(BaseModel):
    cause: str
    confidence: float = Field(..., ge=0.0, le=1.0)

class ErrorAnalysisResponse(BaseModel):
    summary: str = Field(..., description="Concise, plain-English summary of the error")
    category: str = Field(..., description="Broad category (e.g., Database, Network, Syntax)")
    root_causes: List[RootCauseHypothesis] = Field(default_factory=list, description="Ranked list of likely root causes")
    suggested_steps: List[str] = Field(default_factory=list, description="Actionable debugging steps")
    uncertainty_statement: Optional[str] = Field(None, description="Statement if AI is unsure")

class SavedError(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    summary: str
    category: str
    root_cause: str
    created_at: datetime = SQLField(default_factory=datetime.utcnow)
