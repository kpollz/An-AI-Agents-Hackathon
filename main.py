import os
from dotenv import load_dotenv
from typing import Dict, Any

# Import agents
from agents.goal_clarifier import GoalClarifierAgent
from agents.domain_researcher import DomainResearcherAgent
from agents.bio_optimizer import BioOptimizerAgent
from agents.json_formatter import JSONFormatterAgent

# Load environment variables
load_dotenv()


class AtomicTaskPlanner:
    """
    Main orchestrator for Atomic Task Planner system
    Runs the complete pipeline: A1 → A2 → A3 → A4
    """
    
    def __init__(self, use_mock_search: bool = False, model: str = "gemini-2.0-flash-exp"):
        """
        Initialize ATP system
        
        Args:
            use_mock_search: If True, use mock search for testing
            model: Gemini model to use
        """
        print("🚀 Initializing Atomic Task Planner...")
        
        # Check for required API keys
        if not os.getenv("GOOGLE_API_KEY"):
            print("⚠️  Warning: GOOGLE_API_KEY not found in environment variables")
            print("Set it in .env file or as environment variable")
        
        # Initialize agents
        self.agent_a1 = GoalClarifierAgent(model=model)
        self.agent_a2 = DomainResearcherAgent(
            model=model,
            use_mock_search=use_mock_search
        )
        self.agent_a3 = BioOptimizerAgent(
            model=model,
            use_mock_search=use_mock_search
        )
        self.agent_a4 = JSONFormatterAgent()
        
        print("✅ All agents initialized successfully")
    
    def run_interactive_mode(self):
        """
        Run ATP in interactive mode - collects user info through conversation
        """
        print("\n" + "="*60)
        print("🎯 ATOMIC TASK PLANNER - INTERACTIVE MODE")
        print("="*60)
        print("\nChào bạn! Tôi là AI Coach giúp bạn chuyển đổi mục tiêu mơ hồ")
        print("thành chuỗi hành động siêu nhỏ có dẫn chứng khoa học.")
        print("\nHãy cho tôi biết mục tiêu của bạn (ví dụ: 'Ngày mai chạy 5km')")
        print("-"*60)
        
        # Get user input
        user_request = input("\n👤 Bạn: ").strip()
        
        if not user_request:
            print("❌ Không có đầu vào. Thoát...")
            return
        
        # Run Agent A1: Goal Clarifier (Interactive)
        print("\n" + "="*60)
        print("[A1] GOAL CLARIFIER - Thu thập thông tin sinh học")
        print("="*60)
        
        # Reset agent for new conversation
        self.agent_a1.reset()
        
        bio_context = {}
        conversation_complete = False
        
        while not conversation_complete:
            result = self.agent_a1.chat(user_request, bio_context)
            
            # IMPORTANT: Update bio_context with collected info from this turn
            bio_context = result['collected_info']
            
            print(f"\n🤖 Coach: {result['response']}")
            
            if result['context_complete']:
                conversation_complete = True
                print("\n✅ Đã thu thập đủ thông tin!")
                break
            else:
                user_request = input("\n👤 Bạn: ").strip()
                if not user_request:
                    print("❌ Đã hủy.")
                    return
        
        # Generate final goal specification
        if not bio_context or ('goal' not in bio_context and 'goals' not in bio_context):
            print("❌ Không có đủ thông tin. Vui lòng bắt đầu lại.")
            return
        
        print("\nĐang tạo mục tiêu SMART...")
        a1_output = self.agent_a1.generate_goal_spec(user_request, bio_context)
        
        # Display results
        goals_list = bio_context.get('goals', [])
        if len(goals_list) > 1:
            print(f"\n📌 Đã làm rõ {len(goals_list)} mục tiêu:")
            for i, goal in enumerate(goals_list, 1):
                print(f"   {i}. {goal}")
        print(f"\n🎯 Mục tiêu SMART: {a1_output.clarified_goal}")
        print(f"\n🧬 Chronotype: {a1_output.user_bio_profile.chronotype}")
        print(f"⏰ Peak hours: {', '.join(a1_output.user_bio_profile.peak_hours)}")
        print(f"⚡ Energy: {a1_output.user_bio_profile.energy_tomorrow}")
        
        # Run Agent A2: Domain Researcher
        print("\n" + "="*60)
        print("[A2] DOMAIN RESEARCHER - Tìm kiếm workflow và tips")
        print("="*60)
        print("\nĐang nghiên cứu...")
        
        a2_output = self.agent_a2.research_domain(
            goal=a1_output.clarified_goal,
            bio_context=a1_output.user_bio_profile.dict()
        )
        
        print(f"\n📚 Domain: {a2_output.domain}")
        print(f"📋 Tasks: {len(a2_output.tasks)} tasks")
        print(f"💡 Tips: {len(a2_output.pro_tips)} pro tips")
        
        if a2_output.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in a2_output.warnings:
                print(f"   - {warning}")
        
        # Run Agent A3: Bio-Optimizer
        print("\n" + "="*60)
        print("[A3] BIO-OPTIMIZER - Tối ưu sinh học và lịch trình")
        print("="*60)
        print("\nĐang tối ưu lịch trình...")
        
        a3_output = self.agent_a3.optimize_schedule(
            tasks=a2_output.tasks,
            tips=a2_output.pro_tips,
            bio_profile=a1_output.user_bio_profile
        )
        
        print(f"\n📅 Scheduled items: {len(a3_output.optimized_schedule)}")
        print(f"⏱️  Focus time: {a3_output.bio_insights.total_focus_time}")
        print(f"☕ Rest time: {a3_output.bio_insights.total_rest_time}")
        print(f"🎯 Match score: {a3_output.bio_insights.energy_curve_match}")
        
        if a3_output.bio_insights.warning:
            print(f"\n⚠️  {a3_output.bio_insights.warning}")
        
        # Run Agent A4: JSON Formatter
        print("\n" + "="*60)
        print("[A4] JSON FORMATTER - Tạo file kế hoạch")
        print("="*60)
        
        final_plan = self.agent_a4.format_final_plan(
            optimized_schedule=a3_output.optimized_schedule,
            bio_insights=a3_output.bio_insights,
            goal=a1_output.clarified_goal,
            bio_profile=a1_output.user_bio_profile
        )
        
        # Save to file
        output_path = "output/tomorrow_plan.json"
        self.agent_a4.save_to_file(final_plan, output_path)
        
        # Generate markdown summary
        summary = self.agent_a4.generate_summary_markdown(final_plan)
        
        print("\n" + "="*60)
        print("📄 TÓM TẮT KẾ HOẠCH")
        print("="*60)
        print(summary)
        
        # Instructions for next steps
        print("\n" + "="*60)
        print("📝 CÁC BƯỚC TIẾP THEO")
        print("="*60)
        print("\n1. Review file kế hoạch: output/tomorrow_plan.json")
        print("2. Chỉnh sửa nếu cần (thay đổi giờ, xóa task, v.v.)")
        print("3. Khi đã hài lòng, chạy lệnh sync:")
        print("   python standalone/calendar_sync.py --input output/tomorrow_plan.json")
        print("\nHoặc chỉnh sửa trong JSON và đổi 'calendar_ready' thành true")
        print("="*60)
        
        return final_plan


def main():
    """Main entry point"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     ATOMIC TASK PLANNER (ATP) v2.0                       ║
║                                                          ║
║     Hệ thống Multi-Agent AI giúp người trì hoãn          ║
║     chuyển đổi mục tiêu thành hành động siêu nhỏ         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize ATP
    atp = AtomicTaskPlanner(
        use_mock_search=False,  # Set to True for testing without Tavily API
        model="gemini-2.5-flash-lite"  # Using Gemini 2.5 Flash Lite
    )
    
    # Run interactive mode
    try:
        final_plan = atp.run_interactive_mode()
        print("\n✅ HOÀN THÀNH!")
    except KeyboardInterrupt:
        print("\n\n⚠️  Đã hủy bởi người dùng.")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()