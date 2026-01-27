import os
from dotenv import load_dotenv
from app.graph import build_graph

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Initialize the Graph
    app = build_graph()
    
    # Define Input
    initial_input = {
        "user_request": "I want to research and write a document about Multi-Agent Systems.",
        "user_memory": "User works best in 25-minute pomodoro sprints."
    }
    
    print("🚀 STARTING PRODUCTIVITY SYSTEM...")
    
    # Run
    final_state = app.invoke(initial_input)
    
    print("\n✅ WORKFLOW FINISHED.")
    print(f"Updated Memory: {final_state['user_memory']}")