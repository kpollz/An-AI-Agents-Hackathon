import json
from typing import Dict, Any, List
from datetime import datetime
from schemas.final_plan import (
    FinalPlan,
    EditableScheduleItem,
    EditableFields,
    RestPeriodEditable,
    UserContextSummary,
    Metadata
)
from schemas.agent3_output import ScheduleItem, BioInsights
from schemas.agent1_output import UserBioProfile

class JSONFormatterAgent:
    """
    Agent A4: JSON Formatter
    Pure Python module - converts Bio-Optimizer output to editable JSON format
    """
    
    def __init__(self):
        """Initialize JSON Formatter Agent"""
        pass
    
    def format_final_plan(
        self,
        optimized_schedule: List[ScheduleItem],
        bio_insights: BioInsights,
        goal: str,
        bio_profile: UserBioProfile
    ) -> FinalPlan:
        """
        Format optimized schedule into editable final plan
        
        Args:
            optimized_schedule: List of schedule items from Agent A3
            bio_insights: Bio insights from Agent A3
            goal: User's goal
            bio_profile: User's biological profile
        
        Returns:
            FinalPlan object ready for user review
        """
        # Create metadata
        metadata = Metadata(
            goal=goal,
            user_id="anonymous",  # Can be customized
            version="1.0"
        )
        
        # Create user context summary
        context_summary = self._create_context_summary(
            bio_profile=bio_profile,
            bio_insights=bio_insights
        )
        
        # Convert schedule items to editable format
        editable_schedule, rest_periods = self._convert_to_editable(
            optimized_schedule=optimized_schedule
        )
        
        return FinalPlan(
            metadata=metadata,
            user_context_summary=context_summary,
            editable_schedule=editable_schedule,
            rest_periods=rest_periods,
            calendar_ready=False
        )
    
    def _create_context_summary(
        self,
        bio_profile: UserBioProfile,
        bio_insights: BioInsights
    ) -> UserContextSummary:
        """
        Create user context summary
        
        Args:
            bio_profile: User's biological profile
            bio_insights: Bio insights
        
        Returns:
            UserContextSummary object
        """
        return UserContextSummary(
            chronotype=bio_profile.chronotype,
            total_scheduled_hours=bio_insights.total_focus_time,
            notes=f"Optimized for {bio_profile.chronotype} chronotype. {bio_insights.warning}"
        )
    
    def _convert_to_editable(
        self,
        optimized_schedule: List[ScheduleItem]
    ) -> tuple[List[EditableScheduleItem], List[RestPeriodEditable]]:
        """
        Convert schedule items to editable format
        
        Args:
            optimized_schedule: List of schedule items
        
        Returns:
            Tuple of (editable_schedule, rest_periods)
        """
        editable_schedule = []
        rest_periods = []
        
        for item in optimized_schedule:
            if item.type == "focus":
                # Convert to editable schedule item
                editable_item = EditableScheduleItem(
                    id=item.task_id,
                    time=item.scheduled_time,
                    task=item.name,
                    evidence=self._format_evidence(item),
                    tips=item.attached_tips,
                    editable_fields=self._create_editable_fields(item)
                )
                editable_schedule.append(editable_item)
            elif item.type == "rest":
                # Convert to rest period
                rest_item = RestPeriodEditable(
                    time=item.scheduled_time,
                    type="mandatory_break",
                    rationale=item.rationale_timing.why_this_time,
                    can_remove=False,
                    can_extend=True
                )
                rest_periods.append(rest_item)
        
        return editable_schedule, rest_periods
    
    def _format_evidence(self, item: ScheduleItem) -> str:
        """
        Format evidence for display
        
        Args:
            item: Schedule item
        
        Returns:
            Formatted evidence string
        """
        evidence_parts = [
            f"Timing: {item.rationale_timing.why_this_time}",
            f"Principle: {item.atomic_design.principle}",
            f"Trigger: {item.atomic_design.trigger}"
        ]
        
        if item.rationale_timing.evidence_url:
            evidence_parts.append(f"Source: {item.rationale_timing.evidence_url}")
        
        return " | ".join(evidence_parts)
    
    def _create_editable_fields(self, item: ScheduleItem) -> EditableFields:
        """
        Determine which fields are editable for an item
        
        Args:
            item: Schedule item
        
        Returns:
            EditableFields object
        """
        # Time is always editable
        can_move = True
        
        # Can delete unless it's a critical first task
        can_delete = item.atomic_design.principle != "2-minute rule"
        
        # Cannot split small tasks
        can_split = item.duration_minutes > 5
        
        return EditableFields(
            time=item.scheduled_time,
            duration=item.duration_minutes,
            can_move=can_move,
            can_delete=can_delete,
            can_split=can_split
        )
    
    def save_to_file(
        self,
        plan: FinalPlan,
        filepath: str = "output/tomorrow_plan.json"
    ) -> str:
        """
        Save final plan to JSON file
        
        Args:
            plan: FinalPlan object
            filepath: Output file path
        
        Returns:
            File path where plan was saved
        """
        # Convert to dict
        plan_dict = plan.dict()
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(plan_dict, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Plan saved to: {filepath}")
        return filepath
    
    def load_from_file(self, filepath: str) -> FinalPlan:
        """
        Load plan from JSON file
        
        Args:
            filepath: Input file path
        
        Returns:
            FinalPlan object
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            plan_dict = json.load(f)
        
        return FinalPlan(**plan_dict)
    
    def approve_plan(
        self,
        plan: FinalPlan,
        user_edits: Dict[str, Any] = None
    ) -> FinalPlan:
        """
        Mark plan as approved (after user review)
        
        Args:
            plan: FinalPlan object
            user_edits: Optional user edits to apply
        
        Returns:
            Updated FinalPlan with calendar_ready=True
        """
        # Apply user edits if provided
        if user_edits:
            plan = self._apply_edits(plan, user_edits)
        
        # Mark as calendar ready
        plan.calendar_ready = True
        
        return plan
    
    def _apply_edits(
        self,
        plan: FinalPlan,
        edits: Dict[str, Any]
    ) -> FinalPlan:
        """
        Apply user edits to the plan
        
        Args:
            plan: Original plan
            edits: User edits dict
        
        Returns:
            Updated plan
        """
        # Edit schedule items
        if "schedule_edits" in edits:
            for edit in edits["schedule_edits"]:
                item_id = edit.get("id")
                for item in plan.editable_schedule:
                    if item.id == item_id:
                        # Apply allowed edits
                        if "time" in edit and item.editable_fields.can_move:
                            item.time = edit["time"]
                        if "task" in edit and item.editable_fields.can_delete:
                            item.task = edit["task"]
                        if "duration" in edit and item.editable_fields.can_move:
                            item.editable_fields.duration = edit["duration"]
        
        # Edit rest periods
        if "rest_edits" in edits:
            for edit in edits["rest_edits"]:
                for i, rp in enumerate(plan.rest_periods):
                    if edit.get("extend", False) and rp.can_extend:
                        # Extend rest period (simplified logic)
                        rp.duration = rp.duration + 5  # Add 5 minutes
        
        return plan
    
    def generate_summary_markdown(self, plan: FinalPlan) -> str:
        """
        Generate markdown summary of the plan
        
        Args:
            plan: FinalPlan object
        
        Returns:
            Markdown string
        """
        lines = [
            f"# 🎯 Kế hoạch ngày mai: {plan.metadata.goal}",
            "",
            f"**Context của bạn**: {plan.user_context_summary.notes}",
            "",
            f"**Chronotype**: {plan.user_context_summary.chronotype}",
            f"**Tổng thời gian**: {plan.user_context_summary.total_scheduled_hours}",
            "",
            "## 📋 Chuỗi hành động (Atomic Tasks):",
            ""
        ]
        
        for item in plan.editable_schedule:
            lines.append(f"**{item.time}** | {item.task}")
            lines.append(f"- *Trigger*: Được tối ưu theo thời gian sinh học")
            lines.append(f"- *Lý do*: {item.evidence}")
            
            if item.tips:
                tips_str = ", ".join(item.tips)
                lines.append(f"- *Tips*: {tips_str}")
            
            lines.append("")
        
        if plan.rest_periods:
            lines.append("## ☕ Khoảng nghỉ ngơi:")
            lines.append("")
            for rp in plan.rest_periods:
                lines.append(f"**{rp.time}** | {rp.type}")
                lines.append(f"- *Lý do*: {rp.rationale}")
                lines.append("")
        
        lines.append("## ✅ Trạng thái:")
        lines.append(f"- Calendar Sync: {'✅ Đã sẵn sàng' if plan.calendar_ready else '⏳ Chờ duyệt'}")
        lines.append("")
        lines.append("---")
        lines.append("*ATP System - Powered by Behavioral Science*")
        
        return "\n".join(lines)