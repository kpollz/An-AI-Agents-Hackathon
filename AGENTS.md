# AGENTS.md - AI Coding Agent Guide

> This file contains essential information for AI coding agents working on the Atomic Task Planner (ATP) project.
> Language: English (primary), Vietnamese (for user-facing content)

---

## Project Overview

**Atomic Task Planner (ATP) v2.0** is a Multi-Agent AI system designed for the "Commit To Change: An AI Agents Hackathon". The system helps procrastinators transform vague goals into ultra-small, scientifically-backed action sequences with biological optimization and user editing capabilities before calendar synchronization.

### Key Features
- **4-Agent Pipeline**: Goal Clarifier → Domain Researcher → Bio-Optimizer → JSON Formatter
- **Atomic Habits Integration**: Applies James Clear's 4 principles (Make it Obvious, Easy, Attractive, Satisfying)
- **Bio-Optimization**: Schedules tasks based on user's chronotype and biological rhythms
- **Web Search**: Research workflows and tips with scientific evidence citations
- **Rest Management**: Pomodoro and Ultradian rhythm-based break scheduling
- **User Edit Flow**: Allows user review and editing before calendar sync
- **Google Calendar Sync**: Synchronizes approved plans to Google Calendar

---

## Technology Stack

### Core Framework
- **Language**: Python 3.9+
- **LLM Framework**: LangChain (>=0.1.0)
- **LLM Provider**: Google Gemini (gemini-2.5-flash-lite or gemini-2.0-flash-exp)
- **Data Validation**: Pydantic v2 (>=2.0.0)

### External APIs
- **Web Search**: Tavily API (tavily-python>=0.3.0)
- **Calendar**: Google Calendar API (google-api-python-client>=2.100.0)

### Key Dependencies
```
langchain>=0.1.0
langchain-google-genai>=0.0.5
langchain-core>=0.1.0
pydantic>=2.0.0
tavily-python>=0.3.0
google-api-python-client>=2.100.0
google-auth-oauthlib>=1.0.0
pytz>=2023.3
python-dotenv>=1.0.0
```

### Optional
- **LangGraph**: Can be integrated for state machine-based agent orchestration
- **OpenAI**: Alternative LLM provider can be configured

---

## Project Structure

```
An-AI-Agents-Hackathon/
├── agents/                    # 4 Main Agent modules
│   ├── __init__.py
│   ├── goal_clarifier.py      # A1: Goal clarification & bio-context collection
│   ├── domain_researcher.py   # A2: Web research for workflows & tips
│   ├── bio_optimizer.py       # A3: Bio-optimization & scheduling
│   └── json_formatter.py      # A4: JSON formatting (pure Python, no LLM)
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── web_search.py          # Tavily web search wrapper + Mock tool
│   └── validators.py          # Validation functions & time utilities
├── schemas/                   # Pydantic schemas for type safety
│   ├── __init__.py
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
│   ├── test_goal_clarifier.py # Test A1
│   ├── test_domain_researcher.py # Test A2
│   ├── test_bio_optimizer.py  # Test A3
│   ├── test_json_formatter.py # Test A4
│   └── test_validators.py     # Test utilities
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
└── .env                       # Actual environment variables (gitignored)
```

---

## Configuration

### Environment Variables (`.env` file)

Create `.env` from `.env.example`:

```env
# Required: Google AI API Key (for Gemini)
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Tavily API Key (for web search)
TAVILY_API_KEY=your_tavily_api_key_here

# Optional: Use mock search for testing without API keys
USE_MOCK_SEARCH=False

# Optional: Gemini model selection
GEMINI_MODEL=gemini-2.0-flash-exp
```

### Getting API Keys

1. **Google AI API Key**:
   - Visit: https://makersuite.google.com/app/apikey
   - Create a new project and copy the API key

2. **Tavily API Key**:
   - Visit: https://tavily.com/
   - Sign up and copy the API key

3. **Google Calendar Credentials** (for calendar sync):
   - Visit: https://console.cloud.google.com/apis/credentials
   - Create OAuth 2.0 Client ID
   - Download JSON and save as `credentials.json` in project root

