from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.tools.tavily_search import TavilySearchResults
from app.state import AgentState
from typing import List

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# --- AGENT A: THE TASK BREAKER ---
def agent_task_breaker(state: AgentState):
    print("\n--- [A] TASK BREAKER IS WORKING ---")
    request = state["user_request"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert in 'Atomic Habits'. 
        Break down the goal into small, actionable sub-tasks (< 30 mins).
        Return ONLY a list of strings."""),
        ("user", "Goal: {goal}")
    ])
    
    class TaskList(BaseModel):
        tasks: List[str] = Field(description="List of subtasks")

    chain = prompt | llm.with_structured_output(TaskList)
    result = chain.invoke({"goal": request})
    
    return {"subtasks": result.tasks}

# --- AGENT B: RESEARCH & BIO-HACKER ---
def agent_bio_hacker(state: AgentState):
    print("\n--- [B] BIO-HACKER IS RESEARCHING ---")
    subtasks = state["subtasks"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Bio-Hacker. Optimize schedules based on biology.
        - Deep Work: Morning (High Dopamine).
        - Admin: Afternoon.
        Assign an optimal 'TimeBlock' for each task."""),
        ("user", "Tasks: {tasks}")
    ])
    
    class ScheduleItem(BaseModel):
        task: str
        recommended_time: str
        reason: str

    class OptimizedSchedule(BaseModel):
        schedule: List[ScheduleItem]

    chain = prompt | llm.with_structured_output(OptimizedSchedule)
    result = chain.invoke({"tasks": str(subtasks)})
    
    return {"enriched_tasks": [item.dict() for item in result.schedule]}