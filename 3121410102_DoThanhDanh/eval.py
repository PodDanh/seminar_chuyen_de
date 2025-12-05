from nlp_service import classify_sentiment

# Bộ test case
TEST_CASES = [
    ("Hôm nay tôi rất vui", "POSITIVE"),
    ("Món ăn này dở quá", "NEGATIVE"),
    ("Thời tiết bình thường", "NEUTRAL"),
    ("Rất vui hôm nay", "POSITIVE"),
    ("Công việc ổn định", "NEUTRAL"),
    ("Phim này hay lắm", "POSITIVE"),
    ("Tôi buồn vì thất bại", "NEGATIVE"),
    ("Ngày mai đi học", "NEUTRAL"),
    ("Cảm ơn bạn rất nhiều", "POSITIVE"),
    ("Mệt mỏi quá hôm nay", "NEGATIVE"),
]


def main():
    correct = 0
    total = len(TEST_CASES)

    print("=== ĐÁNH GIÁ MÔ HÌNH TRÊN 10 TEST CASE ===\n")

    for idx, (text, expected) in enumerate(TEST_CASES, start=1):
        pred = classify_sentiment(text)
        is_correct = pred["sentiment"] == expected
        if is_correct:
            correct += 1

        print(f"Case {idx}: {text}")
        print(f"  Mong đợi : {expected}")
        print(f"  Dự đoán  : {pred['sentiment']} (score={pred['score']:.3f})")
        print(f"  --> {'OK' if is_correct else 'SAI'}\n")

    acc = correct / total
    print(f"Tổng số đúng: {correct}/{total}")
    print(f"Độ chính xác: {acc:.2%}")


if __name__ == "__main__":
    main()
