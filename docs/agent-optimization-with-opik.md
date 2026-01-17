## **Tối ưu hóa Agent với Opik: Sự trỗi dậy của các Agent tự cải thiện**

Buổi workshop này, do Vincent Koc dẫn dắt, khám phá sự chuyển dịch từ kỹ nghệ câu lệnh (prompt engineering) thủ công sang tối ưu hóa tác nhân tự động. Nội dung giới thiệu về **Opik Optimizer SDK** mã nguồn mở của Comet – một công cụ mạnh mẽ để cải thiện hiệu suất của các tác nhân AI một cách có hệ thống mà không cần đến quá trình tinh chỉnh (fine-tuning) phức tạp.

### **Các khái niệm chính: Vượt xa việc tinh chỉnh thủ công**

Buổi học đặt ra thách thức trong việc phát triển tác nhân AI xoay quanh "tam giác bất khả thi" — sự đánh đổi liên tục giữa **Chi phí (Cost), Tốc độ (Speed) và Độ chính xác (Accuracy)**. Ý tưởng cốt lõi là hướng tới một quy trình có phương pháp hơn để cải thiện hiệu suất.

* **Từ Prompt Engineering đến Intent Engineering:** Lĩnh vực này đang tiến hóa từ việc soạn thảo câu lệnh thủ công (thử và sai) và cung cấp ngữ cảnh (như RAG) sang một tương lai của "Kỹ nghệ Ý định" (Intent Engineering) – nơi AI tự giúp mình tối ưu hóa để đạt được kết quả mong muốn.
* **Nhu cầu về một quy trình có hệ thống:** Việc tinh chỉnh câu lệnh thủ công thường kém hiệu quả và dựa trên cảm tính. Một phương pháp tiếp cận tự động, dựa trên dữ liệu là cần thiết để tìm ra các câu lệnh và cấu hình tốt nhất một cách đáng tin cậy.

### **Giới thiệu Opik Optimizer SDK**

Opik là một bộ công cụ phát triển phần mềm (SDK) bằng Python, mã nguồn mở, được thiết kế để tự động hóa việc tối ưu hóa câu lệnh và cấu hình tác nhân. Nó cung cấp một số thuật toán tối ưu hóa nâng cao:

* **MetaPrompt Optimizer:** Sử dụng một LLM để lập luận và tạo ra các ứng viên câu lệnh mới, cải tiến hơn.
* **Hierarchical Reflective Optimizer (HRPO):** Tương tự như phân tích nguyên nhân gốc rễ (root cause analysis), nó phân tích các lỗi sai, xác định các mẫu hình (patterns) và phát triển các chiến lược mục tiêu để khắc phục chúng.
* **Evolutionary Optimizers (GEPA):** Sử dụng các thuật toán di truyền để coi các câu lệnh như một quần thể, cho chúng tiến hóa qua các thế hệ thông qua đột biến và lai ghép để tìm ra câu lệnh "khỏe" nhất (hiệu suất tốt nhất).
* **Few-Shot Bayesian:** Tối ưu hóa việc lựa chọn và sắp xếp các ví dụ mẫu (few-shot examples) từ một bộ dữ liệu để đưa vào câu lệnh.

### **Demo thực hành: [Phát hiện mối nguy hiểm cho xe tự lái](https://towardsdatascience.com/automatic-prompt-optimization-for-multimodal-vision-agents-a-self-driving-car-example/)**

Workshop bao gồm một phần trình diễn thực tế việc sử dụng trình tối ưu hóa HRPO để cải thiện một tác nhân thị giác đa phương thức (multimodal vision agent).

* **Mục tiêu:** Cải thiện độ chính xác của tác nhân trong việc xác định các mối nguy hiểm tiềm ẩn khi lái xe từ hình ảnh camera hành trình (dashcam).
* **Bộ dữ liệu:** Một phần của bộ dữ liệu *Driving Hazard Prediction and Reasoning (DHPR)* đã được sử dụng, bao gồm các hình ảnh và mô tả về mối nguy hiểm do con người chú thích.
* **Chỉ số đánh giá:** **Tỷ lệ khoảng cách Levenshtein (Levenshtein Distance Ratio)** được sử dụng để đo độ tương đồng văn bản giữa mô tả nguy hiểm do AI tạo ra và văn bản chuẩn (ground-truth) từ bộ dữ liệu.
* **Quy trình:**
1. Thiết lập một câu lệnh cơ sở (baseline) đơn giản.
2. Cấu hình trình tối ưu hóa HRPO với mô hình (ví dụ: GPT-5.2 - *giả định trong ngữ cảnh demo*), câu lệnh, bộ dữ liệu và chỉ số đánh giá.
3. Trình tối ưu hóa chạy qua một số lần thử nghiệm (trials) nhất định. Trong mỗi lần, nó đánh giá câu lệnh hiện tại, phân tích các lỗi, suy ngẫm về nguyên nhân gốc rễ và tạo ra các ứng viên câu lệnh mới được cải thiện.
4. Các kết quả được theo dõi trong giao diện Comet UI, cho thấy sự cải thiện rõ rệt về điểm số chỉ số qua các lần thử nghiệm tối ưu hóa.



**Thông điệp then chốt:** Các công cụ tự động như Opik Optimizer cung cấp một phương pháp có cấu trúc và mạnh mẽ để nâng cao hiệu suất tác nhân AI. Bằng cách xác định mục tiêu rõ ràng với bộ dữ liệu và chỉ số cụ thể, các nhà phát triển có thể tận dụng AI để khám phá ra các câu lệnh phức tạp và hiệu quả mà việc lặp đi lặp lại thủ công khó có thể tìm thấy, từ đó dẫn đến các tác nhân mạnh mẽ và đáng tin cậy hơn.
