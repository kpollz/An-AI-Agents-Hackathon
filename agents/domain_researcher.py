import os
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from schemas.agent2_output import (
    DomainResearcherOutput,
    Task,
    ProTip
)
from utils.web_search import WebSearchTool, MockWebSearchTool

class DomainResearcherAgent:
    """
    Agent A2: Domain Researcher
    Researches workflow + Pro Tips with evidence citations
    """
    
    def __init__(self, model: str = "gemini-2.5-flash-lite", use_mock_search: bool = False):
        """
        Initialize Domain Researcher Agent
        
        Args:
            model: Gemini model to use (default: gemini-2.5-flash-lite)
            use_mock_search: If True, use mock search tool for testing
        """
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=0.3,
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
        
        self.system_prompt = """You are a research expert specializing in productivity, health, and habit formation.
Your task is to research workflows, best practices, and scientific tips for the user's goal.

RESEARCH REQUIREMENTS:
1. Use web search to find:
   - Best workflow steps for the activity
   - Scientific studies supporting each step
   - Professional tips with evidence
   - Common pitfalls to avoid

2. For each task:
   - Provide a clear name and description
   - Estimate duration (ISO 8601 format, e.g., PT30M for 30 minutes)
   - Rate difficulty (high/medium/low)
   - Include evidence with source URL and authority

3. For pro tips:
   - Provide actionable advice
   - Link to specific task it applies to
   - Include study summary and applicability

CITATION RULES:
- Only use high-authority sources (research papers, well-known blogs, reputable organizations)
- Every recommendation must have a source URL
- If sources conflict, prioritize scientific research over general advice
- Include study summary that explains why this works

Return ONLY structured JSON output, no additional text."""
    
    def research_domain(
        self,
        goal: str,
        bio_context: Dict
    ) -> DomainResearcherOutput:
        """
        Research domain for the given goal
        
        Args:
            goal: Clarified goal from Agent A1
            bio_context: User's biological context
        
        Returns:
            DomainResearcherOutput with tasks and tips
        """
        # Extract activity from goal
        activity = self._extract_activity(goal)
        
        # Search for workflow
        workflow_results = self.search_tool.search_workflow(
            activity=activity,
            task_type="workflow"
        )
        
        # Search for tips
        tips_results = self.search_tool.search_workflow(
            activity=activity,
            task_type="tips"
        )
        
        # Generate tasks with evidence
        tasks = self._generate_tasks(
            goal=goal,
            activity=activity,
            workflow_results=workflow_results
        )
        
        # Generate pro tips with evidence
        tips = self._generate_tips(
            activity=activity,
            tips_results=tips_results,
            tasks=tasks
        )
        
        # Generate warnings
        warnings = self._generate_warnings(goal, activity)
        
        return DomainResearcherOutput(
            domain=activity,
            tasks=tasks,
            pro_tips=tips,
            warnings=warnings
        )
    
    def _extract_activity(self, goal: str) -> str:
        """
        Extract the main activity from goal
        
        Args:
            goal: SMART goal
        
        Returns:
            Activity name (e.g., "running", "writing report")
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Extract the main activity from the goal. Return only the activity name, lowercase, 2-3 words max."),
            ("human", "Goal: {goal}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"goal": goal})
        
        # Clean up response
        activity = response.content.strip().lower()
        # Remove articles and prepositions
        activity = " ".join([w for w in activity.split() if w not in ["a", "an", "the", "to", "for"]])
        
        return activity if activity else "activity"
    
    def _generate_tasks(
        self,
        goal: str,
        activity: str,
        workflow_results: List[Dict]
    ) -> List[Task]:
        """
        Generate tasks from workflow search results
        
        Args:
            goal: User's goal
            activity: Activity name
            workflow_results: Search results from web search
        
        Returns:
            List of Task objects
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", """Goal: {goal}
Activity: {activity}

Search Results:
{search_results}

Generate 3-5 key tasks for this activity. Each task must have evidence from the search results.
If search results are limited, use general best practices but note it.""")
        ])
        
        # Format search results
        search_results_text = "\n".join([
            f"- {r.get('title', '')}: {r.get('content', '')[:200]}... (URL: {r.get('url', '')})"
            for r in workflow_results
        ])
        
        # Use structured output
        from pydantic import BaseModel
        from pydantic import Field
        
        class TaskList(BaseModel):
            tasks: List[Task]
        
        chain = prompt | self.llm.with_structured_output(TaskList)
        result = chain.invoke({
            "goal": goal,
            "activity": activity,
            "search_results": search_results_text
        })
        
        return result.tasks
    
    def _generate_tips(
        self,
        activity: str,
        tips_results: List[Dict],
        tasks: List[Task]
    ) -> List[ProTip]:
        """
        Generate pro tips from search results
        
        Args:
            activity: Activity name
            tips_results: Search results for tips
            tasks: List of tasks to link tips to
        
        Returns:
            List of ProTip objects
        """
        if not tasks:
            return []
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", """Activity: {activity}

Available Tasks:
{task_list}

Search Results for Tips:
{search_results}

Generate 3-5 pro tips. Each tip must apply to one of the tasks above.
Include study evidence from search results.""")
        ])
        
        # Format task list
        task_list_text = "\n".join([
            f"- {task.task_id}: {task.name}"
            for task in tasks
        ])
        
        # Format search results
        search_results_text = "\n".join([
            f"- {r.get('title', '')}: {r.get('content', '')[:200]}... (URL: {r.get('url', '')})"
            for r in tips_results
        ])
        
        # Use structured output
        from pydantic import BaseModel
        
        class TipList(BaseModel):
            pro_tips: List[ProTip]
        
        chain = prompt | self.llm.with_structured_output(TipList)
        result = chain.invoke({
            "activity": activity,
            "task_list": task_list_text,
            "search_results": search_results_text
        })
        
        return result.pro_tips
    
    def _generate_warnings(self, goal: str, activity: str) -> List[str]:
        """
        Generate common pitfalls and warnings
        
        Args:
            goal: User's goal
            activity: Activity name
        
        Returns:
            List of warning messages
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert on common mistakes people make when starting new activities."),
            ("human", "Goal: {goal}\nActivity: {activity}\n\nList 3-5 common pitfalls beginners make. Return as a JSON array of strings.")
        ])
        
        # Use structured output
        from pydantic import BaseModel
        
        class WarningList(BaseModel):
            warnings: List[str]
        
        chain = prompt | self.llm.with_structured_output(WarningList)
        result = chain.invoke({
            "goal": goal,
            "activity": activity
        })
        
        return result.warnings