---

## Build and Run Commands

### Installation
```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Testing
```bash
# Run system tests (validates imports, schemas, validators)
python tests/test_goal_clarifier.py
python tests/test_domain_researcher.py
python tests/test_bio_optimizer.py
python tests/test_json_formatter.py
python tests/test_validators.py
```

### Running the Application
```bash
# Interactive mode (main entry point)
python main.py

# With mock search (no Tavily API needed)
# Set USE_MOCK_SEARCH=True in .env first
python main.py
```

### Calendar Sync
```bash
# Sync approved plan to Google Calendar
python standalone/calendar_sync.py --input output/tomorrow_plan.json

# Test mode (dry run)
python standalone/calendar_sync.py --input output/tomorrow_plan.json --dry-run

# With custom credentials
python standalone/calendar_sync.py --input output/tomorrow_plan.json --credentials path/to/credentials.json
```

---

## Agent Architecture

### Pipeline Flow
```
User Input
    ↓
[A1] Goal Clarifier (Interactive Chat)
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
    ├─ Breaks tasks into atomic chunks
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
    ├─ Creates Google Calendar events
    └─ Sets reminders and color coding
```

### Agent Details

| Agent | File | Input | Output | Tools |
|-------|------|-------|--------|-------|
| A1 | `goal_clarifier.py` | User messages | `GoalClarifierOutput` | LLM Chat |
| A2 | `domain_researcher.py` | Goal + Bio context | `DomainResearcherOutput` | Web Search (Tavily) |
| A3 | `bio_optimizer.py` | Tasks + Tips + Bio profile | `BioOptimizerOutput` | LLM + Web Search |
| A4 | `json_formatter.py` | Optimized schedule | `FinalPlan` | Pure Python |
| Sync | `calendar_sync.py` | JSON file | Calendar events | Google Calendar API |

---

## Code Style Guidelines

### Python Style
- **Formatter**: Follow PEP 8
- **Type Hints**: Use typing module for all function signatures
- **Docstrings**: Google-style docstrings for all public methods
- **Imports**: Group imports: stdlib → third-party → local

### Example:
```python
from typing import Dict, List, Any
from pydantic import BaseModel, Field

class MySchema(BaseModel):
    """Description of the schema.
    
    Attributes:
        field1: Description of field1
        field2: Description of field2
    """
    field1: str = Field(description="Description")
    field2: int = Field(default=0, description="Description")

def my_function(param1: str, param2: int) -> Dict[str, Any]:
    """Short description.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Dictionary containing results
    """
    return {"result": param1}
```

### Language Usage
- **Code comments**: English
- **Docstrings**: English
- **User-facing strings**: Vietnamese (as per existing UI)
- **Log messages**: Mixed (follow existing pattern)

---

## Testing Strategy

### Test Files
- Individual test files in `tests/` directory for each agent

### Test Coverage
1. **Import Tests**: Verify all modules can be imported
2. **Schema Tests**: Validate Pydantic schema creation and serialization
3. **Validator Tests**: Test time format validation and conversion utilities
4. **Environment Tests**: Verify environment variables are loaded

### Running Tests
```bash
python tests/test_goal_clarifier.py
python tests/test_domain_researcher.py
python tests/test_bio_optimizer.py
python tests/test_json_formatter.py
python tests/test_validators.py
```

### Mock Mode
Set `USE_MOCK_SEARCH=True` in `.env` to test without Tavily API:
- Uses `MockWebSearchTool` instead of real web search
- Returns sample data for testing pipeline flow

---

## Key Design Patterns

### 1. Pydantic Schemas
All data structures use Pydantic v2 for validation:
- Located in `schemas/` directory
- Each agent has its own output schema
- Final plan schema for user-editable output

### 2. Agent Pattern
Each agent is a class with:
- `__init__`: Initialize LLM and tools
- Main method: Process input and return structured output
- Private helper methods: `_method_name`

### 3. Web Search Abstraction
- `WebSearchTool`: Real Tavily implementation
- `MockWebSearchTool`: Test implementation
- Both implement same interface for easy swapping

### 4. Rest Period Calculation
- **Pomodoro**: 5 min break after 25-30 min focus
- **Ultradian**: 15-20 min break after 90 min focus
- **Meal avoidance**: No focus work ±30 min from meal times

### 5. Atomic Habits Principles
Applied in `bio_optimizer.py`:
- **Make it obvious**: Clear triggers (time, location)
- **Make it easy**: 2-minute rule for first step
- **Make it attractive**: Temptation bundling
- **Make it satisfying**: Immediate reward

---

## Security Considerations

### API Keys
- Store in `.env` file (never commit to git)
- `.env` is in `.gitignore`
- Use `python-dotenv` to load in development

### Google Calendar OAuth
- `credentials.json`: OAuth client secrets (never commit)
- `token.json`: Auto-generated after first auth (gitignored)
- Scopes limited to: `https://www.googleapis.com/auth/calendar`

