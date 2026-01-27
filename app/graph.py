from langgraph.graph import StateGraph, END
from app.state import AgentState

# Import Agents
from app.agents.planning import agent_task_breaker, agent_bio_hacker
from app.agents.execution import agent_integration, agent_secretary

def build_graph():
    workflow = StateGraph(AgentState)

    # 1. Add Nodes
    workflow.add_node("task_breaker", agent_task_breaker)
    workflow.add_node("bio_hacker", agent_bio_hacker)
    workflow.add_node("integration", agent_integration)
    workflow.add_node("secretary", agent_secretary)

    # 2. Add Edges (Linear Flow)
    workflow.set_entry_point("task_breaker")
    
    workflow.add_edge("task_breaker", "bio_hacker")
    workflow.add_edge("bio_hacker", "integration")
    workflow.add_edge("integration", "secretary")
    workflow.add_edge("secretary", END)

    # 3. Compile
    return workflow.compile()