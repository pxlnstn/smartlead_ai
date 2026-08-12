from datetime import datetime
from pydantic import BaseModel, Field


# --- Chat ---
class ChatRequest(BaseModel):
    """Incoming chat message from the Wix frontend (#inputMessage)."""
    message: str = Field(..., min_length=1, max_length=2000, description="User's chat message")
    history: list[dict] = Field(default_factory=list, description="Previous conversation turns")


class ChatResponse(BaseModel):
    """Chat response sent back to #txtResponse."""
    success: bool
    response: str


# --- Contact / Demo Request ---
class ContactRequest(BaseModel):
    """Demo request form from Wix (#inputName, #inputNumber, #inputNote, #btnGetDemo)."""
    name: str = Field(..., min_length=1, max_length=150, description="Contact name")
    number: str = Field(..., min_length=1, max_length=30, description="Phone number")
    note: str = Field(default="", max_length=1000, description="Optional note")


class ContactResponse(BaseModel):
    """Confirmation after saving a lead."""
    success: bool
    message: str


# --- Lead Output ---
class LeadOut(BaseModel):
    """Single lead record for the dashboard / CSV export."""
    id: int
    name: str
    phone_number: str
    note: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class LeadsListResponse(BaseModel):
    """Response for GET /api/leads."""
    success: bool
    leads: list[LeadOut]


# --- Health ---
class HealthResponse(BaseModel):
    """Liveness check response."""
    success: bool
    status: str
    version: str
