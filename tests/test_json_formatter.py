"""
Test Agent A4: JSON Formatter - Pure Python
Run: python tests/test_json_formatter.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.json_formatter import JSONFormatterAgent
from schemas.agent3_output import (
    BioOptimizerOutput, ScheduleItem, BioInsights,
    RationaleTiming, AtomicDesign, RestPeriod
)
from schemas.agent1_output import UserBioProfile


def create_fake_schedule():
    """Create fake schedule for testing"""
    return [
        ScheduleItem(
            task_id="atomic_1",
            original_task_ref="task_1",
            name="Để sẵn giày chạy",
            description="Chuẩn bị giày và nước uống",
            scheduled_time="06:00-06:02",
            rationale_timing=RationaleTiming(
                why_this_time="Peak cortisol moment",
                evidence_url="https://example.com",
                chronotype_match="lark"
            ),
            atomic_design=AtomicDesign(
                principle="2-minute rule",
                trigger="Sau khi thức dậy",
                friction_reduction="Để sẵn tối hôm trước"
            ),
            attached_tips=["tip_1"],
            duration_minutes=2,
            type="focus"
        ),
        RestPeriod(
            task_id="rest_1",
            scheduled_time="06:02-06:07",
            duration_minutes=5,
            rationale_timing=RationaleTiming(
                why_this_time="Pomodoro break",
                evidence_url="https://example.com/pomodoro",
                chronotype_match="all"
            )
        ),
        ScheduleItem(
            task_id="atomic_2",
            original_task_ref="task_2",
            name="Khởi động nhẹ",
            description="Đi bộ và giãn cơ",
            scheduled_time="06:07-06:12",
            rationale_timing=RationaleTiming(
                why_this_time="Preparation for run",
                evidence_url="https://example.com",
                chronotype_match="lark"
            ),
            atomic_design=AtomicDesign(
                principle="make it obvious",
                trigger="Sau khi uống nước",
                friction_reduction="Có sẵn playlist"
            ),
            attached_tips=["tip_2"],
            duration_minutes=5,
            type="focus"
        )
    ]


def create_fake_bio_insights():
    """Create fake bio insights"""
    return BioInsights(
        total_focus_time="12 minutes",
        total_rest_time="5 minutes",
        energy_curve_match="85%",
        warning=""
    )


def main():
    """Run JSON Formatter test"""
    print("\n" + "="*60)
    print("📄 TEST AGENT A4: JSON FORMATTER")
    print("="*60)
    print("\nPure Python - No LLM needed")
    print("-"*60)
    
    agent = JSONFormatterAgent()
    
    # Create fake data
    optimized_schedule = create_fake_schedule()
    bio_insights = create_fake_bio_insights()
    goal = "Chạy 5km vào buổi sáng"
    bio_profile = UserBioProfile(
        chronotype="lark",
        sleep_time="23:00",
        wake_time="06:00",
        meal_times={"breakfast": "07:00", "lunch": "12:00", "dinner": "19:00"},
        peak_hours=["06:00-08:00"],
        slump_hours=[],
        fixed_commitments=[],
        energy_tomorrow="high",
        physical_constraints=[]
    )
    
    print(f"\n🎯 Goal: {goal}")
    print(f"🧬 Schedule items: {len(optimized_schedule)}")
    print(f"⚡ Bio insights: {bio_insights.total_focus_time} focus, {bio_insights.total_rest_time} rest")
    
    print("\n📄 Formatting final plan...")
    print("-"*60)
    
    try:
        # Format final plan
        final_plan = agent.format_final_plan(
            optimized_schedule=optimized_schedule,
            bio_insights=bio_insights,
            goal=goal,
            bio_profile=bio_profile
        )
        
        print(f"\n✅ Final Plan Created:")
        print(f"   - Metadata: {final_plan.metadata.goal}")
        print(f"   - Created at: {final_plan.metadata.created_at}")
        print(f"   - Schedule items: {len(final_plan.editable_schedule)}")
        print(f"   - Rest periods: {len(final_plan.rest_periods)}")
        print(f"   - Calendar ready: {final_plan.calendar_ready}")
        
        # Generate markdown summary
        print("\n📝 Markdown Summary:")
        print("-"*60)
        summary = agent.generate_summary_markdown(final_plan)
        print(summary[:500] + "...")
        
        # Save to file (optional)
        output_path = "output/test_plan.json"
        saved_path = agent.save_to_file(final_plan, output_path)
        print(f"\n💾 Saved to: {saved_path}")
        
        print("\n" + "="*60)
        print("✅ TEST COMPLETED SUCCESSFULLY")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
