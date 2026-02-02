"""
Test Agent A1: Goal Clarifier - Interactive Mode
Run: python tests/test_goal_clarifier.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from agents.goal_clarifier import GoalClarifierAgent


def main():
    """Run Goal Clarifier in interactive test mode"""
    print("\n" + "="*60)
    print("🎯 TEST AGENT A1: GOAL CLARIFIER")
    print("="*60)
    print("\nNhập mục tiêu của bạn để test agent...")
    print("Ví dụ: 'Tôi muốn viết báo cáo trước chiều mai'")
    print("-"*60)
    
    agent = GoalClarifierAgent()
    
    # Get initial input
    user_input = input("\n👤 Bạn: ").strip()
    if not user_input:
        print("❌ Không có input. Thoát...")
        return
    
    bio_context = {}
    conversation_complete = False
    
    # Conversation loop
    while not conversation_complete:
        result = agent.chat(user_input, bio_context)
        bio_context = result['collected_info']
        
        print(f"\n🤖 Coach: {result['response']}")
        print(f"   [DEBUG] Collected: {bio_context}")
        
        if result['context_complete']:
            conversation_complete = True
            print("\n✅ Đã thu thập đủ thông tin!")
        else:
            user_input = input("\n👤 Bạn: ").strip()
            if not user_input:
                print("❌ Đã hủy.")
                return
    
    # Generate final output
    print("\n" + "="*60)
    print("📋 GENERATING GOAL SPECIFICATION...")
    print("="*60)
    
    try:
        output = agent.generate_goal_spec("User request", bio_context)
        
        print(f"\n🎯 SMART Goal: {output.clarified_goal}")
        print(f"\n🧬 Bio Profile:")
        print(f"   - Chronotype: {output.user_bio_profile.chronotype}")
        print(f"   - Wake time: {output.user_bio_profile.wake_time}")
        print(f"   - Energy: {output.user_bio_profile.energy_tomorrow}")
        print(f"   - Peak hours: {output.user_bio_profile.peak_hours}")
        
        print("\n" + "="*60)
        print("✅ TEST COMPLETED SUCCESSFULLY")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY not set!")
        print("   Set it with: set GOOGLE_API_KEY=your_key")
        print()
    
    main()
