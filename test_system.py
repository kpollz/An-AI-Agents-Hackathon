"""
Simple test script for ATP system
Run this to verify the system is working correctly
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from schemas.agent1_output import GoalClarifierOutput, UserBioProfile
        print("✅ Agent1 schemas imported")
    except Exception as e:
        print(f"❌ Agent1 schemas import failed: {e}")
        return False
    
    try:
        from schemas.agent2_output import DomainResearcherOutput, Task, ProTip
        print("✅ Agent2 schemas imported")
    except Exception as e:
        print(f"❌ Agent2 schemas import failed: {e}")
        return False
    
    try:
        from schemas.agent3_output import BioOptimizerOutput, ScheduleItem
        print("✅ Agent3 schemas imported")
    except Exception as e:
        print(f"❌ Agent3 schemas import failed: {e}")
        return False
    
    try:
        from schemas.final_plan import FinalPlan
        print("✅ Final plan schema imported")
    except Exception as e:
        print(f"❌ Final plan schema import failed: {e}")
        return False
    
    try:
        from utils.web_search import WebSearchTool, MockWebSearchTool
        print("✅ Web search tool imported")
    except Exception as e:
        print(f"❌ Web search tool import failed: {e}")
        return False
    
    try:
        from utils.validators import validate_plan, validate_user_bio_profile
        print("✅ Validators imported")
    except Exception as e:
        print(f"❌ Validators import failed: {e}")
        return False
    
    try:
        from agents.goal_clarifier import GoalClarifierAgent
        from agents.domain_researcher import DomainResearcherAgent
        from agents.bio_optimizer import BioOptimizerAgent
        from agents.json_formatter import JSONFormatterAgent
        print("✅ All agents imported")
    except Exception as e:
        print(f"❌ Agents import failed: {e}")
        return False
    
    print("\n✅ All imports successful!\n")
    return True


def test_environment():
    """Test environment variables"""
    print("🔍 Testing environment variables...")
    
    google_key = os.getenv("GOOGLE_API_KEY")
    if google_key:
        print(f"✅ GOOGLE_API_KEY: {'*' * 20}{google_key[-4:]}")
    else:
        print("⚠️  GOOGLE_API_KEY not found (optional for testing)")
    
    tavily_key = os.getenv("TAVILY_API_KEY")
    if tavily_key:
        print(f"✅ TAVILY_API_KEY: {'*' * 20}{tavily_key[-4:]}")
    else:
        print("⚠️  TAVILY_API_KEY not found (will use mock search)")
    
    print()


def test_schemas():
    """Test schema creation"""
    print("🔍 Testing schema creation...")
    
    try:
        from schemas.agent1_output import UserBioProfile, GoalClarifierOutput
        
        bio_profile = UserBioProfile(
            chronotype="intermediate",
            sleep_time="23:00",
            wake_time="07:00",
            meal_times={"breakfast": "07:30", "lunch": "12:00", "dinner": "19:00"},
            peak_hours=["09:00-11:00"],
            slump_hours=[],
            fixed_commitments=[],
            energy_tomorrow="medium",
            physical_constraints=[]
        )
        
        goal_output = GoalClarifierOutput(
            clarified_goal="Test goal",
            user_bio_profile=bio_profile,
            conversation_complete=True
        )
        
        print(f"✅ GoalClarifierOutput created: {goal_output.clarified_goal}")
        
        # Test JSON serialization
        json_str = goal_output.json()
        print(f"✅ JSON serialization successful (length: {len(json_str)} chars)")
        
    except Exception as e:
        print(f"❌ Schema creation failed: {e}")
        return False
    
    print()
    return True


def test_validators():
    """Test validators"""
    print("🔍 Testing validators...")
    
    try:
        from utils.validators import validate_time_format, time_to_minutes, minutes_to_time
        
        # Test time format validation
        assert validate_time_format("08:00") == True
        assert validate_time_format("08:00-09:00") == True
        assert validate_time_format("25:00") == False
        print("✅ Time format validation works")
        
        # Test time conversion
        assert time_to_minutes("08:30") == 510
        assert minutes_to_time(510) == "08:30"
        print("✅ Time conversion works")
        
        # Test plan validation
        test_plan = {
            "editable_schedule": [
                {
                    "task": "Test task",
                    "editable_fields": {"duration": 30, "can_move": True, "can_delete": True, "can_split": False}
                }
            ],
            "rest_periods": [
                {
                    "type": "mandatory_break",
                    "can_remove": False,
                    "can_extend": True,
                    "duration_minutes": 5
                }
            ]
        }
        
        result = validate_plan(test_plan)
        print(f"✅ Plan validation: {result['valid']}")
        
    except Exception as e:
        print(f"❌ Validators test failed: {e}")
        return False
    
    print()
    return True


def main():
    """Run all tests"""
    print("="*60)
    print("🧪 ATP SYSTEM TEST")
    print("="*60)
    print()
    
    # Test 1: Imports
    if not test_imports():
        print("❌ Import tests failed. Exiting.")
        return
    
    # Test 2: Environment
    test_environment()
    
    # Test 3: Schemas
    if not test_schemas():
        print("❌ Schema tests failed. Exiting.")
        return
    
    # Test 4: Validators
    if not test_validators():
        print("❌ Validator tests failed. Exiting.")
        return
    
    print("="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print()
    print("Next steps:")
    print("1. Configure .env file with your API keys")
    print("2. Run: python main.py")
    print("3. Or test with mock search: set USE_MOCK_SEARCH=True in .env")
    print()


if __name__ == "__main__":
    main()