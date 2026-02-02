from pydantic import BaseModel, Field
from typing import List, Dict, Any

class UserBioProfile(BaseModel):
    """User's biological context and profile"""
    chronotype: str = Field(description="lark|owl|intermediate")
    sleep_time: str = Field(description="Sleep time in HH:MM format")
    wake_time: str = Field(description="Wake time in HH:MM format")
    meal_times: Dict[str, str] = Field(description="Meal times: breakfast, lunch, dinner")
    peak_hours: List[str] = Field(description="Peak performance hours (e.g., ['08:00-10:00'])")
    slump_hours: List[str] = Field(default_factory=list, description="Low energy hours")
    fixed_commitments: List[str] = Field(default_factory=list, description="Fixed time commitments")
    energy_tomorrow: str = Field(description="high|medium|low")
    physical_constraints: List[str] = Field(default_factory=list, description="Physical limitations")

class GoalClarifierOutput(BaseModel):
    """Output from Goal Clarifier Agent (A1)"""
    clarified_goal: str = Field(description="SMART format goal")
    user_bio_profile: UserBioProfile
    conversation_complete: bool = Field(default=True, description="True when all info collected")