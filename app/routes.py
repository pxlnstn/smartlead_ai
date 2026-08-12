"""
API Routes — Ino Labs Backend

Handles incoming HTTP requests, validates them via Pydantic schemas,
and delegates to the appropriate service/database layer.

No SQL or AI logic lives here — only request/response orchestration.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Lead
from app.schemas import (
    ChatRequest,
    ChatResponse,
    ContactRequest,
    ContactResponse,
    HealthResponse,
    LeadOut,
    LeadsListResponse,
)
from app.services import AIServiceError, ai_service
from config import APP_VERSION

logger = logging.getLogger(__name__)

# --- Routers ---
api_router = APIRouter(prefix="/api", tags=["api"])
health_router = APIRouter(tags=["health"])


# ──────────────────────────────────────────────
# Health Check
# ──────────────────────────────────────────────
@health_router.get(
    "/health",
    response_model=HealthResponse,
    summary="Liveness check",
)
async def health_check() -> HealthResponse:
    """Return server status for uptime monitoring (e.g., Render, UptimeRobot)."""
    return HealthResponse(
        success=True,
        status="healthy",
        version=APP_VERSION,
    )


# ──────────────────────────────────────────────
# POST /api/chat  —  AI Conversation
# ──────────────────────────────────────────────
@api_router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send a message to the AI assistant",
)
async def chat(request: ChatRequest) -> ChatResponse:
    """Accept a user message (+optional history) and return an AI response.

    Called from Wix Velo via #btnSend → fetch('/api/chat', ...).
    Response text is displayed in #txtResponse.
    """
    try:
        response_text = await ai_service.generate_response(
            message=request.message,
            history=request.history,
        )
        return ChatResponse(success=True, response=response_text)

    except AIServiceError as exc:
        logger.error("AI service failure: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "success": False,
                "response": "Our AI assistant is temporarily unavailable. Please try again shortly.",
            },
        ) from exc


# ──────────────────────────────────────────────
# POST /api/contact  —  Save a Demo Request / Lead
# ──────────────────────────────────────────────
@api_router.post(
    "/contact",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a demo request / contact form",
)
async def create_contact(
    request: ContactRequest,
    db: AsyncSession = Depends(get_db),
) -> ContactResponse:
    """Save a new lead from the Wix contact form (#btnGetDemo).

    Maps incoming fields:
        name   → Lead.name
        number → Lead.phone_number
        note   → Lead.note
    """
    try:
        lead = Lead(
            name=request.name,
            phone_number=request.number,
            note=request.note or None,
        )
        db.add(lead)
        await db.flush()  # get the id before commit (commit happens in get_db)

        logger.info("New lead saved: id=%s, name=%s", lead.id, lead.name)
        return ContactResponse(
            success=True,
            message="Thank you! Your demo request has been received. We'll be in touch soon.",
        )

    except Exception as exc:
        logger.error("Failed to save lead: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": "An error occurred while saving your request. Please try again.",
            },
        ) from exc


# ──────────────────────────────────────────────
# GET /api/leads  —  List All Leads
# ──────────────────────────────────────────────
@api_router.get(
    "/leads",
    response_model=LeadsListResponse,
    summary="Retrieve all collected leads",
)
async def list_leads(
    db: AsyncSession = Depends(get_db),
) -> LeadsListResponse:
    """Return every lead record for the management dashboard.

    Called from Wix Velo Repeater on the admin page.
    Each record includes _id-compatible `id` field for Repeater binding.
    """
    try:
        result = await db.execute(
            select(Lead).order_by(Lead.created_at.desc())
        )
        leads = result.scalars().all()

        return LeadsListResponse(
            success=True,
            leads=[LeadOut.model_validate(lead) for lead in leads],
        )

    except Exception as exc:
        logger.error("Failed to fetch leads: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "leads": [],
                "message": "Failed to retrieve leads.",
            },
        ) from exc
