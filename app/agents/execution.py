from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.state import AgentState
from app.tools.external import add_to_todoist, block_google_calendar

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# --- AGENT C: INTEGRATION SPECIALIST ---
def agent_integration(state: AgentState):
    print("\n--- [C] INTEGRATION SPECIALIST IS SYNCING ---")
    enriched_tasks = state["enriched_tasks"]
    
    logs = []
    for item in enriched_tasks:
        # Execute Tools
        log_todo = add_to_todoist(item['task'], "today")
        log_cal = block_google_calendar(item['task'], item['recommended_time'])
        
        logs.append(f"{log_todo} | {log_cal}")
        print(f"-> Synced: {item['task']}")

    # Mock status for Agent D
    return {"execution_status": "All tasks synced successfully. User usually completes Morning tasks well."}

# --- AGENT D: THE SECRETARY ---
def agent_secretary(state: AgentState):
    print("\n--- [D] SECRETARY IS ANALYZING ---")
    status = state["execution_status"]
    current_memory = state.get("user_memory", "No prior memory.")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Secretary managing User Memory.
        Update the memory based on today's report."""),
        ("user", "Old Memory: {memory}\nReport: {report}")
    ])
    
    chain = prompt | llm
    result = chain.invoke({"memory": current_memory, "report": status})
    
    return {"user_memory": result.content}