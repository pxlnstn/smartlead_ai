from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ChatTurn(BaseModel):
    """One validated conversation turn accepted from the public client."""

    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=2000)


# --- Chat ---
class ChatRequest(BaseModel):
    """Incoming chat message from the Wix frontend (#inputMessage)."""
    message: str = Field(..., min_length=1, max_length=2000, description="User's chat message")
    history: list[ChatTurn] = Field(
        default_factory=list,
        max_length=20,
        description="Previous conversation turns",
    )

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message cannot be blank")
        return value


class ChatResponse(BaseModel):
    """Chat response sent back to #txtResponse."""
    success: bool
    response: str


# --- Contact / Demo Request ---
class ContactRequest(BaseModel):
    """Demo request form from Wix (#inputName, #inputNumber, #inputNote, #btnGetDemo)."""
    name: str = Field(..., min_length=1, max_length=150, description="Contact name")
    number: str = Field(..., min_length=7, max_length=30, description="Phone number")
    note: str = Field(default="", max_length=1000, description="Optional note")

    @field_validator("name", "number", "note")
    @classmethod
    def strip_text_fields(cls, value: str) -> str:
        return value.strip()

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value:
            raise ValueError("Name cannot be blank")
        return value

    @field_validator("number")
    @classmethod
    def phone_must_have_enough_digits(cls, value: str) -> str:
        if sum(character.isdigit() for character in value) < 7:
            raise ValueError("Phone number must contain at least 7 digits")
        return value


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
