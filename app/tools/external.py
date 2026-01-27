def add_to_todoist(task_name: str, due_string: str) -> str:
    """
    Mock function to add task to Todoist.
    Replace with actual Todoist API call.
    """
    # TODO: Implement Todoist API here
    # api.add_task(content=task_name, due_string=due_string)
    return f"[Todoist] Added '{task_name}' due {due_string}"

def block_google_calendar(task_name: str, time_block: str) -> str:
    """
    Mock function to add event to Google Calendar.
    Replace with actual Google Calendar API call.
    """
    # TODO: Implement Google Calendar API here
    # service.events().insert(...)
    return f"[GCal] Blocked '{task_name}' in {time_block}"