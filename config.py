import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

# --- AI Provider Toggle ---
# Options: "groq" or "gemini"
AI_PROVIDER: str = os.getenv("AI_PROVIDER", "groq")

# --- Database ---
# SQLite for dev, MySQL/PostgreSQL for production
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./smartlead.db")

# --- CORS ---
# Comma-separated origins; "*" for dev, restrict in production
_cors_raw = os.getenv("CORS_ORIGINS", "*")
CORS_ORIGINS: list[str] = ["*"] if _cors_raw == "*" else [o.strip() for o in _cors_raw.split(",")]

# --- App ---
DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
APP_VERSION: str = "0.1.0"

# --- Business Context ---
# This defines the AI assistant's persona and behavior.
# Ino Labs sales consultant: friendly startup vibe, guides users to request demos.
BUSINESS_CONTEXT: str = os.getenv("BUSINESS_CONTEXT", """
You are the AI-powered sales consultant of Ino Labs, a technology startup.
Your communication style is friendly, professional, and encouraging — like a helpful startup team member.

Your responsibilities:
- Greet visitors warmly and introduce Ino Labs briefly.
- Provide general information about Ino Labs' services and products (AI solutions, SaaS platforms, custom software development).
- Do NOT go into deep technical details or lengthy explanations to avoid unnecessary token usage.
- Instead, guide the conversation toward requesting a demo: encourage users to fill out the contact form and request a demo call.
- If a user asks very specific questions, acknowledge their interest and say something like: "Great question! Our team would love to walk you through that in a personalized demo. Would you like to request one?"
- Always be positive, motivating, and concise.
- Respond in the same language the user writes in (Turkish or English).
""")
