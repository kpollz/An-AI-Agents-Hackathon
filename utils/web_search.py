import os
from typing import List, Dict, Optional
from tavily import TavilyClient
import json

class WebSearchTool:
    """Wrapper for Tavily Web Search API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Tavily client
        
        Args:
            api_key: Tavily API key. If None, reads from TAVILY_API_KEY env var
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables")
        
        self.client = TavilyClient(api_key=self.api_key)
    
    def search(
        self,
        query: str,
        max_results: int = 5,
        include_domains: Optional[List[str]] = None,
        search_depth: str = "advanced"
    ) -> Dict:
        """
        Perform web search using Tavily API
        
        Args:
            query: Search query
            max_results: Maximum number of results (default: 5)
            include_domains: List of domains to include (optional)
            search_depth: Search depth - "basic" or "advanced" (default: "advanced")
        
        Returns:
            Dict containing search results
        """
        try:
            response = self.client.search(
                query=query,
                max_results=max_results,
                include_domains=include_domains,
                search_depth=search_depth
            )
            return response
        except Exception as e:
            print(f"Error in web search: {e}")
            return {"results": []}
    
    def get_reliable_sources(self) -> List[str]:
        """
        Get list of reliable domains for research
        
        Returns:
            List of reliable domain names
        """
        return [
            "verywellmind.com",
            "healthline.com",
            "jamesclear.com",
            "ncbi.nlm.nih.gov",
            "todoist.com",
            "lifehacker.com",
            "nytimes.com",
            "hbr.org",
            "psychologytoday.com",
            "mayoclinic.org",
            "nature.com",
            "science.org"
        ]
    
    def format_search_result(self, result: Dict) -> Dict:
        """
        Format a single search result into structured data
        
        Args:
            result: Raw search result from Tavily
        
        Returns:
            Formatted result dict
        """
        return {
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", ""),
            "score": result.get("score", 0.0)
        }
    
    def search_workflow(
        self,
        activity: str,
        task_type: str = "workflow"
    ) -> List[Dict]:
        """
        Search for workflow, tips, or evidence for a specific activity
        
        Args:
            activity: Activity name (e.g., "running", "writing")
            task_type: Type of search - "workflow", "tips", "timing", "evidence"
        
        Returns:
            List of formatted search results
        """
        queries = {
            "workflow": f"best workflow for {activity} beginners steps",
            "tips": f"scientific tips for {activity} performance study",
            "timing": f"best time of day for {activity} chronotype research",
            "evidence": f"study evidence benefits of {activity} research"
        }
        
        query = queries.get(task_type, f"{activity} guide")
        
        # Use reliable sources
        domains = self.get_reliable_sources()
        
        results = self.search(
            query=query,
            max_results=5,
            include_domains=domains,
            search_depth="advanced"
        )
        
        return [
            self.format_search_result(r) 
            for r in results.get("results", [])
        ]


# Mock version for testing without API key
class MockWebSearchTool:
    """Mock web search tool for testing without API key"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    def search(self, query: str, max_results: int = 5, **kwargs) -> Dict:
        """Mock search that returns sample results"""
        return {
            "results": [
                {
                    "title": f"Best practices for {query}",
                    "url": "https://example.com/article",
                    "content": "This is a mock search result for testing purposes.",
                    "score": 0.9
                }
            ]
        }
    
    def search_workflow(self, activity: str, task_type: str = "workflow") -> List[Dict]:
        """Mock search workflow"""
        return self.search(f"{activity} {task_type}")["results"]
    
    def get_reliable_sources(self) -> List[str]:
        """Get reliable sources"""
        return ["example.com", "mocksource.com"]
    
    def format_search_result(self, result: Dict) -> Dict:
        """Format search result"""
        return result