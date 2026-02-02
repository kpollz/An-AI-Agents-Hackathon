from pydantic import BaseModel, Field
from typing import List, Dict, Any

class RationaleTiming(BaseModel):
    """Rationale for timing assignment"""
    why_this_time: str = Field(description="Why this time was chosen")
    evidence_url: str = Field(description="URL of supporting evidence")
    chronotype_match: str = Field(description="lark|owl|intermediate")

class AtomicDesign(BaseModel):
    """Atomic habits design principles"""
    principle: str = Field(description="Atomic habit principle applied")
    trigger: str = Field(description="Trigger for the habit")
    friction_reduction: str = Field(description="How friction is reduced")

class ScheduleItem(BaseModel):
    """A scheduled item (task or rest)"""
    task_id: str = Field(description="Unique identifier")
    original_task_ref: str = Field(default="", description="Reference to original task")
    name: str = Field(description="Task name")
    description: str = Field(description="Task description")
    scheduled_time: str = Field(description="Scheduled time range (HH:MM-HH:MM)")
    rationale_timing: RationaleTiming = Field(description="Timing rationale")
    atomic_design: AtomicDesign = Field(description="Atomic habit design")
    attached_tips: List[str] = Field(default_factory=list, description="Tip IDs attached")
    duration_minutes: int = Field(description="Duration in minutes")
    type: str = Field(description="focus|rest|meal|commute")

class RestPeriod(BaseModel):
    """A rest period"""
    task_id: str = Field(description="Unique identifier")
    name: str = Field(default="Rest period")
    description: str = Field(default="Rest and recovery")
    scheduled_time: str = Field(description="Scheduled time range")
    duration_minutes: int = Field(description="Duration in minutes")
    type: str = Field(default="rest")
    rationale_timing: RationaleTiming = Field(description="Why rest is needed here")

class BioInsights(BaseModel):
    """Insights about the schedule"""
    total_focus_time: str = Field(description="Total focus time")
    total_rest_time: str = Field(description="Total rest time")
    energy_curve_match: str = Field(description="Percentage match to user's energy curve")
    warning: str = Field(default="", description="Any warnings about the schedule")

class BioOptimizerOutput(BaseModel):
    """Output from Bio-Optimizer Agent (A3)"""
    optimized_schedule: List[ScheduleItem] = Field(description="List of scheduled tasks and rest periods")
    bio_insights: BioInsights = Field(description="Insights about the schedule")