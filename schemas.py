"""Pydantic schemas for 360Learning Connector."""
from __future__ import annotations
from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameters model."""
    pass

class ConnectParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Primary 360Learning.")
    api_key: str = Field(description="LMS API Key / Access Token")
    base_url: str = Field(default="https://app.360learning.com/api/v1", description="360Learning API base URL.")

class ConnectionIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier (empty uses active connection).")

class ConnectionRecord(BaseModel):
    id: str
    label: str
    masked_key: str
    base_url: str
    is_active: bool

class ConnectionList(BaseModel):
    connections: list[ConnectionRecord]
    total: int

class DeleteResult(BaseModel):
    success: bool
    message: str

class CourseRecord(BaseModel):
    id: str
    name: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    raw: Dict[str, Any] = Field(default_factory=dict)

class CourseList(BaseModel):
    courses: list[CourseRecord]
    total: int

class ListCourseParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    limit: int = Field(default=20, ge=1, le=100, description="Max records to return.")

class GetCourseParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    course_id: str = Field(description="360Learning Course ID.")

class AuditHealthReport(BaseModel):
    healthy: bool
    total_courses: int
    details: Dict[str, Any] = Field(default_factory=dict)
    summary: str
