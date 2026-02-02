# Atomic Task Planner (ATP) v2.0 - Project Overview

> **Hackathon**: Commit To Change: An AI Agents Hackathon by Encode Club & Comet  
> **Category**: Productivity & Work Habits  
> **Status**: MVP Complete

---

## What is ATP?

Atomic Task Planner (ATP) is a Multi-Agent AI system that helps procrastinators transform vague goals into ultra-small, scientifically-backed action sequences. It combines behavioral science (Atomic Habits), chronobiology (biological rhythms), and AI to create personalized, actionable plans.

### Key Innovation
Unlike traditional todo apps, ATP doesn't just list tasks—it:
- **Understands your biology** (chronotype, peak hours, energy levels)
- **Researches scientific evidence** for each recommendation
- **Applies Atomic Habits principles** to make actions irresistibly small
- **Optimizes timing** based on your biological clock
- **Requires user approval** before syncing to calendar

---

## Core Features

| Feature | Description |
|---------|-------------|
| **4-Agent Pipeline** | Goal Clarifier → Domain Researcher → Bio-Optimizer → JSON Formatter |
| **Atomic Habits** | Applies James Clear's 4 principles: Make it Obvious, Easy, Attractive, Satisfying |
| **Bio-Optimization** | Schedules tasks based on chronotype (Lark/Owl/Intermediate) |
| **Web Search** | Tavily-powered research for workflows and scientific evidence |
| **Rest Management** | Pomodoro (5min/25min) + Ultradian rhythm (15-20min/90min) breaks |
| **User Edit Flow** | Review and edit plans before calendar sync |
| **Google Calendar Sync** | OAuth-based synchronization with color-coded events |

---

## Quick Start

### Installation

```bash
# Clone repository
cd An-AI-Agents-Hackathon

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Required API Keys

| Key | Purpose | Get From |
|-----|---------|----------|
| `GOOGLE_API_KEY` | Gemini LLM | https://makersuite.google.com/app/apikey |
| `TAVILY_API_KEY` | Web search (optional) | https://tavily.com/ |
| Google OAuth | Calendar sync | https://console.cloud.google.com/apis/credentials |

### Running ATP

```bash
# Interactive mode
python main.py

# Test without API keys (mock search)
# Set USE_MOCK_SEARCH=True in .env
python main.py

# Sync to Google Calendar (after approval)
python standalone/calendar_sync.py --input output/tomorrow_plan.json
```

---

## How It Works

### The 4-Agent Pipeline

```
User Input: "Tomorrow I want to run 5km"
    ↓
[A1] Goal Clarifier (Interactive Chat)
    ├─ Asks 1-2 questions per turn
    ├─ Collects: chronotype, sleep/wake times, meal times, peak hours, constraints
    ├─ Generates SMART goal
    └─ Output: GoalClarifierOutput
        ↓
[A2] Domain Researcher (Web Search)
    ├─ Searches: workflow, tips, timing
    ├─ Generates tasks with evidence citations
    ├─ Generates pro tips with study references
    └─ Output: DomainResearcherOutput
        ↓
[A3] Bio-Optimizer (LLM + Logic)
    ├─ Researches biological timing
    ├─ Applies Atomic Habits principles
    ├─ Breaks tasks into atomic chunks (2-min rule)
    ├─ Calculates rest periods (Pomodoro + Ultradian)
    ├─ Assigns to time slots based on chronotype
    └─ Output: BioOptimizerOutput
        ↓
[A4] JSON Formatter (Pure Python)
    ├─ Converts to editable format
    ├─ Generates markdown summary
    ├─ Saves to output/tomorrow_plan.json
    └─ Output: FinalPlan
        ↓
User Review & Edit
    ↓
[Calendar Sync] (Standalone Tool)
    ├─ Loads approved plan
    ├─ Creates Google Calendar events with reminders
    └─ Color-coded: Green (easy), Yellow (short), Turquoise (medium), Red (deep work)
