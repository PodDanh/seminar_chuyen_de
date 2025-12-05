# Trợ lý phân loại cảm xúc tiếng Việt  
Ứng dụng phân loại câu tiếng Việt thành 3 nhãn cảm xúc:  
- **POSITIVE (tích cực)**  
- **NEUTRAL (trung tính)**  
- **NEGATIVE (tiêu cực)**  

Ứng dụng sử dụng mô hình **Transformer PhoBERT** thông qua pipeline `sentiment-analysis` của HuggingFace.

---

##  1. Giới thiệu
Đây là ứng dụng đồ án môn học *Seminar chuyên đề*: xây dựng hệ thống phân loại cảm xúc tiếng Việt dạng trợ lý AI, có giao diện Web bằng **Streamlit**, sử dụng mô hình **PhoBERT sentiment finetuned** và lưu lịch sử phân loại bằng **SQLite**.


## 2. Tính năng chính

###  Phân loại cảm xúc tiếng Việt  
- Trả về 1 trong 3 nhãn: POSITIVE / NEUTRAL / NEGATIVE  
- Kèm theo **score** tin cậy.

###  Tiền xử lý tiếng Việt  
- Chuẩn hóa văn bản  
- Tách từ bằng **underthesea** (nếu có)  
- Giới hạn **≤ 50 ký tự**  
- Từ điển chỉnh lỗi gõ đơn giản  

###  Kiểm tra câu hợp lệ  
- Câu phải ≥ 5 ký tự  
- Phải chứa ít nhất 1 nguyên âm tiếng Việt  
- Nếu không → báo: “Câu không hợp lệ, thử lại”

###  Lưu lịch sử phân loại (SQLite)  
- Lưu câu, nhãn, score, timestamp  
- Hiển thị bảng lịch sử  
- **Có nút xoá toàn bộ lịch sử**

###  Giao diện trực quan  
- **Xanh lá → POSITIVE**  
- **Vàng → NEUTRAL**  
- **Đỏ → NEGATIVE**



## 3. Cấu trúc thư mục


ser_doan/
│
├── app.py                # Giao diện Streamlit
├── nlp_service.py        # Xử lý NLP + mô hình Transformer
├── db.py                 # Tạo / lưu / xoá lịch sử SQLite
├── eval.py               # Đánh giá mô hình trên 10 test case
├── sentiments.db         # Tự sinh trong quá trình chạy
├── requirements.txt      # Danh sách thư viện
└── README.md             # File mô tả dự án


##  4. Cài đặt môi trường

###  Tạo môi trường ảo (khuyến nghị)

```
py -3.11 -m venv venv
venv\Scripts\activate
```

> **Không dùng Python 3.14**, nhiều thư viện chưa hỗ trợ.

---

###  Cài thư viện

python -m pip install -r requirements.txt

##  5. Chạy ứng dụng

python -m streamlit run app.py

Mặc định app sẽ mở tại:  
👉 http://localhost:8501



##  6. Chạy eval.py để kiểm tra mô hình

python eval.py
=== ĐÁNH GIÁ MÔ HÌNH TRÊN 10 TEST CASE ===
Độ chính xác: 90%


##  7. Bộ 10 Test Case theo yêu cầu đồ án

| STT | Câu đầu vào | Nhãn mong đợi |
|-----|-------------|----------------|
| 1 | Hôm nay tôi rất vui | POSITIVE |
| 2 | Món ăn này dở quá | NEGATIVE |
| 3 | Thời tiết bình thường | NEUTRAL |
| 4 | Rất vui hôm nay | POSITIVE |
| 5 | Công việc ổn định | NEUTRAL |
| 6 | Phim này hay lắm | POSITIVE |
| 7 | Tôi buồn vì thất bại | NEGATIVE |
| 8 | Ngày mai đi học | NEUTRAL |
| 9 | Cảm ơn bạn rất nhiều | POSITIVE |
|10 | Mệt mỏi quá hôm nay | NEGATIVE |

---

##  8. Công nghệ sử dụng

- **Transformer PhoBERT sentiment** (HuggingFace)
- torch
- transformers
- underthesea
- streamlit
- sqlite3

