from sqlmodel import Session, select
from app.models import SavedError, ErrorAnalysisResponse
from typing import List

class StorageService:
    def __init__(self, session: Session):
        self.session = session

    def save_error(self, analysis: ErrorAnalysisResponse) -> SavedError:
        # Sanitization logic would go here (stripping PII/Secrets)
        # For now, we assume the AI Summary is safe as it's generated text
        
        saved_error = SavedError(
            summary=analysis.summary,
            category=analysis.category,
            root_cause=analysis.root_causes[0].cause if analysis.root_causes else "Unknown",
        )
        self.session.add(saved_error)
        self.session.commit()
        self.session.refresh(saved_error)
        return saved_error

    def get_history(self) -> List[SavedError]:
        results = self.session.exec(select(SavedError).order_by(SavedError.created_at.desc())).all()
        return results
    
    def clear_history(self):
        # Delete all records
        self.session.exec("DELETE FROM savederror") # SQLModel requires explicit delete logic usually, using raw for brevity or loop
        # Better:
        statement = select(SavedError)
        results = self.session.exec(statement)
        for res in results:
            self.session.delete(res)
        self.session.commit()
