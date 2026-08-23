"""
AI Service — ino Backend

Google Gemini AI Service.
Falls back to demo mode if no API key is configured.

This module knows NOTHING about HTTP, databases, or FastAPI.
It only communicates with external AI APIs.
"""
import re
from google import genai
from google.genai.types import (
    Content,
    GenerateContentConfig,
    Part,
    ThinkingConfig,
)

from config import BUSINESS_CONTEXT, GEMINI_API_KEY, GEMINI_MODEL


def clean_plain_text(text: str) -> str:
    """Remove accidental Markdown formatting from Gemini responses."""
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r"\1 (\2)",
        text,
    )
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", text)
    text = re.sub(r"(?m)^\s*[-*+]\s+", "• ", text)
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("`", "")
    return text.strip()


class AIServiceError(Exception):
    """Raised when the AI provider returns an error or is unreachable."""
    pass


class AIService:
    """Async AI service using Google Gemini.

    Falls back to demo mode if the API key is missing.
    """

    # Demo mode response when no API key is configured
    DEMO_RESPONSE = (
        "ino asistanı şu anda demo modunda çalışıyor. "
        "Ürün hakkında bilgi almak veya deneyimi yakından görmek için demo talebi bırakabilirsiniz."
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
        """Send a request to the configured Google Gemini model."""
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
                model=GEMINI_MODEL,
                contents=[
                    *gemini_history,
                    Content(role="user", parts=[Part(text=message)]),
                ],
                config=GenerateContentConfig(
                    system_instruction=BUSINESS_CONTEXT,
                    temperature=0.7,
                    max_output_tokens=2048,
                    thinking_config=ThinkingConfig(
                        thinking_level="low",
                    ),
                ),
            )
            if not response.text:
                raise AIServiceError("Gemini returned an empty response.")
            return clean_plain_text(response.text)

        except AIServiceError:
            raise
        except Exception as exc:
            raise AIServiceError(f"Gemini API error: {exc}") from exc


# Singleton instance — imported by routes
ai_service = AIService()
