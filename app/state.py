from typing import List, TypedDict, Dict, Any

class AgentState(TypedDict):
    """
    State dictionary to hold data flow between agents.
    """
    user_request: str           # Input ban đầu
    subtasks: List[str]         # Output từ Agent A
    enriched_tasks: List[Dict[str, Any]] # Output từ Agent B (có thêm time block)
    execution_status: str       # Output từ Agent C (kết quả chạy tool)
    user_memory: str            # Output từ Agent D (bộ nhớ dài hạn)