```

### Example Output

```json
{
  "metadata": {
    "goal": "Run 5km tomorrow morning",
    "version": "1.0"
  },
  "editable_schedule": [
    {
      "id": "atomic_1",
      "time": "06:00-06:02",
      "task": "Place running shoes and water by the door",
      "evidence": "Timing: Peak cortisol moment | Principle: 2-minute rule | Source: jamesclear.com",
      "tips": ["Listen to 'Eye of the Tiger' for motivation"],
      "editable_fields": {
        "time": "06:00-06:02",
        "duration": 2,
        "can_move": true,
        "can_delete": false,
        "can_split": false
      }
    }
  ],
  "rest_periods": [
    {
      "time": "06:02-06:07",
      "type": "mandatory_break",
      "rationale": "Pomodoro short break for cognitive recovery"
    }
  ],
  "calendar_ready": false
}
```

---

## Project Structure

```
An-AI-Agents-Hackathon/
├── agents/                    # 4 Main Agent modules
│   ├── goal_clarifier.py      # A1: Goal clarification & bio-context collection
│   ├── domain_researcher.py   # A2: Web research for workflows & tips
│   ├── bio_optimizer.py       # A3: Bio-optimization & scheduling
│   └── json_formatter.py      # A4: JSON formatting (pure Python, no LLM)
├── utils/                     # Utility modules
│   ├── web_search.py          # Tavily web search wrapper + Mock tool
│   └── validators.py          # Validation functions & time utilities
├── schemas/                   # Pydantic schemas for type safety
│   ├── agent1_output.py       # GoalClarifierOutput, UserBioProfile
│   ├── agent2_output.py       # DomainResearcherOutput, Task, ProTip
│   ├── agent3_output.py       # BioOptimizerOutput, ScheduleItem, RestPeriod
│   └── final_plan.py          # FinalPlan, EditableScheduleItem
├── standalone/                # Standalone tools
│   └── calendar_sync.py       # Google Calendar sync tool (OAuth)
├── output/                    # Generated plans (created at runtime)
│   └── tomorrow_plan.json
├── main.py                    # Main orchestrator (entry point)
├── tests/                     # Individual agent tests
│   ├── test_goal_clarifier.py
│   ├── test_domain_researcher.py
│   ├── test_bio_optimizer.py
│   ├── test_json_formatter.py
│   └── test_validators.py
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── docs/
│   ├── PROJECT_OVERVIEW.md    # This file
│   └── TECHNICAL_SPEC.md      # Detailed technical documentation
└── README.md                  # Vietnamese user documentation
```

---

## Technology Stack

### Core Framework
- **Language**: Python 3.9+
- **LLM Framework**: LangChain (>=0.1.0)
- **LLM Provider**: Google Gemini (gemini-2.5-flash-lite)
- **Data Validation**: Pydantic v2 (>=2.0.0)

### External APIs
- **Web Search**: Tavily API
- **Calendar**: Google Calendar API

### Key Dependencies
```
langchain>=0.1.0
langchain-google-genai>=0.0.5
pydantic>=2.0.0
tavily-python>=0.3.0
google-api-python-client>=2.100.0
python-dotenv>=1.0.0
```

---

## Atomic Habits Integration

ATP applies James Clear's 4 laws of behavior change:

### 1. Make It Obvious
- Clear triggers (time, location, preceding action)
- Visual cues and environment design

### 2. Make It Easy
- **2-Minute Rule**: First task must be completable in ≤2 minutes
- Friction reduction (prepare materials in advance)

### 3. Make It Attractive
- Temptation bundling (pair with enjoyable activities)
- Rewards and positive reinforcement

### 4. Make It Satisfying
- Immediate rewards in task descriptions
- Progress tracking and completion feedback

---

## Chronobiology Optimization

### Chronotypes Supported
| Type | Characteristics | Optimal Deep Work Time |
|------|----------------|----------------------|
| **Lark** | Early riser, peak energy in morning | 06:00-10:00 |
| **Owl** | Night person, peak energy in evening | 18:00-22:00 |
| **Intermediate** | Balanced energy throughout day | 09:00-12:00, 14:00-17:00 |

### Smart Scheduling Rules
- High-difficulty tasks → Peak hours
- Low-difficulty tasks → Slump hours or gaps
- No focus work ±30 min from meal times (blood flow to digestion)
- Mandatory rest after 90 min continuous focus (ultradian rhythm)
- 5 min break after 25-30 min focus (Pomodoro)

---

## Development Status

### ✅ Completed
- [x] 4-Agent Pipeline (A1-A4)
- [x] Pydantic Schemas for all outputs
- [x] Web Search Integration (Tavily + Mock)
- [x] Bio-optimization with chronotypes
- [x] Atomic Habits principles
- [x] Rest period calculation
- [x] User Edit Flow
- [x] Google Calendar Sync
- [x] Comprehensive documentation
- [x] Test script

### ⏳ Future Enhancements
- [ ] Opik integration for observability
- [ ] Frontend UI
- [ ] Database persistence
- [ ] Multi-day planning
- [ ] User history and learning

---

## Testing

```bash
# Run system tests
# Test individual agents
python tests/test_goal_clarifier.py
python tests/test_domain_researcher.py
python tests/test_bio_optimizer.py
python tests/test_json_formatter.py
python tests/test_validators.py

# Test with mock search
# Set USE_MOCK_SEARCH=True in .env
python main.py
```

---

## License

Created for "Commit To Change: An AI Agents Hackathon" by Encode Club & Comet.

---

**Built with ❤️ using AI Agents, Behavioral Science, and Chronobiology**
