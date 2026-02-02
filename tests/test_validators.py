"""
Test Utility Functions - Pure Python
Run: python tests/test_validators.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validators import time_to_minutes, minutes_to_time, check_schedule_conflicts


def test_time_conversion():
    """Test time conversion functions"""
    print("\n" + "="*60)
    print("⏰ TEST: Time Conversion")
    print("="*60)
    
    test_cases = [
        ("06:00", 360),
        ("12:30", 750),
        ("23:59", 1439),
        ("00:00", 0),
    ]
    
    all_pass = True
    for time_str, expected_minutes in test_cases:
        result = time_to_minutes(time_str)
        status = "✅" if result == expected_minutes else "❌"
        print(f"   {status} time_to_minutes('{time_str}') = {result} (expected {expected_minutes})")
        if result != expected_minutes:
            all_pass = False
    
    # Test reverse conversion
    print("\n   Reverse conversion:")
    minutes_list = [0, 360, 750, 1439]
    for mins in minutes_list:
        result = minutes_to_time(mins)
        back = time_to_minutes(result)
        status = "✅" if back == mins else "❌"
        print(f"   {status} minutes_to_time({mins}) = '{result}' -> back = {back}")
        if back != mins:
            all_pass = False
    
    return all_pass


def test_schedule_conflicts():
    """Test schedule conflict detection"""
    print("\n" + "="*60)
    print("⚠️  TEST: Schedule Conflicts")
    print("="*60)
    
    # Test case 1: No conflicts
    schedule1 = [
        {"time": "08:00-09:00", "task": "Task 1"},
        {"time": "09:30-10:30", "task": "Task 2"},
        {"time": "11:00-12:00", "task": "Task 3"},
    ]
    conflicts1 = check_schedule_conflicts(schedule1)
    status1 = "✅" if len(conflicts1) == 0 else "❌"
    print(f"   {status1} No conflicts case: {len(conflicts1)} conflicts found")
    
    # Test case 2: Has conflicts
    schedule2 = [
        {"time": "08:00-09:00", "task": "Task 1"},
        {"time": "08:30-09:30", "task": "Task 2 (overlap)"},
        {"time": "10:00-11:00", "task": "Task 3"},
    ]
    conflicts2 = check_schedule_conflicts(schedule2)
    status2 = "✅" if len(conflicts2) == 1 else "❌"
    print(f"   {status2} One conflict case: {len(conflicts2)} conflicts found")
    if conflicts2:
        print(f"        └─ {conflicts2[0]['task1']} vs {conflicts2[0]['task2']}")
    
    # Test case 3: Adjacent (no conflict)
    schedule3 = [
        {"time": "08:00-09:00", "task": "Task 1"},
        {"time": "09:00-10:00", "task": "Task 2 (adjacent)"},
    ]
    conflicts3 = check_schedule_conflicts(schedule3)
    status3 = "✅" if len(conflicts3) == 0 else "❌"
    print(f"   {status3} Adjacent times: {len(conflicts3)} conflicts found")
    
    return len(conflicts1) == 0 and len(conflicts2) == 1 and len(conflicts3) == 0


def main():
    """Run all utility tests"""
    print("\n" + "="*70)
    print("🔧 TEST UTILITIES: Validators")
    print("="*70)
    
    results = []
    
    results.append(("Time Conversion", test_time_conversion()))
    results.append(("Schedule Conflicts", test_schedule_conflicts()))
    
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {status}: {name}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + "="*70)
    if all_passed:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*70)


if __name__ == "__main__":
    main()
