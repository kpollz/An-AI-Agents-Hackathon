from typing import Dict, List, Any

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