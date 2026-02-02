"""
Test Agent A3: Bio-Optimizer - with Fake Data
Run: python tests/test_bio_optimizer.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from agents.bio_optimizer import BioOptimizerAgent
from schemas.agent1_output import UserBioProfile
from schemas.agent2_output import Task, TaskEvidence, ProTip, TipEvidence


def create_fake_tasks():
    """Create fake tasks for testing"""
    return [
        Task(
            task_id="task_1",
            name="Khởi động nhẹ",
            description="Đi bộ nhanh và giãn cơ 5 phút",
            estimated_duration="PT5M",
            difficulty="low",
            evidence=TaskEvidence(
                source_url="https://example.com/warmup",
                authority="Fitness Expert",
                summary="Warmup prevents injury"
            )
        ),
        Task(
            task_id="task_2",
            name="Chạy 5km",
            description="Chạy bộ với tốc độ vừa phải",
            estimated_duration="PT30M",
            difficulty="high",
            evidence=TaskEvidence(
                source_url="https://example.com/running",
                authority="Running Coach",
                summary="Consistent running improves cardio"
            )
        ),
        Task(
            task_id="task_3",
            name="Thư giãn",
            description="Đi bộ chậm và thở sâu",
            estimated_duration="PT5M",
            difficulty="low",
            evidence=TaskEvidence(
                source_url="https://example.com/cooldown",
                authority="Health Site",
                summary="Cooldown helps recovery"
            )
        )
    ]


def create_fake_tips():
    """Create fake tips for testing"""
    return [
        ProTip(
            tip_id="tip_1",
            content="Nghe nhạc EDM 120-140 BPM giúp tăng hiệu suất 15%",
            applies_to_task="task_2",
            evidence=TipEvidence(
                source_url="https://example.com/music",
                study_summary="Study shows music improves performance",
                applicability="Good for running"
            )
        ),
        ProTip(
            tip_id="tip_2",
            content="Uống nước 30 phút trước khi chạy",
            applies_to_task="task_1",
            evidence=TipEvidence(
                source_url="https://example.com/hydration",
                study_summary="Hydration affects performance",
                applicability="All exercise"
            )
        )
    ]


def main():
    """Run Bio-Optimizer with fake data"""
    print("\n" + "="*60)
    print("⚡ TEST AGENT A3: BIO-OPTIMIZER")
    print("="*60)
    print("\nUsing FAKE data (no API calls)")
    print("-"*60)
    
    agent = BioOptimizerAgent(use_mock_search=True)
    
    # Create fake data
    tasks = create_fake_tasks()
    tips = create_fake_tips()
    bio_profile = UserBioProfile(
        chronotype="lark",
        sleep_time="23:00",
        wake_time="06:00",
        meal_times={"breakfast": "07:00", "lunch": "12:00", "dinner": "19:00"},
        peak_hours=["06:00-08:00", "17:00-19:00"],
        slump_hours=["13:00-14:00"],
        fixed_commitments=["09:00-17:00: Work"],
        energy_tomorrow="high",
        physical_constraints=[]
    )
    
    print(f"\n🎯 Tasks ({len(tasks)}):")
    for task in tasks:
        print(f"   • {task.name} ({task.difficulty}, {task.estimated_duration})")
    
    print(f"\n💡 Tips ({len(tips)}):")
    for tip in tips:
        print(f"   • {tip.content[:50]}...")
    
    print(f"\n🧬 Bio Profile:")
    print(f"   - Chronotype: {bio_profile.chronotype}")
    print(f"   - Wake: {bio_profile.wake_time}")
    print(f"   - Peak: {bio_profile.peak_hours}")
    
    print("\n⚡ Optimizing schedule...")
    print("-"*60)
    
    try:
        result = agent.optimize_schedule(tasks, tips, bio_profile)
        
        print(f"\n📅 Optimized Schedule ({len(result.optimized_schedule)} items):")
        for item in result.optimized_schedule:
            icon = "☕" if item.type == "rest" else "📋"
            print(f"   {icon} {item.scheduled_time} | {item.name}")
            if item.type == "focus":
                print(f"      └─ Principle: {item.atomic_design.principle}")
        
        print(f"\n📊 Bio Insights:")
        print(f"   - Focus time: {result.bio_insights.total_focus_time}")
        print(f"   - Rest time: {result.bio_insights.total_rest_time}")
        print(f"   - Match score: {result.bio_insights.energy_curve_match}")
        if result.bio_insights.warning:
            print(f"   - Warning: {result.bio_insights.warning}")
        
        print("\n" + "="*60)
        print("✅ TEST COMPLETED SUCCESSFULLY")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
