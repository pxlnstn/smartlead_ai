"""
AI Service — Ino Labs Backend

Google Gemini AI Service.
Falls back to demo mode if no API key is configured.

This module knows NOTHING about HTTP, databases, or FastAPI.
It only communicates with external AI APIs.
"""

from google import genai
from google.genai.types import Content, Part

from config import GEMINI_API_KEY, BUSINESS_CONTEXT


class AIServiceError(Exception):
    """Raised when the AI provider returns an error or is unreachable."""
    pass


class AIService:
    """Async AI service using Google Gemini.

    Falls back to demo mode if the API key is missing.
    """

    # Demo mode response when no API key is configured
    DEMO_RESPONSE = (
        "\U0001f680 Thanks for your interest in Ino Labs! "
        "I'm currently running in demo mode. "
        "Please contact our team or request a demo to experience the full AI assistant."
    )

    def __init__(self) -> None:
        # Initialize Google Gemini client (new google-genai SDK)
        self._gemini_client: genai.Client | None = None
        if GEMINI_API_KEY:
            self._gemini_client = genai.Client(api_key=GEMINI_API_KEY)

    async def generate_response(self, message: str, history: list[dict] | None = None) -> str:
        """Generate an AI response using Google Gemini.

        Args:
            message: The user's latest message.
            history: Previous conversation turns [{"role": "user"|"assistant", "content": "..."}].

        Returns:
            The AI-generated response string.

        Raises:
            AIServiceError: If the AI provider call fails.
        """
        history = history or []

        return await self._call_gemini(message, history)

    async def _call_gemini(self, message: str, history: list[dict]) -> str:
        """Send a request to Google Gemini (gemini-2.0-flash)."""
        if not self._gemini_client:
            return self.DEMO_RESPONSE

        try:
            # Convert history to Gemini Content format
            gemini_history: list[Content] = []
            for turn in history:
                role = "user" if turn["role"] == "user" else "model"
                gemini_history.append(
                    Content(role=role, parts=[Part(text=turn["content"])])
                )

            response = await self._gemini_client.aio.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    *gemini_history,
                    Content(role="user", parts=[Part(text=message)]),
                ],
                config={
                    "system_instruction": BUSINESS_CONTEXT,
                    "temperature": 0.7,
                    "max_output_tokens": 512,
                },
            )
            return response.text

        except Exception as exc:
            raise AIServiceError(f"Gemini API error: {exc}") from exc


# Singleton instance — imported by routes
ai_service = AIService()
