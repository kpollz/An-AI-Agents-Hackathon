"""
Agent A1: Goal Clarifier
Bước 1: Break multiple goals from user input
Bước 2: Clarify each goal (deadline, duration, energy)
"""
import os
from typing import Dict, Any, Optional, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from schemas.agent1_output import GoalClarifierOutput, UserBioProfile


class GoalClarifierAgent:
    """
    Agent A1: Goal Clarifier
    Two-phase process:
    1. Break: Extract multiple goals from user input
    2. Clarify: Get deadline, duration, energy for each goal
    """
    
    def __init__(self, model: str = "gemini-2.5-flash-lite"):
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=0.7,
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Phase 1: Break goals
        self.break_prompt = """You are a goal analyzer. Extract ALL distinct goals/tasks from the user's message.

RULES:
1. If user mentions multiple activities, break them into separate goals
2. Each goal should be specific and actionable
3. Return as a list of goal descriptions

Examples:
User: "Tôi muốn viết báo cáo và chạy bộ"
→ Goals: ["Viết báo cáo", "Chạy bộ"]

User: "Mai tôi cần học bài và đi siêu thị mua đồ"
→ Goals: ["Học bài", "Đi siêu thị mua đồ"]

User: "Tôi muốn hoàn thiện báo cáo kỹ thuật về Open Vocabulary Object Detection đồng thờ
i thì làm xong cũng muốn chạy bộ một chút"
→ Goals: ["Hoàn thiện báo cáo kỹ thuật về Open Vocabulary Object Detection", "Chạy bộ"]"""

        # Phase 2: Clarify each goal
        self.clarify_prompt = """You are a friendly coach helping clarify a specific goal.

YOUR JOB for this goal:
1. Understand WHAT needs to be done
2. Understand WHEN (deadline)
3. Understand HOW LONG (estimated duration)
4. Understand user's ENERGY LEVEL

RULES:
- Ask only 1-2 questions per turn
- If the goal is vague, help make it specific
- Once you have: deadline + duration + energy, confirm completion
- Vietnamese responses only"""
        
        self.conversation_history = []
        self.goals_list: List[str] = []  # Multiple goals
        self.current_goal_idx: int = 0   # Which goal we're clarifying
        self.collected_info: Dict[str, Any] = {}  # Info for current goal
        self.all_goals_info: List[Dict] = []  # Info for all goals
    
    def _break_goals(self, user_input: str) -> List[str]:
        """Phase 1: Break user input into multiple goals"""
        from pydantic import BaseModel, Field
        from typing import List as TypingList
        
        class GoalsList(BaseModel):
            goals: TypingList[str] = Field(description="List of distinct goals from user input")
        
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.break_prompt),
                ("human", f"User input: {user_input}\n\nExtract all goals as a list.")
            ])
            
            chain = prompt | self.llm.with_structured_output(GoalsList)
            result = chain.invoke({})
            
            print(f"DEBUG: Broken goals: {result.goals}")
            return result.goals if result.goals else [user_input]
            
        except Exception as e:
            print(f"DEBUG: Break goals error: {e}")
            # Fallback: treat entire input as single goal
            return [user_input]
    
    def _extract_info(self, user_input: str) -> Dict[str, Any]:
        """Extract clarification info for current goal"""
        from pydantic import BaseModel, Field
        from typing import Optional as TypingOptional
        
        class ExtractedInfo(BaseModel):
            deadline: TypingOptional[str] = Field(None, description="When it needs to be done")
            estimated_duration: TypingOptional[str] = Field(None, description="Estimated time")
            energy_level: TypingOptional[str] = Field(None, description="high/medium/low")
            
        extraction_prompt = f"""Current goal: "{self.goals_list[self.current_goal_idx] if self.goals_list else 'Unknown'}"

Extract deadline, duration, and energy level from this user message.
If user mentions "mai", "ngày mai", "tomorrow" → deadline = "tomorrow"
If user mentions "chiều mai", "sáng mai" → include time of day.

User message: "{user_input}"""
        
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Extract structured information. Be precise."),
                ("human", extraction_prompt)
            ])
            
            chain = prompt | self.llm.with_structured_output(ExtractedInfo)
            result = chain.invoke({})
            
            return {k: v for k, v in result.dict().items() if v is not None}
        except Exception as e:
            print(f"DEBUG: Extraction error: {e}")
            return {}
    
    def chat(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Handle conversation with user
        Phase 1: Break goals (first turn)
        Phase 2: Clarify each goal
        """
        # Initialize or merge context
        if context:
            self.collected_info.update(context)
        
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # PHASE 1: First turn - Break goals
        if not self.goals_list:
            self.goals_list = self._break_goals(user_input)
            self.current_goal_idx = 0
            
            if len(self.goals_list) > 1:
                response = f"Tuyệt vợi! Mình thấy bạn có {len(self.goals_list)} mục tiêu:\n"
                for i, goal in enumerate(self.goals_list, 1):
                    response += f"  {i}. {goal}\n"
                response += f"\nHãy cùng làm rõ từng mục tiêu nhé! "
                response += f"Bắt đầu với mục tiêu 1: **{self.goals_list[0]}**\n\n"
                response += "Bạn dự định hoàn thành vào **khi nào** và mất khoảng **bao lâu**?"
            else:
                response = f"Tuyệt vợi! Bạn muốn: **{self.goals_list[0]}**\n\n"
                response += "Bạn dự định hoàn thành vào **khi nào** và mất khoảng **bao lâu**?"
            
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return {
                "response": response,
                "context_complete": False,
                "collected_info": {"goals": self.goals_list}
            }
        
        # PHASE 2: Clarify current goal
        extracted = self._extract_info(user_input)
        if extracted:
            self.collected_info.update(extracted)
            print(f"DEBUG: Extracted for goal {self.current_goal_idx + 1}: {extracted}")
        
        # Check if current goal is complete
        has_deadline = "deadline" in self.collected_info and self.collected_info["deadline"]
        has_duration = "estimated_duration" in self.collected_info and self.collected_info["estimated_duration"]
        
        current_goal_complete = has_deadline  # Minimum: need deadline
        
        print(f"DEBUG: Goal {self.current_goal_idx + 1}/{len(self.goals_list)} complete: {current_goal_complete}")
        
        if current_goal_complete:
            # Save current goal info
            goal_info = {
                "goal": self.goals_list[self.current_goal_idx],
                "deadline": self.collected_info.get("deadline", ""),
                "estimated_duration": self.collected_info.get("estimated_duration", ""),
                "energy_level": self.collected_info.get("energy_level", "medium")
            }
            self.all_goals_info.append(goal_info)
            
            # Move to next goal
            self.current_goal_idx += 1
            self.collected_info = {}  # Reset for next goal
            
            # Check if all goals done
            if self.current_goal_idx >= len(self.goals_list):
                # All goals clarified
                response = "Mình đã hiểu rõ. Để mình nghiên cứu cách tối ưu nhất cho bạn nhé!"
                self.conversation_history.append({"role": "assistant", "content": response})
                
                return {
                    "response": response,
                    "context_complete": True,
                    "collected_info": {
                        "goals": self.goals_list,
                        "all_goals_info": self.all_goals_info
                    }
                }
            else:
                # Next goal
                response = f"Tiếp theo, hãy làm rõ mục tiêu {self.current_goal_idx + 1}: **{self.goals_list[self.current_goal_idx]}**\n\n"
                response += "Bạn dự định hoàn thành vào **khi nào**?"
                self.conversation_history.append({"role": "assistant", "content": response})
                
                return {
                    "response": response,
                    "context_complete": False,
                    "collected_info": {"goals": self.goals_list, "current_idx": self.current_goal_idx}
                }
        
        # Still need more info for current goal
        missing = []
        if not has_deadline:
            missing.append("deadline (khi nào)")
        if not has_duration:
            missing.append("thờ gian dự kiến")
        
        context_str = f"Mục tiêu hiện tại: {self.goals_list[self.current_goal_idx]}\n"
        context_str += f"Đã có: {self.collected_info}\n"
        context_str += f"Còn thiếu: {', '.join(missing)}"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.clarify_prompt),
            ("human", f"{context_str}\n\nUser vừa nói: {user_input}\n\nHỏi ngắn gọn về thông tin còn thiếu.")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({})
        response_text = response.content
        
        self.conversation_history.append({"role": "assistant", "content": response_text})
        
        return {
            "response": response_text,
            "context_complete": False,
            "collected_info": self.collected_info.copy()
        }
    
    def generate_goal_spec(self, user_request: str, bio_context: Dict) -> GoalClarifierOutput:
        """Generate final goal specification for all goals"""
        
        # Get all goals info
        all_goals_info = bio_context.get("all_goals_info", [])
        goals_list = bio_context.get("goals", [])
        
        if not all_goals_info and goals_list:
            # Fallback: create from goals list
            all_goals_info = [{"goal": g, "deadline": "tomorrow", "estimated_duration": "1 hour", "energy_level": "medium"} for g in goals_list]
        
        # Combine all goals into one description
        if len(all_goals_info) == 1:
            combined_goal = all_goals_info[0]["goal"]
            main_deadline = all_goals_info[0].get("deadline", "tomorrow")
            main_energy = all_goals_info[0].get("energy_level", "medium")
        else:
            goal_descriptions = [f"{i+1}. {g['goal']}" for i, g in enumerate(all_goals_info)]
            combined_goal = "Hoàn thành các mục tiêu: " + "; ".join([g['goal'] for g in all_goals_info])
            main_deadline = all_goals_info[0].get("deadline", "tomorrow")
            main_energy = all_goals_info[0].get("energy_level", "medium")
        
        # Generate SMART goal
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Convert goals into a SMART goal. Be concise."),
            ("human", f"Goals: {combined_goal}\nDeadline: {main_deadline}\nEnergy: {main_energy}")
        ])
        
        try:
            chain = prompt | self.llm
            result = chain.invoke({})
            clarified_goal = result.content.strip()
        except:
            clarified_goal = combined_goal
        
        # Create bio profile with defaults
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
            energy_tomorrow=main_energy,
            physical_constraints=bio_context.get("physical_constraints", [])
        )
        
        return GoalClarifierOutput(
            clarified_goal=clarified_goal,
            user_bio_profile=bio_profile,
            conversation_complete=True
        )
    
    def reset(self):
        """Reset for new conversation"""
        self.conversation_history = []
        self.goals_list = []
        self.current_goal_idx = 0
        self.collected_info = {}
        self.all_goals_info = []
