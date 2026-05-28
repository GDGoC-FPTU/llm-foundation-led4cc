# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> *Khi temperature thấp như 0.0, phản hồi thường ổn định, ngắn gọn và ít thay đổi giữa các lần chạy. Khi tăng lên 1.0 hoặc 1.5, câu trả lời có xu hướng sáng tạo, đa dạng và bất ngờ hơn, nhưng cũng có thể kém nhất quán hoặc thêm chi tiết không cần thiết.*

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> *Mình sẽ đặt khoảng 0.2 đến 0.5, ưu tiên 0.3, vì chatbot hỗ trợ khách hàng cần trả lời nhất quán, chính xác và dễ kiểm soát. Mức này vẫn đủ tự nhiên trong giao tiếp nhưng hạn chế việc mô hình “sáng tạo quá mức” hoặc đưa ra thông tin không ổn định.*

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> *Workload mỗi ngày là:

10.000 users × 3 calls/user × 350 tokens/call = 10.500.000 tokens/ngày

Nếu dùng pricing trong bài lab:

GPT-4o:      input $5.00 / 1M, output $20.00 / 1M
GPT-4o-mini: input $0.15 / 1M, output $0.60 / 1M

thì GPT-4o đắt hơn GPT-4o-mini khoảng:

5.00 / 0.15 = 33.33 lần
20.00 / 0.60 = 33.33 lần

Vậy GPT-4o đắt hơn khoảng 33 lần so với GPT-4o-mini cho workload này.*

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> *GPT-4o xứng đáng khi tác vụ cần độ chính xác và khả năng suy luận cao, ví dụ phân tích tài liệu pháp lý, xử lý yêu cầu phức tạp của khách hàng VIP, hoặc tạo câu trả lời cần hiểu ngữ cảnh sâu. GPT-4o-mini phù hợp hơn cho các tác vụ đơn giản, số lượng lớn và nhạy cảm về chi phí, như chatbot FAQ, phân loại intent, tóm tắt ngắn, hoặc trả lời các câu hỏi hỗ trợ khách hàng phổ biến.*

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> *Streaming quan trọng nhất khi phản hồi dài hoặc người dùng cần cảm giác hệ thống đang “đang trả lời ngay”, ví dụ chatbot tư vấn, trợ lý viết nội dung, giải thích code, tóm tắt tài liệu dài hoặc các tác vụ có độ trễ cao. Nó giúp cải thiện trải nghiệm vì người dùng thấy từng phần câu trả lời xuất hiện ngay thay vì phải chờ toàn bộ kết quả. Ngược lại, non-streaming phù hợp hơn khi phản hồi ngắn, cần xử lý toàn bộ kết quả trước khi hiển thị, hoặc cần parse dữ liệu có cấu trúc như JSON, chấm điểm, phân loại intent, gọi API backend, vì khi đó ta muốn nhận một output hoàn chỉnh và dễ kiểm soát hơn.*


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định
