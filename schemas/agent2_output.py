from pydantic import BaseModel, Field
from typing import List, Optional

class TaskEvidence(BaseModel):
    """Evidence supporting a task"""
    source_url: str = Field(description="URL of the source")
    authority: str = Field(description="Author or organization name")
    summary: str = Field(description="Why this task is necessary")

class Task(BaseModel):
    """A task from domain research"""
    task_id: str = Field(description="Unique task identifier")
    name: str = Field(description="Task name")
    description: str = Field(description="Task description")
    estimated_duration: str = Field(description="ISO 8601 duration (e.g., PT30M)")
    difficulty: str = Field(description="high|medium|low")
    evidence: TaskEvidence

class TipEvidence(BaseModel):
    """Evidence supporting a pro tip"""
    source_url: str = Field(description="URL of the source")
    study_summary: str = Field(description="Summary of the study")
    applicability: str = Field(description="When this tip applies")

class ProTip(BaseModel):
    """Professional tip for task execution"""
    tip_id: str = Field(description="Unique tip identifier")
    content: str = Field(description="Tip content")
    applies_to_task: str = Field(description="Task ID this tip applies to")
    evidence: TipEvidence

class DomainResearcherOutput(BaseModel):
    """Output from Domain Researcher Agent (A2)"""
    domain: str = Field(description="Domain/activity name")
    tasks: List[Task] = Field(description="List of tasks with evidence")
    pro_tips: List[ProTip] = Field(description="List of professional tips")
    warnings: List[str] = Field(default_factory=list, description="Common pitfalls to avoid")