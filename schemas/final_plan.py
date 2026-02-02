from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class EditableFields(BaseModel):
    """Fields that user can edit"""
    time: str = Field(description="Scheduled time range")
    duration: int = Field(description="Duration in minutes")
    can_move: bool = Field(default=True, description="Can move this item")
    can_delete: bool = Field(default=True, description="Can delete this item")
    can_split: bool = Field(default=False, description="Can split this item")

class EditableScheduleItem(BaseModel):
    """Editable schedule item for user review"""
    id: str = Field(description="Unique identifier")
    time: str = Field(description="Scheduled time range (HH:MM-HH:MM)")
    task: str = Field(description="Task name")
    evidence: str = Field(description="Evidence for this task")
    tips: List[str] = Field(default_factory=list, description="Tips attached")
    editable_fields: EditableFields = Field(description="Editable fields configuration")

class RestPeriodEditable(BaseModel):
    """Editable rest period"""
    time: str = Field(description="Scheduled time range")
    type: str = Field(default="mandatory_break")
    rationale: str = Field(description="Why this rest is needed")
    can_remove: bool = Field(default=False)
    can_extend: bool = Field(default=True)

class UserContextSummary(BaseModel):
    """Summary of user context"""
    chronotype: str = Field(description="lark|owl|intermediate")
    total_scheduled_hours: str = Field(description="Total hours scheduled")
    notes: str = Field(description="Additional notes")

class Metadata(BaseModel):
    """Plan metadata"""
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    goal: str = Field(description="The goal")
    user_id: str = Field(default="anonymous")
    version: str = Field(default="1.0")

class FinalPlan(BaseModel):
    """Final plan output from JSON Formatter (A4)"""
    metadata: Metadata = Field(description="Plan metadata")
    user_context_summary: UserContextSummary = Field(description="User context summary")
    editable_schedule: List[EditableScheduleItem] = Field(description="Editable schedule items")
    rest_periods: List[RestPeriodEditable] = Field(description="Rest periods")
    calendar_ready: bool = Field(default=False, description="True after user approval")