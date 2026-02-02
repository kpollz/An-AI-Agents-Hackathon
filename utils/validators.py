from typing import Dict, List, Any
from schemas.final_plan import FinalPlan

def validate_plan(plan: Dict) -> Dict[str, Any]:
    """
    Validate the final plan before syncing to calendar
    
    Args:
        plan: Final plan dictionary
    
    Returns:
        Validation result with 'valid' boolean and 'errors' list
    """
    errors = []
    
    try:
        # Validate minimum rest time
        rest_periods = len(plan.get("rest_periods", []))
        if rest_periods == 0:
            errors.append("Plan must include at least one rest period")
        
        # Validate no task longer than 90 minutes
        schedule = plan.get("editable_schedule", [])
        for item in schedule:
            duration = item.get("editable_fields", {}).get("duration", 0)
            if duration > 90:
                errors.append(f"Task '{item.get('task')}' exceeds 90 minutes. Consider splitting it.")
        
        # Validate total focus time vs rest time ratio
        total_focus = sum(
            item.get("editable_fields", {}).get("duration", 0)
            for item in schedule
            if item.get("editable_fields", {}).get("can_move", True)
        )
        total_rest = sum(
            rp.get("duration_minutes", 0)
            for rp in plan.get("rest_periods", [])
        )
        
        if total_focus > 0 and total_rest / total_focus < 0.15:
            errors.append("Rest time should be at least 15% of focus time to prevent burnout")
        
        # Validate mandatory rest periods
        for rp in plan.get("rest_periods", []):
            if rp.get("type") == "mandatory_break" and rp.get("can_remove", True):
                errors.append("Mandatory rest periods cannot be removed")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "total_focus_time": total_focus,
            "total_rest_time": total_rest
        }
    
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Validation error: {str(e)}"],
            "total_focus_time": 0,
            "total_rest_time": 0
        }

def validate_user_bio_profile(profile: Dict) -> Dict[str, Any]:
    """
    Validate user bio profile from Agent A1
    
    Args:
        profile: User bio profile dictionary
    
    Returns:
        Validation result
    """
    errors = []
    
    required_fields = [
        "chronotype",
        "sleep_time",
        "wake_time",
        "peak_hours",
        "energy_tomorrow"
    ]
    
    for field in required_fields:
        if field not in profile:
            errors.append(f"Missing required field: {field}")
    
    # Validate chronotype
    chronotype = profile.get("chronotype", "")
    if chronotype not in ["lark", "owl", "intermediate"]:
        errors.append(f"Invalid chronotype: {chronotype}. Must be 'lark', 'owl', or 'intermediate'")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

def validate_time_format(time_str: str) -> bool:
    """
    Validate time format (HH:MM or HH:MM-HH:MM)
    
    Args:
        time_str: Time string to validate
    
    Returns:
        True if valid, False otherwise
    """
    try:
        if "-" in time_str:
            start, end = time_str.split("-")
            # Validate both start and end times
            return validate_time_format(start) and validate_time_format(end)
        else:
            # Single time format HH:MM
            hours, minutes = time_str.split(":")
            return (0 <= int(hours) <= 23) and (0 <= int(minutes) <= 59)
    except:
        return False

def check_schedule_conflicts(schedule: List[Dict]) -> List[Dict]:
    """
    Check for overlapping time slots in schedule
    
    Args:
        schedule: List of schedule items with time ranges
    
    Returns:
        List of conflicts found
    """
    conflicts = []
    
    # Parse time ranges to minutes from midnight
    time_slots = []
    for item in schedule:
        time_range = item.get("time", "")
        if "-" in time_range:
            start, end = time_range.split("-")
            start_mins = time_to_minutes(start)
            end_mins = time_to_minutes(end)
            time_slots.append((start_mins, end_mins, item))
    
    # Check for overlaps
    for i, (s1, e1, item1) in enumerate(time_slots):
        for j, (s2, e2, item2) in enumerate(time_slots):
            if i >= j:
                continue
            # Check if intervals overlap
            if not (e1 <= s2 or e2 <= s1):
                conflicts.append({
                    "time1": item1.get("time"),
                    "task1": item1.get("task"),
                    "time2": item2.get("time"),
                    "task2": item2.get("task"),
                    "overlap": True
                })
    
    return conflicts

def time_to_minutes(time_str: str) -> int:
    """
    Convert time string HH:MM to minutes from midnight
    
    Args:
        time_str: Time string in HH:MM format
    
    Returns:
        Minutes from midnight
    """
    try:
        hours, minutes = time_str.split(":")
        return int(hours) * 60 + int(minutes)
    except:
        return 0

def minutes_to_time(minutes: int) -> str:
    """
    Convert minutes from midnight to time string HH:MM
    
    Args:
        minutes: Minutes from midnight
    
    Returns:
        Time string in HH:MM format
    """
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"