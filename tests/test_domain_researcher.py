"""
Test Agent A2: Domain Researcher - with Mock Search
Run: python tests/test_domain_researcher.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from agents.domain_researcher import DomainResearcherAgent


def main():
    """Run Domain Researcher with mock search"""
    print("\n" + "="*60)
    print("🔍 TEST AGENT A2: DOMAIN RESEARCHER")
    print("="*60)
    print("\nUsing MOCK search (no API key needed)")
    print("-"*60)
    
    # Use mock search for testing
    agent = DomainResearcherAgent(use_mock_search=True)
    
    # Test goal
    goal = "Chạy 5km vào ngày mai"
    bio_context = {
        "chronotype": "intermediate",
        "wake_time": "06:00",
        "energy_tomorrow": "high"
    }
    
    print(f"\n🎯 Goal: {goal}")
    print(f"🧬 Bio Context: {bio_context}")
    print("\n🔍 Researching...")
    print("-"*60)
    
    try:
        result = agent.research_domain(goal, bio_context)
        
        print(f"\n📊 Domain: {result.domain}")
        print(f"\n📋 Tasks ({len(result.tasks)}):")
        for task in result.tasks:
            print(f"   • {task.name} ({task.difficulty})")
            print(f"     └─ {task.description[:80]}...")
        
        print(f"\n💡 Pro Tips ({len(result.pro_tips)}):")
        for tip in result.pro_tips[:3]:
            print(f"   • {tip.content[:80]}...")
        
        if result.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in result.warnings:
                print(f"   • {warning}")
        
        print("\n" + "="*60)
        print("✅ TEST COMPLETED SUCCESSFULLY")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
