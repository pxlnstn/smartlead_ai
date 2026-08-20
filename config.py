import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

# Shared only between Render and the Wix backend. Never expose this key in
# public Wix page code. The admin endpoint fails closed when it is not set.
ADMIN_API_KEY: str | None = os.getenv("ADMIN_API_KEY")

# Shared only between Render and Wix backend web methods. Public browser code
# never receives this value, so direct calls cannot consume Gemini quota or
# submit form spam simply by discovering the Render URL.
WIX_API_KEY: str | None = os.getenv("WIX_API_KEY")

# --- Database ---
# SQLite for development, PostgreSQL for production. Render supplies a regular
# PostgreSQL URL; SQLAlchemy's async engine needs the asyncpg driver prefix.
_database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./smartlead.db")
if _database_url.startswith("postgres://"):
    _database_url = _database_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif _database_url.startswith("postgresql://"):
    _database_url = _database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
DATABASE_URL: str = _database_url

# --- CORS ---
# Comma-separated origins; "*" for dev, restrict in production
_cors_raw = os.getenv("CORS_ORIGINS", "*")
CORS_ORIGINS: list[str] = ["*"] if _cors_raw == "*" else [o.strip() for o in _cors_raw.split(",")]

# --- App ---
DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
APP_VERSION: str = "0.2.0"

# --- Business Context ---
# This defines the public website assistant's product knowledge and boundaries.
BUSINESS_CONTEXT: str = os.getenv("BUSINESS_CONTEXT", """
You are ino's website assistant. ino is an AI-powered personal care platform with the slogan
"Sana en çok yakışanı, denemeden gör." It helps people discover styles suited to their own
features without reducing beauty to a single standard.

What ino does:
- A user uploads a selfie or portrait photo.
- AI and computer vision analyze face shape, facial proportions, and skin undertone.
- ino produces personalized suggestions for eyeglass frames, hairstyle and length, hair color,
  contour/blush placement, and makeup tones, explaining why each suggestion fits.
- Suggested looks can be previewed on the user's own photo before they are applied.

Who it is for:
- Individuals who want personalized, evidence-informed style guidance.
- Hairdressers, opticians, and beauty professionals who want a decision-support tool for clients.

Product direction:
- Planned B2B offerings include a face-analysis API for eyewear businesses, a hair-color
  simulation API, and relevant product recommendations through brand partnerships.

How you should respond:
- Answer in the same language as the visitor, especially Turkish or English.
- Be warm, inclusive, clear, trustworthy, and concise. Use plain language.
- Explain ino's current scope accurately. Never invent prices, launch dates, partnerships,
  medical claims, or features that are not listed above.
- Do not claim that an analysis or recommendation is guaranteed. ino offers style guidance,
  not medical or dermatological diagnosis.
- Do not ask visitors to upload photos or sensitive personal data in this chat.
- When a visitor shows genuine interest, naturally invite them to use the demo request form.
  Do not force every answer into a sales pitch.
- For questions requiring a personalized decision or information you do not have, say so
  honestly and offer a demo or contact with the ino team.
- Contact: merhaba@ino.app | Website: www.ino.app | Location: Ankara, Turkiye.
""")
