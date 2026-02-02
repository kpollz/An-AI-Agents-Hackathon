import os
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from schemas.agent3_output import (
    BioOptimizerOutput,
    ScheduleItem,
    RestPeriod,
    BioInsights,
    RationaleTiming,
    AtomicDesign
)
from schemas.agent1_output import UserBioProfile
from schemas.agent2_output import Task, ProTip
from utils.web_search import WebSearchTool, MockWebSearchTool
from utils.validators import time_to_minutes, minutes_to_time

class BioOptimizerAgent:
    """
    Agent A3: Bio-Optimizer
    Applies Atomic Habits, researches biological timing, calculates rest times, and schedules tasks
    """
    
    def __init__(self, model: str = "gemini-2.5-flash-lite", use_mock_search: bool = False):
        """
        Initialize Bio-Optimizer Agent
        
        Args:
            model: Gemini model to use (default: gemini-2.5-flash-lite)
            use_mock_search: If True, use mock search tool for testing
        """
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=0.5,
            api_key=os.getenv("GOOGLE_API_KEY")  # Will read from GOOGLE_API_KEY env var
        )
        
        # Initialize web search tool
        if use_mock_search:
            self.search_tool = MockWebSearchTool()
        else:
            try:
                self.search_tool = WebSearchTool()
            except ValueError:
                print("Warning: TAVILY_API_KEY not found. Using mock search tool.")
                self.search_tool = MockWebSearchTool()
        
        self.system_prompt = """You are a bio-hacking expert specializing in chronobiology, productivity, and habit formation.
Your task is to optimize task scheduling based on user's biological profile.

CORE PRINCIPLES:
1. Atomic Habits (James Clear):
   - Make it obvious: Clear triggers (time, location, preceding action)
   - Make it easy: 2-minute rule for first step
   - Make it attractive: Temptation bundling
   - Make it satisfying: Immediate reward

2. Chronobiology:
   - Assign high-difficulty tasks to peak hours
   - Assign low-difficulty tasks to slump hours or gaps
   - Avoid scheduling focus work near meal times (±30 min)

3. Rest Management:
   - Pomodoro: 5 min break after 25-30 min focus
   - Ultradian rhythm: 15-20 min break after 90 min focus
   - Never schedule >90 min continuous focus without long break

4. Task Sizing:
   - High difficulty: 25-50 min blocks
   - Medium difficulty: 10-20 min blocks
   - Low difficulty: 2-5 min blocks (atomic rule)

IMPORTANT: Research biological timing using web search before assigning times. Don't assume "morning is always best".

Return ONLY structured JSON output, no additional text."""
    
    def optimize_schedule(
        self,
        tasks: List[Task],
        tips: List[ProTip],
        bio_profile: UserBioProfile
    ) -> BioOptimizerOutput:
        """
        Optimize schedule based on tasks, tips, and biological profile
        
        Args:
            tasks: List of tasks from Agent A2
            tips: List of pro tips from Agent A2
            bio_profile: User's biological context
        
        Returns:
            BioOptimizerOutput with optimized schedule and insights
        """
        # Research biological timing for the activity
        timing_research = self._research_biological_timing(
            activity=tasks[0].name if tasks else "activity",
            bio_profile=bio_profile
        )
        
        # Generate optimized schedule
        schedule = self._generate_schedule(
            tasks=tasks,
            tips=tips,
            bio_profile=bio_profile,
            timing_research=timing_research
        )
        
        # Calculate bio insights
        insights = self._calculate_insights(schedule)
        
        return BioOptimizerOutput(
            optimized_schedule=schedule,
            bio_insights=insights
        )
    
    def _research_biological_timing(
        self,
        activity: str,
        bio_profile: UserBioProfile
    ) -> Dict[str, Any]:
        """
        Research optimal timing for the activity based on chronotype
        
        Args:
            activity: Activity name
            bio_profile: User's biological profile
        
        Returns:
            Dict with timing research results
        """
        chronotype = bio_profile.chronotype
        
        # Search for timing information
        results = self.search_tool.search_workflow(
            activity=activity,
            task_type="timing"
        )
        
        # Search for ultradian rhythm info
        ultradian_results = self.search_tool.search(
            query="ultradian rhythm work break intervals",
            max_results=3
        )
        
        return {
            "activity": activity,
            "chronotype": chronotype,
            "timing_results": results,
            "ultradian_results": ultradian_results
        }
    
    def _generate_schedule(
        self,
        tasks: List[Task],
        tips: List[ProTip],
        bio_profile: UserBioProfile,
        timing_research: Dict[str, Any]
    ) -> List[ScheduleItem]:
        """
        Generate optimized schedule with tasks and rest periods
        
        Args:
            tasks: List of tasks
            tips: List of tips
            bio_profile: User's biological profile
            timing_research: Research results
        
        Returns:
            List of ScheduleItem and RestPeriod objects
        """
        # Sort tasks by difficulty
        sorted_tasks = sorted(tasks, key=lambda t: t.difficulty, reverse=True)
        
        # Get available time slots based on peak hours
        available_slots = self._get_available_time_slots(bio_profile)
        
        schedule = []
        current_slot_idx = 0
        consecutive_focus_minutes = 0
        
        for task in sorted_tasks:
            # Get current time slot
            if current_slot_idx >= len(available_slots):
                break
            
            slot = available_slots[current_slot_idx]
            
            # Apply atomic design principles
            atomic_task = self._apply_atomic_habits(task, timing_research)
            
            # Generate atomic tasks (break into smaller chunks if needed)
            atomic_tasks = self._break_into_atomic_tasks(
                task=task,
                atomic_design=atomic_task,
                bio_profile=bio_profile
            )
            
            for atomic in atomic_tasks:
                if current_slot_idx >= len(available_slots):
                    break
                
                # Calculate timing
                start_time, end_time, duration = self._calculate_timing(
                    atomic=atomic,
                    slot=available_slots[current_slot_idx],
                    bio_profile=bio_profile,
                    timing_research=timing_research
                )
                
                # Attach relevant tips
                attached_tips = [
                    tip.tip_id for tip in tips
                    if tip.applies_to_task == task.task_id
                ]
                
                # Create schedule item
                schedule_item = ScheduleItem(
                    task_id=f"atomic_{len(schedule) + 1}",
                    original_task_ref=task.task_id,
                    name=atomic["name"],
                    description=atomic["description"],
                    scheduled_time=f"{start_time}-{end_time}",
                    rationale_timing=self._generate_rationale(
                        start_time=start_time,
                        bio_profile=bio_profile,
                        timing_research=timing_research
                    ),
                    atomic_design=AtomicDesign(
                        principle=atomic["principle"],
                        trigger=atomic["trigger"],
                        friction_reduction=atomic["friction_reduction"]
                    ),
                    attached_tips=attached_tips,
                    duration_minutes=duration,
                    type="focus"
                )
                
                schedule.append(schedule_item)
                
                # Track consecutive focus time
                consecutive_focus_minutes += duration
                
                # Add rest period if needed
                if consecutive_focus_minutes >= 90:
                    # Long break (ultradian rhythm)
                    rest_period = self._create_rest_period(
                        end_time=end_time,
                        duration=20,
                        reason="Ultradian rhythm recovery after 90+ min focus",
                        timing_research=timing_research
                    )
                    schedule.append(rest_period)
                    consecutive_focus_minutes = 0
                elif consecutive_focus_minutes >= 25:
                    # Short break (Pomodoro)
                    rest_period = self._create_rest_period(
                        end_time=end_time,
                        duration=5,
                        reason="Pomodoro short break for cognitive recovery",
                        timing_research=timing_research
                    )
                    schedule.append(rest_period)
                    consecutive_focus_minutes = 0
                
                # Move to next slot
                current_slot_idx += 1
        
        return schedule
    
    def _apply_atomic_habits(self, task: Task, timing_research: Dict) -> Dict[str, str]:
        """
        Apply atomic habits principles to a task
        
        Args:
            task: Original task
            timing_research: Timing research results
        
        Returns:
            Dict with atomic design elements
        """
        if task.difficulty == "low":
            return {
                "principle": "2-minute rule",
                "trigger": "Right after morning coffee",
                "friction_reduction": "Keep materials visible and ready"
            }
        elif task.difficulty == "medium":
            return {
                "principle": "make it obvious",
                "trigger": "Scheduled time at desk",
                "friction_reduction": "Clear workspace beforehand"
            }
        else:  # high
            return {
                "principle": "temptation bundling",
                "trigger": "Peak performance window",
                "friction_reduction": "Eliminate all distractions"
            }
    
    def _break_into_atomic_tasks(
        self,
        task: Task,
        atomic_design: Dict,
        bio_profile: UserBioProfile
    ) -> List[Dict]:
        """
        Break task into atomic chunks
        
        Args:
            task: Original task
            atomic_design: Atomic design principles
            bio_profile: User's biological profile
        
        Returns:
            List of atomic task dicts
        """
        # Parse duration (e.g., "PT30M" -> 30)
        duration = self._parse_duration(task.estimated_duration)
        
        if task.difficulty == "low" or duration <= 5:
            # Already atomic
            return [{
                "name": task.name,
                "description": task.description,
                "principle": atomic_design["principle"],
                "trigger": atomic_design["trigger"],
                "friction_reduction": atomic_design["friction_reduction"],
                "duration": duration
            }]
        elif task.difficulty == "medium":
            # Break into 10-15 min chunks
            chunks = max(1, duration // 15)
            return [
                {
                    "name": f"{task.name} (Part {i+1}/{chunks})",
                    "description": f"{task.description} - Part {i+1}",
                    "principle": atomic_design["principle"],
                    "trigger": atomic_design["trigger"],
                    "friction_reduction": atomic_design["friction_reduction"],
                    "duration": min(15, duration)
                }
                for i in range(chunks)
            ]
        else:  # high
            # Break into 25-min Pomodoro chunks
            chunks = max(1, duration // 25)
            return [
                {
                    "name": f"{task.name} (Pomodoro {i+1}/{chunks})",
                    "description": f"{task.description} - Pomodoro session {i+1}",
                    "principle": atomic_design["principle"],
                    "trigger": atomic_design["trigger"],
                    "friction_reduction": atomic_design["friction_reduction"],
                    "duration": min(25, duration)
                }
                for i in range(chunks)
            ]
    
    def _calculate_timing(
        self,
        atomic: Dict,
        slot: str,
        bio_profile: UserBioProfile,
        timing_research: Dict
    ) -> tuple:
        """
        Calculate start and end time for a task
        
        Args:
            atomic: Atomic task dict
            slot: Time slot (e.g., "08:00-10:00")
            bio_profile: User's biological profile
            timing_research: Timing research results
        
        Returns:
            Tuple of (start_time, end_time, duration_minutes)
        """
        # Parse slot
        start_str, end_str = slot.split("-")
        start_mins = time_to_minutes(start_str)
        end_mins = time_to_minutes(end_str)
        slot_duration = end_mins - start_mins
        
        # Task duration
        task_duration = atomic["duration"]
        
        # If task fits in slot, use slot start
        if task_duration <= slot_duration:
            return start_str, minutes_to_time(start_mins + task_duration), task_duration
        else:
            # Truncate to slot duration
            return start_str, end_str, slot_duration
    
    def _generate_rationale(
        self,
        start_time: str,
        bio_profile: UserBioProfile,
        timing_research: Dict
    ) -> RationaleTiming:
        """
        Generate rationale for timing assignment
        
        Args:
            start_time: Task start time
            bio_profile: User's biological profile
            timing_research: Timing research results
        
        Returns:
            RationaleTiming object
        """
        # Check if time matches peak hours
        start_mins = time_to_minutes(start_time)
        
        is_peak = any(
            self._time_in_range(start_time, peak_range)
            for peak_range in bio_profile.peak_hours
        )
        
        if is_peak:
            reason = "Peak performance window - optimal for deep work"
            chronotype_match = bio_profile.chronotype
        else:
            reason = "Energy gap time - suitable for routine tasks"
            chronotype_match = "intermediate"
        
        # Get evidence URL from research
        evidence_url = timing_research.get("timing_results", [{}])[0].get("url", "")
        
        return RationaleTiming(
            why_this_time=reason,
            evidence_url=evidence_url,
            chronotype_match=chronotype_match
        )
    
    def _create_rest_period(
        self,
        end_time: str,
        duration: int,
        reason: str,
        timing_research: Dict
    ) -> RestPeriod:
        """
        Create a rest period
        
        Args:
            end_time: End time of previous task
            duration: Rest duration in minutes
            reason: Reason for rest
            timing_research: Timing research results
        
        Returns:
            RestPeriod object
        """
        end_mins = time_to_minutes(end_time)
        start_mins = end_mins
        end_rest_mins = end_mins + duration
        
        evidence_url = timing_research.get("ultradian_results", [{}])[0].get("url", "")
        
        return RestPeriod(
            task_id=f"rest_{end_time.replace(':', '')}",
            scheduled_time=f"{end_time}-{minutes_to_time(end_rest_mins)}",
            duration_minutes=duration,
            rationale_timing=RationaleTiming(
                why_this_time=reason,
                evidence_url=evidence_url,
                chronotype_match="all"
            )
        )
    
    def _get_available_time_slots(self, bio_profile: UserBioProfile) -> List[str]:
        """
        Get available time slots based on user's peak hours and constraints
        
        Args:
            bio_profile: User's biological profile
        
        Returns:
            List of time slots in "HH:MM-HH:MM" format
        """
        slots = []
        
        # Add peak hours as priority slots
        for peak_range in bio_profile.peak_hours:
            slots.append(peak_range)
        
        # Add other hours if needed
        if len(slots) < 3:
            slots.extend([
                "06:00-07:00",
                "11:00-12:00",
                "14:00-15:00",
                "16:00-17:00"
            ])
        
        return slots[:6]  # Max 6 slots for MVP
    
    def _calculate_insights(self, schedule: List) -> BioInsights:
        """
        Calculate insights about the schedule
        
        Args:
            schedule: List of schedule items
        
        Returns:
            BioInsights object
        """
        total_focus = sum(
            item.duration_minutes
            for item in schedule
            if item.type == "focus"
        )
        
        total_rest = sum(
            item.duration_minutes
            for item in schedule
            if item.type == "rest"
        )
        
        total_time = total_focus + total_rest
        match_score = min(100, int((total_rest / total_time) * 100)) if total_time > 0 else 0
        
        warning = ""
        if total_focus > 90 and total_rest < 20:
            warning = "High focus time detected. Consider adding more rest periods to prevent burnout."
        
        return BioInsights(
            total_focus_time=f"{total_focus} minutes",
            total_rest_time=f"{total_rest} minutes",
            energy_curve_match=f"{match_score}%",
            warning=warning
        )
    
    def _parse_duration(self, iso_duration: str) -> int:
        """
        Parse ISO 8601 duration to minutes
        
        Args:
            iso_duration: Duration string (e.g., "PT30M")
        
        Returns:
            Duration in minutes
        """
        try:
            # Parse PT30M -> 30
            import re
            match = re.search(r'PT(\d+)M', iso_duration)
            if match:
                return int(match.group(1))
            return 30  # Default
        except:
            return 30
    
    def _time_in_range(self, time_str: str, time_range: str) -> bool:
        """
        Check if a time falls within a range
        
        Args:
            time_str: Time string "HH:MM"
            time_range: Time range "HH:MM-HH:MM"
        
        Returns:
            True if time is in range
        """
        try:
            start_str, end_str = time_range.split("-")
            time_mins = time_to_minutes(time_str)
            start_mins = time_to_minutes(start_str)
            end_mins = time_to_minutes(end_str)
            
            return start_mins <= time_mins <= end_mins
        except:
            return False