# 🎯 Atomic Task Planner (ATP) v2.0

Hệ thống Multi-Agent AI giúp người dùng trì hoãn chuyển đổi mục tiêu mơ hồ thành chuỗi hành động siêu nhỏ có dẫn chứng khoa học, tối ưu sinh học, và cho phép chỉnh sửa trước khi đồng bộ lịch.

## 📋 Tính năng chính

- ✅ **4 Agent Pipeline**: Goal Clarifier → Domain Researcher → Bio-Optimizer → JSON Formatter
- ✅ **Atomic Habits**: Áp dụng 4 nguyên lý từ James Clear
- ✅ **Bio-Optimization**: Tối ưu lịch trình dựa trên chronotype và sinh học
- ✅ **Web Search**: Research workflow và tips có dẫn chứng khoa học
- ✅ **Rest Management**: Pomodoro và Ultradian rhythm
- ✅ **User Edit Flow**: Cho phép user review và chỉnh sửa trước khi sync
- ✅ **Google Calendar Sync**: Đồng bộ kế hoạch vào Google Calendar
- ✅ **Gemini 2.5 Flash Lite**: Sử dụng model mới nhất của Google

## 🏗️ Cấu trúc dự án

```
An-AI-Agents-Hackathon/
├── agents/                    # Agent modules
│   ├── __init__.py
│   ├── goal_clarifier.py      # Agent A1: Thu thập thông tin
│   ├── domain_researcher.py   # Agent A2: Research workflow + tips
│   ├── bio_optimizer.py       # Agent A3: Tối ưu sinh học
│   └── json_formatter.py      # Agent A4: Format JSON
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── web_search.py           # Tavily web search wrapper
│   └── validators.py           # Validation functions
├── schemas/                   # Pydantic schemas
│   ├── __init__.py
│   ├── agent1_output.py       # A1 output schema
│   ├── agent2_output.py       # A2 output schema
│   ├── agent3_output.py       # A3 output schema
│   └── final_plan.py          # Final plan schema
├── standalone/                # Standalone tools
│   └── calendar_sync.py       # Google Calendar sync tool
├── output/                    # Generated files
│   └── tomorrow_plan.json     # Generated plan
├── main.py                   # Main orchestrator
├── requirements.txt            # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🚀 Cài đặt

### 1. Clone repository

```bash
cd D:\linhtinh\An-AI-Agents-Hackathon
```

### 2. Tạo virtual environment (khuyến nghị)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình environment variables

Sao chép `.env.example` thành `.env` và điền API keys:

```bash
cp .env.example .env
```

Chỉnh sửa `.env`:

```env
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
USE_MOCK_SEARCH=False
GEMINI_MODEL=gemini-2.0-flash-exp
```

#### Lấy API Keys:

1. **Google AI API Key**:
   - Truy cập: https://makersuite.google.com/app/apikey
   - Tạo project mới và copy API key

2. **Tavily API Key**:
   - Truy cập: https://tavily.com/
   - Đăng ký và copy API key

3. **Google Calendar Credentials** (cho calendar sync):
   - Truy cập: https://console.cloud.google.com/apis/credentials
   - Tạo OAuth 2.0 Client ID
   - Download JSON file và đặt tên là `credentials.json`

## 📖 Cách sử dụng

### Chế độ tương tác (Interactive Mode)

Chạy ATP và tương tác với AI Coach:

```bash
python main.py
```

**Quy trình**:

1. **Agent A1 - Goal Clarifier**:
   - AI Coach sẽ hỏi về mục tiêu của bạn
   - Thu thập thông tin sinh học (chronotype, peak hours, v.v.)
   - Hỏi cho đến khi đủ thông tin

2. **Agent A2 - Domain Researcher**:
   - Tìm kiếm workflow chuẩn cho hoạt động của bạn
   - Research tips có dẫn chứng khoa học
   - Tạo danh sách tasks với evidence

3. **Agent A3 - Bio-Optimizer**:
   - Áp dụng Atomic Habits để chia nhỏ tasks
   - Tối ưu thời gian dựa trên chronotype
   - Tính toán rest periods (Pomodoro + Ultradian)
   - Gán tasks vào các khung giờ phù hợp

4. **Agent A4 - JSON Formatter**:
   - Tạo file `output/tomorrow_plan.json`
   - Format để user có thể chỉnh sửa
   - Tạo summary markdown

### Review và Chỉnh sửa

Mở file `output/tomorrow_plan.json` để review:

```json
{
  "metadata": {
    "goal": "Chạy 5km vào ngày mai",
    "version": "1.0"
  },
  "editable_schedule": [
    {
      "id": "atomic_1",
      "time": "06:00-06:02",
      "task": "Để sẵn giày và nước",
      "evidence": "Timing: Peak cortisol moment...",
      "tips": ["Nghe playlist 'Running Motivation'"],
      "editable_fields": {
        "time": "06:00-06:02",
        "duration": 2,
        "can_move": true,
        "can_delete": false,
        "can_split": false
      }
    }
  ],
  "rest_periods": [...],
  "calendar_ready": false
}
```

**Chỉnh sửa**:
- Thay đổi thời gian (`time`)
- Xóa task không cần (`can_delete: true`)
- Kéo dài thời gian (`duration`)

### Đồng bộ Google Calendar

Sau khi đã hài lòng với kế hoạch, sync vào Calendar:

```bash
python standalone/calendar_sync.py --input output/tomorrow_plan.json --user your_name
```

**Options**:
- `--input`: Bắt buộc - path đến file JSON đã approve
- `--user`: User ID cho tracking (optional)
- `--credentials`: Path đến file credentials Google (default: credentials.json)
- `--dry-run`: Test mode, không tạo events thật

## 🧪 Testing

Test từng agent riêng lẻ:

```bash
# Test Agent A1 - Goal Clarifier (Interactive)
python tests/test_goal_clarifier.py

