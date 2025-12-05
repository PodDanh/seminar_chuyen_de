import streamlit as st
import pandas as pd

from nlp_service import classify_sentiment
from db import init_db, insert_sentiment, get_latest
from db import init_db, insert_sentiment, get_latest, clear_history


# Khởi tạo DB khi app chạy
init_db()

# Cấu hình trang
st.set_page_config(
    page_title="Trợ lý phân loại cảm xúc tiếng Việt",
    layout="centered"
)


def show_colored_result(label: str, score: float):
    label = label.upper()

    if label == "POSITIVE":
        bg = "#d4edda"      # xanh nhạt
        border = "#28a745"  # viền xanh
        text = "#155724"
    elif label == "NEGATIVE":
        bg = "#f8d7da"      # đỏ nhạt
        border = "#dc3545"
        text = "#721c24"
    else:  # NEUTRAL
        bg = "#fff3cd"      # vàng nhạt
        border = "#ffc107"
        text = "#856404"

    st.markdown(
        f"""
        <div style="
            border: 1px solid {border};
            background-color: {bg};
            color: {text};
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            margin-top: 0.75rem;
        ">
            <b>Kết quả:</b> {label} (score = {score:.3f})
        </div>
        """,
        unsafe_allow_html=True
    )


# ================== GIAO DIỆN CHÍNH ==================

st.title("🇻🇳 Trợ lý phân loại cảm xúc tiếng Việt")

st.write(
    """
Ứng dụng phân loại cảm xúc của câu tiếng Việt thành 3 nhãn:
**POSITIVE (tích cực)**, **NEUTRAL (trung tính)**, **NEGATIVE (tiêu cực)**.  
Nhập câu tiếng Việt vào ô bên dưới và nhấn nút để phân loại cảm xúc.
"""
)

# --------- Nhập câu ----------
user_text = st.text_area(
    "Nhập câu tiếng Việt",
    placeholder="Ví dụ: Hôm nay tôi rất vui",
    height=130
)

if st.button("Phân loại cảm xúc"):
    if not user_text.strip():
        st.error("Câu không hợp lệ, thử lại")
    else:
        with st.spinner("Đang phân tích cảm xúc..."):
            try:
                result = classify_sentiment(user_text)

                # Lưu vào SQLite
                insert_sentiment(result)

                # Hộp màu theo nhãn
                show_colored_result(result["sentiment"], result["score"])

                # Thông tin thêm
                st.write("Câu gốc:", result["text"])
                st.caption(f"Thời gian: {result['timestamp']}")
            except ValueError as e:
                st.error(str(e))

#Lịch sử phân loại
st.subheader("Lịch sử phân loại gần đây")
# Nút xoá lịch sử
if st.button("🗑 Xoá toàn bộ lịch sử"):
    clear_history()
    st.warning("Đã xoá toàn bộ lịch sử phân loại.")
rows = get_latest(20)
if not rows:
    st.info("Chưa có bản ghi nào trong lịch sử.")
else:
    df = pd.DataFrame(
        rows,
        columns=["ID", "Câu", "Cảm xúc", "Score", "Thời gian"]
    )
    st.dataframe(df, use_container_width=True)
    



