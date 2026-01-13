from google import genai
from app.models import ErrorAnalysisResponse, RootCauseHypothesis
import json
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, api_key: str = None):
        if not api_key:
            logger.warning("GEMINI_API_KEY is not set. AI analysis will fail.")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)
            self.model_name = 'gemini-2.5-flash'

    async def analyze_error(self, raw_error: str, language: str = None, api_key_override: str = None) -> ErrorAnalysisResponse:
        # Use override key if provided, otherwise fall back to system client
        client_to_use = self.client
        model_name = self.model_name

        if api_key_override:
            try:
                 # Create a temporary client for this request
                 client_to_use = genai.Client(api_key=api_key_override)
            except Exception as e:
                logger.error(f"Failed to initialize client with user key: {e}")
                return ErrorAnalysisResponse(
                    summary="Configuration Error: Invalid User API Key",
                    category="System Error",
                    root_causes=[],
                    suggested_steps=["Check the API Key in VS Code Settings."],
                    uncertainty_statement="The provided API key could not be used."
                )

        if not client_to_use:
             return ErrorAnalysisResponse(
                summary="Configuration Error: No API Key",
                category="System Error",
                root_causes=[],
                suggested_steps=["Set GEMINI_API_KEY in .env or VS Code Settings"],
                uncertainty_statement="API Key missing."
            )
        
        prompt = self._construct_prompt(raw_error, language)
        
        try:
            # Generate content using new SDK
            response = client_to_use.models.generate_content(
                model=model_name,
                contents=prompt
            )
            response_text = response.text
            
            # Clean up potential markdown formatting (```json ... ```)
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            # Parse JSON
            data = json.loads(response_text)
            
            # Validation via Pydantic
            return ErrorAnalysisResponse(**data)
            
        except Exception as e:
            logger.error(f"AI Analysis Failed: {str(e)}")
            # Return a fallback response so the UI doesn't crash
            return ErrorAnalysisResponse(
                summary="AI Analysis failed to generate a valid response.",
                category="System Error",
                root_causes=[RootCauseHypothesis(cause=f"Internal Logic Error: {str(e)}", confidence=1.0)],
                suggested_steps=["Check API Key", "Check Logs"],
                uncertainty_statement="The AI model could not process this request."
            )

    def _construct_prompt(self, raw_error: str, language: str = None) -> str:
        ctx_lang = f"Language: {language}\n" if language else ""
        return f"""
You are an expert Senior Developer and System Architect.
Your task is to analyze the following error log and provide a structured diagnosis.

{ctx_lang}
Input Error Log:
{raw_error}
---------------------------------------------------

Format your response as a strict JSON object matching this schema:
{{
  "summary": "One line summary of what went wrong (plain english)",
  "category": "The broad category e.g. 'Network', 'Database', 'Syntax', 'Runtime', 'Configuration'",
  "root_causes": [
    {{ "cause": "Most likely root cause", "confidence": 0.9 }},
    {{ "cause": "Alternative possibility", "confidence": 0.4 }}
  ],
  "suggested_steps": [
    "Step 1", "Step 2", "Step 3"
  ],
  "uncertainty_statement": "If you are unsure, explain why here. Otherwise null"
}}

Rules:
1. Be concise and actionable.
2. Do not invent files that don't exist.
3. If the error is cut off, state that in uncertainty.
4. Output specific debugging steps, not generic "check logs".
5. RETURN ONLY VALID JSON. NO MARKDOWN.
"""
