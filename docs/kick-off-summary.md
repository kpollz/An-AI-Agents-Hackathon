# BÁO CÁO TÓM TẮT BUỔI KICK-OFF: COMMIT TO CHANGE AI AGENT HACKATHON

## 1. Mở đầu & Mục tiêu cuộc thi (00:00 - 04:00)

* **Đơn vị tổ chức:** Encode Club giới thiệu về sự hợp tác với các đối tác để tổ chức Hackathon.
* **Tầm nhìn:** Tận dụng làn sóng AI Agent để giải quyết một bài toán thực tế: **Giúp con người thực hiện các cam kết năm mới (New Year's Resolutions)**. Thay vì chỉ là các ứng dụng tĩnh, cuộc thi hướng tới các "Agent" có khả năng chủ động tương tác và hỗ trợ người dùng.

## 2. Thông tin vận hành Hackathon (04:00 - 12:30)

* **Thời gian:** Kéo dài 4 tuần trực tuyến (kết thúc vào đầu tháng 2/2026).
* **5 Hạng mục dự thi (Tracks):** Mỗi hạng mục thắng cuộc nhận **5.000 USD**.
1. **Productivity:** Công cụ làm việc, quản lý thời gian.
2. **Personal Growth:** Học tập, phát triển bản thân.
3. **Social Impact:** Hoạt động cộng đồng, môi trường.
4. **Health & Fitness:** Sức khỏe thể chất/tâm thần.
5. **Financial Wellness:** Quản lý tài chính cá nhân.


* **Giải thưởng đặc biệt:** **5.000 USD** dành riêng cho dự án ứng dụng **Opik** hiệu quả nhất.

## 3. Quy trình nộp bài & Tiêu chí (12:35 - 22:00)

* **Yêu cầu nộp bài:**
* **Video Pitch & Demo (2-5 phút):** Đây là yếu tố quan trọng nhất để thuyết phục giám khảo.
* **GitHub Repository:** Mã nguồn phải được công khai.
* **Mô tả dự án:** Giải thích rõ vấn đề đang giải quyết và cách AI Agent thực hiện điều đó.


* **Mốc thời gian:** Lưu ý hạn chót nộp bài cuối cùng là **08/02/2026**.

## 4. Chuyên đề chuyên sâu: Nền tảng Opik (22:27 - 01:00:00)

*Đây là phần nội dung trọng tâm về kỹ thuật của buổi kick-off.*

### A. Bài toán: Tại sao cần Opik?

Yishai từ đội ngũ Opik giải thích rằng việc xây dựng AI Agent rất khó vì LLM có tính "bất định" (không ổn định). Khi Agent thực hiện nhiều bước (lấy dữ liệu, gọi công cụ, suy luận), nếu có lỗi xảy ra, nhà phát triển thường không biết nó sai ở đâu trong "hộp đen" đó.

### B. Các tính năng cốt lõi của Opik:

* **Tracing (Theo dõi luồng):** * Cho phép ghi lại mọi "vết tích" của Agent. Khi bạn gửi một yêu cầu, Opic sẽ phân rã thành các bước (Spans) như: *Prompt đầu vào -> Kết quả trung gian -> Gọi Tool A -> Kết quả Tool A -> Trả lời cuối cùng*.
* Giúp nhà phát triển kiểm soát được chi phí (tokens) và độ trễ (latency) của từng bước.


* **Evaluation (Đánh giá tự động):**
* Thay vì kiểm tra bằng mắt, Opik cung cấp các bộ chấm điểm tự động (Metrics).
* Sử dụng phương pháp **LLM-as-a-judge**: Dùng một model mạnh để chấm điểm model yếu hơn dựa trên các tiêu chí: *Sự thật (Faithfulness), Tính liên quan (Answer Relevance), và Sự an toàn (Hallucination detection)*.


* **Dataset Management:**
* Bạn có thể lưu trữ các tập dữ liệu thử nghiệm ngay trên Opik để chạy test mỗi khi thay đổi Prompt hoặc Logic của Agent.


* **Prompt Engineering & Optimization:**
* Công cụ này cho phép thử nghiệm nhiều phiên bản Prompt khác nhau và so sánh trực tiếp xem phiên bản nào cho ra kết quả tốt hơn dựa trên số liệu thực tế.



### C. Cách thức tích hợp:

* Cực kỳ đơn giản với SDK cho **Python** và **TypeScript**.
* Chỉ cần thêm Decorator `@track` vào các hàm quan trọng, mọi dữ liệu sẽ tự động được đẩy lên Dashboard của Opik để theo dõi theo thời gian thực.

## 5. Phiên giải đáp thắc mắc - Q&A (01:00:00 - Kết thúc)

* **Về công nghệ:** Không giới hạn mô hình (có thể dùng GPT, Gemini, Claude...). Khuyến khích dùng các Framework như LangChain, CrewAI hoặc AutoGen.
* **Về đội nhóm:** Có thể tham gia cá nhân hoặc nhóm (tối đa 5 người). Khuyến khích tìm đồng đội trên Discord của Encode Club.
* **Về ý tưởng:** Giám khảo đánh giá cao các dự án có tính thực tế cao, giải quyết được "nỗi đau" thực sự của người dùng trong việc duy trì thói quen.
