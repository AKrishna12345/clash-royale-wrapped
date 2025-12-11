from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class PlayerTagRequest(BaseModel):
    """Request model for player tag"""
    tag: str = Field(..., description="Clash Royale player tag", min_length=3, max_length=20)


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    message: str


class PlayerInfoResponse(BaseModel):
    """Response model for player information"""
    success: bool = True
    data: Dict[str, Any]