### Data Privacy
- User bio-profile stored only in memory during session
- Output JSON saved locally in `output/` directory
- No external data persistence except Google Calendar sync

---

## Common Tasks for AI Agents

### Adding a New Agent
1. Create file in `agents/` directory
2. Define Pydantic schema in `schemas/` directory
3. Implement agent class with standard interface
4. Add to `agents/__init__.py`
5. Integrate into `main.py` pipeline

### Modifying Schema
1. Update Pydantic model in `schemas/`
2. Update agent implementation
3. Update any downstream consumers
4. Run individual test files to validate

### Adding Web Search Queries
Edit `utils/web_search.py`:
- Add query pattern to `search_workflow()` method
- Update docstring with query purpose

### Extending Calendar Sync
Edit `standalone/calendar_sync.py`:
- Modify `_create_schedule_event()` or `_create_rest_event()`
- Update color coding in `_get_color_id()`
- Add new command-line arguments in `main()`

---

## Troubleshooting

### Common Issues

1. **"GOOGLE_API_KEY not found"**
   - Ensure `.env` file exists and contains valid key
   - Run `python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('GOOGLE_API_KEY'))"` to verify

2. **"TAVILY_API_KEY not found"**
   - Set `USE_MOCK_SEARCH=True` in `.env` for testing
   - Or obtain API key from https://tavily.com/

3. **Module import errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`
   - Check Python version (3.9+)

4. **Google Calendar auth fails**
   - Ensure `credentials.json` exists in project root
   - Delete `token.json` to re-authenticate
   - Verify Google Calendar API is enabled in Cloud Console

5. **No events created in Calendar**
   - Check `calendar_ready: true` in JSON output
   - Verify plan file path is correct
   - Use `--dry-run` flag to test without creating events

---

## File References

### Documentation
- `README.md`: User-facing documentation (Vietnamese)
- `DEVELOPMENT_v2.md`: Technical specification
- `DEVELOPMENT_v1.md`: Legacy version reference
- `IMPLEMENTATION_SUMMARY.md`: Implementation checklist

### Core Code
- `main.py`: Application entry point
- `agents/`: Agent implementations
- `schemas/`: Data models
- `utils/`: Shared utilities

### Configuration
- `requirements.txt`: Dependencies
- `.env.example`: Environment template
- `.gitignore`: Git exclusions

---

## Notes for AI Agents

1. **Always validate schema changes** with Pydantic before committing
2. **Test with mock search first** to avoid API rate limits
3. **Preserve Vietnamese UI strings** in user-facing output
4. **Follow existing docstring style** (Google format)
5. **Check for existing utility functions** in `utils/` before writing new ones
6. **Respect editable fields** in JSON output - some fields should not be user-modifiable
7. **Maintain atomic task sizes** - tasks should be 2-25 minutes max
8. **Always include rest periods** - never schedule >90 min continuous focus

---

*Last updated: 2026-02-02*
*Project: Atomic Task Planner (ATP) v2.0*
*Hackathon: Commit To Change - An AI Agents Hackathon*
