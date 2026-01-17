## **Giới thiệu về Opik: Khả năng quan sát & Đánh giá cho các AI Agent**

Buổi workshop này là một phần của cuộc thi **"Commit to Change: An AI Agents Hackathon"**, với sự góp mặt của Abby Morgan từ Comet. Cô giới thiệu về **Opik** – một công cụ mạnh mẽ được thiết kế để giúp các nhà phát triển xây dựng, giám sát và cải thiện các hệ thống tác nhân AI (AI agentic systems).

### **Tại sao việc đánh giá AI lại quan trọng?**

Abby Morgan bắt đầu bằng việc giải thích tầm quan trọng của việc đánh giá có hệ thống trong phát triển AI. Nếu không có nó, các nhà phát triển thường chỉ đang "đoán mò".

* **Sẵn sàng cho thực tế (Production Readiness):** Đánh giá giúp biến các "bản demo thú vị" thành các hệ thống ổn định, có thể tự tin triển khai vào thực tế.
* **Quy trình khoa học:** Chuyển đổi việc lặp lại ngẫu nhiên (đoán mò) thành một quy trình khoa học có cấu trúc: **Đo lường → Học hỏi → Cải thiện.**
* **Sự tin cậy và Gỡ lỗi:** Cung cấp công cụ để so sánh các phiên bản khác nhau, gỡ lỗi sai sót và cuối cùng là xây dựng niềm tin của người dùng vào hệ thống AI.

### **Demo trực tiếp Opik: [Tác nhân tạo công thức nấu ăn](https://gist.github.com/vincentkoc/638f11fcb00d0351473be5a8705d4c08)**

Trọng tâm của buổi workshop là phần demo trực tiếp Opik bằng một tác nhân AI đơn giản gồm hai bước: đề xuất công thức nấu ăn và sau đó nghiên cứu cách thực hiện.

#### **Các tính năng chính được giới thiệu:**

* **Khả năng quan sát & Theo dấu (Observability & Tracing):** Opik tự động ghi lại toàn bộ quy trình làm việc của một tác nhân. Bản demo cho thấy cách chia nhỏ một yêu cầu đơn lẻ thành một **Trace** (toàn bộ quy trình từ đầu đến cuối) và nhiều **Spans** (các bước riêng lẻ như lệnh gọi LLM hoặc sử dụng công cụ). Chế độ xem chi tiết này rất cần thiết để gỡ lỗi.
* **Đánh giá trực tuyến (LLM-as-a-Judge):** Abby trình bày cách tạo các quy tắc đánh giá tùy chỉnh trực tiếp trên giao diện Opik. Các quy tắc này sử dụng một LLM (ví dụ: GPT-4) để chấm điểm đầu ra của tác nhân dựa trên các tiêu chí chủ quan như "Độ ngon", "Độ khó" và "Sự liên quan". Điều này cung cấp phản hồi tự động, thời gian thực cho mỗi lần chạy.
* **Vòng lặp phản hồi từ con người (Human Feedback Loop):** Nền tảng cho phép người thẩm định thủ công chấm điểm. Điều này rất quan trọng để hiệu chỉnh phương pháp "LLM-as-a-Judge" và đảm bảo điểm số tự động khớp với cảm nhận của con người về chất lượng.
* **Tạo bộ dữ liệu để kiểm thử hồi quy (Regression Testing):** Chỉ với vài cú nhấp chuột, các dấu vết (traces) có vấn đề (ví dụ: điểm thấp hoặc có lỗi) có thể được tập hợp thành một bộ dữ liệu. Bộ dữ liệu này sau đó được sử dụng để kiểm tra một cách hệ thống các phiên bản mới của tác nhân, nhằm đảm bảo rằng các bản sửa lỗi không gây ra lỗi mới (hồi quy).

### **Bắt đầu với Opik**

Buổi workshop kết thúc bằng phần hướng dẫn sử dụng sổ tay Opik Quickstart Colab, cho thấy việc tích hợp Opik vào dự án dễ dàng như thế nào:

1. **Cài đặt:** Chỉ cần lệnh đơn giản `pip install opik`.
2. **Cấu hình:** Chạy `opik configure` để thiết lập khóa API và kết nối với tầng đám mây (cloud tier) miễn phí của Comet.
3. **Theo dấu (Tracing):** Cách dễ nhất để bắt đầu là sử dụng decorator `@track` cho bất kỳ hàm Python nào. Đối với các khung phổ biến như OpenAI SDK, LangChain hoặc Google ADK, Opik cung cấp các tích hợp liền mạch chỉ với một dòng mã, tự động thu thập tất cả dữ liệu liên quan mà không cần dùng decorator.

---

**Tổng kết:** Buổi học nhấn mạnh Opik là một công cụ không thể thiếu để vượt xa các bản mẫu (prototype) AI cơ bản, tiến tới xây dựng các ứng dụng tác nhân (agentic applications) đáng tin cậy, chất lượng cao và không ngừng được cải thiện.