# Test Agent A2 - Domain Researcher (Mock search)
python tests/test_domain_researcher.py

# Test Agent A3 - Bio-Optimizer (Fake data)
python tests/test_bio_optimizer.py

# Test Agent A4 - JSON Formatter (Pure Python)
python tests/test_json_formatter.py

# Test Utilities
python tests/test_validators.py
```

Chạy với mock search (không cần Tavily API):

```bash
# Chỉnh sửa .env: USE_MOCK_SEARCH=True
# Hoặc chỉnh trong code:
atp = AtomicTaskPlanner(use_mock_search=True, model="gemini-2.0-flash-exp")
```

## 📊 Agent Pipeline Details

### Agent A1: Goal Clarifier
- **Vai trò**: Thu thập thông tin sinh học và làm rõ mục tiêu
- **Tools**: LLM conversation
- **Output**: SMART goal + UserBioProfile

### Agent A2: Domain Researcher
- **Vai trò**: Research workflow, tips, evidence
- **Tools**: Tavily Web Search
- **Output**: Tasks với evidence, Pro tips, Warnings

### Agent A3: Bio-Optimizer
- **Vai trò**: Áp dụng Atomic Habits + Tối ưu sinh học
- **Tools**: LLM + Web Search (timing research)
- **Output**: Optimized schedule với rest periods

### Agent A4: JSON Formatter
- **Vai trò**: Format để user chỉnh sửa
- **Tools**: Pure Python (no LLM)
- **Output**: Editable JSON file

### Standalone: Calendar Sync
- **Vai trò**: Đồng bộ vào Google Calendar
- **Tools**: Google Calendar API
- **Input**: Approved JSON file

## 🎨 Tính năng nổi bật

### 1. Atomic Habits Integration
- **Make it Obvious**: Clear triggers (time, location, action)
- **Make it Easy**: 2-minute rule cho task đầu tiên
- **Make it Attractive**: Temptation bundling
- **Make it Satisfying**: Immediate reward trong description

### 2. Chronobiology Optimization
- Phân tích chronotype (lark/owl/intermediate)
- Gán high-difficulty tasks vào peak hours
- Tránh schedule focus work gần meal times
- Research timing từ nguồn khoa học

### 3. Smart Rest Management
- Pomodoro: 5p break sau 25-30p focus
- Ultradian: 15-20p break sau 90p focus
- Mandatory rest periods (không thể xóa)
- Rest periods hiển thị transparent trong Calendar

### 4. User Control
- Review trước khi sync
- Chỉnh sửa time, duration, xóa task
- Editable fields được đánh dấu rõ ràng
- Dry-run mode cho testing

## 🐛 Troubleshooting

### Lỗi: "GOOGLE_API_KEY not found"
**Giải pháp**: Đảm bảo file `.env` tồn tại và chứa `GOOGLE_API_KEY`

### Lỗi: "TAVILY_API_KEY not found"
**Giải pháp**: Set `USE_MOCK_SEARCH=True` trong `.env` hoặc lấy Tavily API key

### Lỗi: "Credentials file not found" (Calendar sync)
**Giải pháp**: Download OAuth credentials từ Google Cloud Console và đặt tên `credentials.json`

### Lỗi: No events created
**Giải pháp**: Kiểm tra:
1. `calendar_ready: true` trong JSON
2. Có quyền truy cập Google Calendar
3. Chạy với `--dry-run` để test

## 📝 Ví dụ Output

### Markdown Summary

```markdown
# 🎯 Kế hoạch ngày mai: Chạy 5km vào ngày mai

**Context của bạn**: Optimized for lark chronotype. High focus time detected.

**Chronotype**: lark
**Tổng thời gian**: 45 minutes

## 📋 Chuỗi hành động (Atomic Tasks):

**06:00-06:02** | Để sẵn giày và nước
- *Trigger*: Được tối ưu theo thời gian sinh học
- *Lý do*: Timing: Peak cortisol moment | Principle: 2-minute rule | Trigger: Right after morning coffee
- *Tips*: ["tip_1", "tip_2"]

**06:05-06:10** | Khởi động nhẹ
- *Trigger*: Được tối ưu theo thời gian sinh học
- *Lý do*: Timing: Post-activation window | Principle: make it easy
...
```

## 🚀 Development Status

- ✅ Agent A1 (Goal Clarifier)
- ✅ Agent A2 (Domain Researcher)
- ✅ Agent A3 (Bio-Optimizer)
- ✅ Agent A4 (JSON Formatter)
- ✅ Calendar Sync Tool
- ✅ Pydantic Schemas
- ✅ Web Search Integration
- ⏳ Frontend UI (optional for future)
- ⏳ Opik Integration (for hackathon tracking)

## 📄 License

Dự án được tạo cho mục đích thi hackathon "Commit To Change: An AI Agents Hackathon".

## 👥 Hackathon Details

- **Tên cuộc thi**: Commit To Change: An AI Agents Hackathon
- **Hạng mục tham gia**: Productivity & Work Habits
- **Tech Stack**: LangChain + Gemini 2.5 Flash Lite + Google Calendar
- **Observability**: Opik (to be integrated)

## 🤝 Contributing

Dự án đang phát triển cho hackathon. Feedback và suggestions được hoan nghênh!

## 📞 Liên hệ

Để cập nhật và thông tin, xem:
- DEVELOPMENT_v2.md (Tài liệu kỹ thuật chi tiết)
- DEVELOPMENT_v1.md (Phiên bản cũ)
- docs/ (Tài liệu bổ sung)

---

**Built with ❤️ using AI Agents, Behavioral Science, and Chronobiology**