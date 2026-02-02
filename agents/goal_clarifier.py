import os
from typing import Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from schemas.agent1_output import GoalClarifierOutput, UserBioProfile

class GoalClarifierAgent:
    """
    Agent A1: Goal Clarifier
    Collects detailed biological and contextual information from user
    """
    
    def __init__(self, model: str = "gemini-2.5-flash-lite"):
        """
        Initialize Goal Clarifier Agent
        
        Args:
            model: Gemini model to use (default: gemini-2.5-flash-lite)
        """
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=0.7,
            api_key=os.getenv("GOOGLE_API_KEY")  # Will read from GOOGLE_API_KEY env var
        )
        
        self.system_prompt = """You are a friendly, patient coach helping someone who tends to procrastinate.
Your task is to gather detailed information about their goal and biological context.

INFORMATION TO COLLECT:
1. Mục tiêu cụ thể (SMART format): What exactly do they want to achieve?
2. Deadline hoặc khung thời gian cứng: When do they need to complete it?
3. Chronotype:
   - Morning Lark (dậy sớm, làm việc tốt buổi sáng)
   - Night Owl (tỉnh thức tối, làm việc tốt buổi tối)
   - Intermediate (nằm ở giữa)
4. Giờ ngủ/thức dậy thường lệ
5. Meal timing: Ăn sáng/trưa/tối thường lúc mấy giờ?
6. Peak hours: Giờ nào trong ngày họ tỉnh táo nhất?
7. Slump hours: Giờ nào họ buồn ngủ/mệt nhất?
8. Fixed commitments: Có họp/công việc cố định nào ngày mai không?
9. Energy level tomorrow: high/medium/low?
10. Physical constraints: Có đau nhức, bệnh tật gì không?

CONVERSATION RULES:
- Chỉ hỏi 1-2 câu mỗi lượt để không overwhelm user
- Nếu user trả lời mơ hồ, hỏi lại theo cách cụ thể hơn
- Nếu user không biết chronotype, gợi ý họ làm bài test online hoặc default là "intermediate"
- Khi đủ thông tin, kết thúc bằng câu: "Mình đã hiểu rõ. Để mình nghiên cứu cách tối ưu nhất cho bạn nhé!"

IMPORTANT: Bạn KHÔNG ĐƯỢC đưa ra kế hoạch ngay lập tức. Phải hỏi đủ thông tin trước."""
        
        self.conversation_history = []
    
    def chat(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Handle multi-turn conversation with user
        
        Args:
            user_input: User's message
            context: Current conversation context (collected info so far)
        
        Returns:
            Dict containing:
            - response: Agent's response message
            - context_complete: Boolean indicating if all info collected
            - collected_info: Dict of information collected so far
        """
        if context is None:
            context = {}
        
        # Add user input to history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Build prompt with current context
        context_str = self._format_context(context)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", """Context đã thu thập:
{context}

User nói: {input}

Hãy trả lời người dùng. Nếu cần thêm thông tin, hãy hỏi. Nếu đã đủ, hãy thông báo.""")
        ])
        
        # Generate response
        chain = prompt | self.llm
        response = chain.invoke({
            "context": context_str,
            "input": user_input
        })
        
        response_text = response.content
        
        # Add response to history
        self.conversation_history.append({"role": "assistant", "content": response_text})
        
        # Check if conversation is complete
        is_complete = self._check_conversation_complete(context, response_text)
        
        return {
            "response": response_text,
            "context_complete": is_complete,
            "collected_info": context
        }
    
    def generate_goal_spec(self, user_request: str, bio_context: Dict) -> GoalClarifierOutput:
        """
        Generate final goal specification from collected information
        
        Args:
            user_request: Original user request
            bio_context: Collected biological context
        
        Returns:
            GoalClarifierOutput object
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at goal setting and SMART goal formulation.
Convert the user's vague goal into a SMART goal (Specific, Measurable, Achievable, Relevant, Time-bound).

Return ONLY the JSON output, no additional text."""),
            ("human", """User Request: {request}

Biological Context:
{bio_context}

Generate a SMART goal and structure the bio context properly.""")
        ])
        
        # Parse bio context
        bio_profile = UserBioProfile(
            chronotype=bio_context.get("chronotype", "intermediate"),
            sleep_time=bio_context.get("sleep_time", "23:00"),
            wake_time=bio_context.get("wake_time", "07:00"),
            meal_times=bio_context.get("meal_times", {
                "breakfast": "07:30",
                "lunch": "12:00",
                "dinner": "19:00"
            }),
            peak_hours=bio_context.get("peak_hours", ["09:00-11:00", "15:00-17:00"]),
            slump_hours=bio_context.get("slump_hours", []),
            fixed_commitments=bio_context.get("fixed_commitments", []),
            energy_tomorrow=bio_context.get("energy_tomorrow", "medium"),
            physical_constraints=bio_context.get("physical_constraints", [])
        )
        
        # Use structured output
        from langchain_core.pydantic_v1 import BaseModel
        from pydantic import Field
        
        class SmartGoal(BaseModel):
            clarified_goal: str = Field(description="SMART format goal")
        
        chain = prompt | self.llm.with_structured_output(SmartGoal)
        result = chain.invoke({
            "request": user_request,
            "bio_context": bio_profile.dict()
        })
        
        return GoalClarifierOutput(
            clarified_goal=result.clarified_goal,
            user_bio_profile=bio_profile,
            conversation_complete=True
        )
    
    def _format_context(self, context: Dict) -> str:
        """Format context for display"""
        if not context:
            return "Chưa có thông tin"
        
        lines = []
        for key, value in context.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)
    
    def _check_conversation_complete(self, context: Dict, response: str) -> bool:
        """Check if all required information is collected"""
        required_fields = [
            "chronotype",
            "sleep_time",
            "wake_time",
            "peak_hours",
            "energy_tomorrow"
        ]
        
        has_all_fields = all(field in context for field in required_fields)
        has_completion_phrase = "đã hiểu rõ" in response.lower() or "nghiên cứu" in response.lower()
        
        return has_all_fields and has_completion_phrase
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []