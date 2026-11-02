import json
import os
import subprocess

# Paths
hsk1_path = 'hsk1_vocab_data.json'
hanzi_details_path = 'hsk1_hanzi_details.json'

# 20 target words for HSK1 Lesson 12
lesson12_words = [
    {
        "hanzi": "天",
        "pinyin": "tiān",
        "meaning": "trời, ngày",
        "lesson": "12",
        "type": "danh từ",
        "ex_cn": "今天天很冷。",
        "ex_py": "Jīntiān tiān hěn lěng.",
        "ex_vn": "Hôm nay trời rất lạnh."
    },
    {
        "hanzi": "天气",
        "pinyin": "tiānqì",
        "meaning": "thời tiết",
        "lesson": "12",
        "type": "danh từ",
        "ex_cn": "今天天气很热。",
        "ex_py": "Jīntiān tiānqì hěn rè.",
        "ex_vn": "Thời tiết hôm nay rất nóng."
    },
    {
        "hanzi": "了",
        "pinyin": "le",
        "meaning": "rồi (trợ từ ngữ khí)",
        "lesson": "12",
        "type": "trợ từ",
        "ex_cn": "天冷了。",
        "ex_py": "Tiān lěng le.",
        "ex_vn": "Trời lạnh rồi."
    },
    {
        "hanzi": "冷",
        "pinyin": "lěng",
        "meaning": "lạnh",
        "lesson": "12",
        "type": "tính từ",
        "ex_cn": "我觉得很冷。",
        "ex_py": "Wǒ juéde hěn lěng.",
        "ex_vn": "Tôi cảm thấy rất lạnh."
    },
    {
        "hanzi": "热",
        "pinyin": "rè",
        "meaning": "nóng",
        "lesson": "12",
        "type": "tính từ",
        "ex_cn": "今天不太热。",
        "ex_py": "Jīntiān bú tài rè.",
        "ex_vn": "Hôm nay không nóng lắm."
    },
    {
        "hanzi": "觉得",
        "pinyin": "juéde",
        "meaning": "cảm thấy, thấy rằng",
        "lesson": "12",
        "type": "động từ",
        "ex_cn": "你觉得怎么样？",
        "ex_py": "Nǐ juéde zěnmeyàng?",
        "ex_vn": "Bạn thấy thế nào?"
    },
    {
        "hanzi": "下",
        "pinyin": "xià",
        "meaning": "rơi, đổ (mưa, tuyết), xuống",
        "lesson": "12",
        "type": "động từ",
        "ex_cn": "下雨了。",
        "ex_py": "Xià yǔ le.",
        "ex_vn": "Trời mưa rồi."
    },
    {
        "hanzi": "下雨",
        "pinyin": "xià yǔ",
        "meaning": "mưa, trời mưa",
        "lesson": "12",
        "type": "động từ",
        "ex_cn": "明天会下雨。",
        "ex_py": "Míngtiān huì xià yǔ.",
        "ex_vn": "Ngày mai trời sẽ mưa."
    },
    {
        "hanzi": "下雪",
        "pinyin": "xià xuě",
        "meaning": "tuyết rơi",
        "lesson": "12",
        "type": "động từ",
        "ex_cn": "今天下雪吗？",
        "ex_py": "Jīntiān xià xuě ma?",
        "ex_vn": "Hôm nay có tuyết rơi không?"
    },
    {
        "hanzi": "来",
        "pinyin": "lái",
        "meaning": "đến, lại, tới",
        "lesson": "12",
        "type": "động từ",
        "ex_cn": "你来看一下这个。",
        "ex_py": "Nǐ lái kàn yíxià zhè ge.",
        "ex_vn": "Bạn lại xem cái này một chút đi."
    },
    {
        "hanzi": "有点儿",
        "pinyin": "yǒudiǎnr",
        "meaning": "hơi, một chút",
        "lesson": "12",
        "type": "phó từ",
        "ex_cn": "这个有点儿大。",
        "ex_py": "Zhè ge yǒudiǎnr dà.",
        "ex_vn": "Cái này hơi to một chút."
    },
    {
        "hanzi": "生病",
        "pinyin": "shēngbìng",
        "meaning": "bị ốm, bị bệnh",
        "lesson": "12",
        "type": "động từ",
        "ex_cn": "她生病了。",
        "ex_py": "Tā shēngbìng le.",
        "ex_vn": "Cô ấy bị ốm rồi."
    },
    {
        "hanzi": "药",
        "pinyin": "yào",
        "meaning": "thuốc",
        "lesson": "12",
        "type": "danh từ",
        "ex_cn": "我要吃药。",
        "ex_py": "Wǒ yào chī yào.",
        "ex_vn": "Tôi phải uống thuốc."
    },
    {
        "hanzi": "回",
        "pinyin": "huí",
        "meaning": "về, quay về",
        "lesson": "12",
        "type": "động từ",
        "ex_cn": "爸爸回家了吗？",
        "ex_py": "Bàba huí jiā le ma?",
        "ex_vn": "Bố đã về nhà chưa?"
    },
    {
        "hanzi": "喝",
        "pinyin": "hē",
        "meaning": "uống",
        "lesson": "12",
        "type": "động từ",
        "ex_cn": "你想喝茶吗？",
        "ex_py": "Nǐ xiǎng hē chá ma?",
        "ex_vn": "Bạn có muốn uống trà không?"
    },
    {
        "hanzi": "公司",
        "pinyin": "gōngsī",
        "meaning": "công ty",
        "lesson": "12",
        "type": "danh từ",
        "ex_cn": "他来公司了吗？",
        "ex_py": "Tā lái gōngsī le ma?",
        "ex_vn": "Anh ấy đã đến công ty chưa?"
    },
    {
        "hanzi": "看病",
        "pinyin": "kànbìng",
        "meaning": "khám bệnh, đi khám",
        "lesson": "12",
        "type": "động từ",
        "ex_cn": "他去医院看病了。",
        "ex_py": "Tā qù yīyuàn kànbìng le.",
        "ex_vn": "Anh ấy đi bệnh viện khám bệnh rồi."
    },
    {
        "hanzi": "一点儿",
        "pinyin": "yìdiǎnr",
        "meaning": "một chút, một ít",
        "lesson": "12",
        "type": "lượng từ",
        "ex_cn": "你想喝一点儿水吗？",
        "ex_py": "Nǐ xiǎng hē yìdiǎnr shuǐ ma?",
        "ex_vn": "Bạn có muốn uống một chút nước không?"
    },
    {
        "hanzi": "再",
        "pinyin": "zài",
        "meaning": "lại, nữa, sau đó mới",
        "lesson": "12",
        "type": "phó từ",
        "ex_cn": "回家后再喝点儿热水吧。",
        "ex_py": "Huí jiā hòu zài hē diǎnr rè shuǐ ba.",
        "ex_vn": "Về nhà rồi uống thêm chút nước ấm nhé."
    },
    {
        "hanzi": "先",
        "pinyin": "xiān",
        "meaning": "trước, trước tiên",
        "lesson": "12",
        "type": "phó từ",
        "ex_cn": "你先吃饭，再去学校吧。",
        "ex_py": "Nǐ xiān chī fàn, zài qù xuéxiào ba.",
        "ex_vn": "Bạn ăn cơm trước đi, rồi hãy đến trường nhé."
    }
]

# Additional Hanzi details needed for Lesson 12
additional_hanzi_details = {
    "雪": {
        "strokes": 11,
        "radical": "雨",
        "pinyin": "xuě",
        "meaning": "tuyết",
        "mnemonic": "Dưới cơn mưa (vũ 雨) mùa đông, dùng chổi (kệ 彐) quét tuyết trắng đọng trên mặt đất."
    },
    "药": {
        "strokes": 9,
        "radical": "艹",
        "pinyin": "yào",
        "meaning": "thuốc",
        "mnemonic": "Cây cỏ (thảo 艹) đem lại niềm vui (lạc 约/乐), chữa khỏi bệnh tật gọi là thuốc."
    },
    "司": {
        "strokes": 5,
        "radical": "口",
        "pinyin": "sī",
        "meaning": "quản lý, cơ quan (trong 公司)",
        "mnemonic": "Một người đứng chỉ huy và mở miệng (khẩu 口) ban hành mệnh lệnh quản lý công việc."
    },
    "得": {
        "strokes": 11,
        "radical": "彳",
        "pinyin": "dé / de",
        "meaning": "được, thấy (trong 觉得)",
        "mnemonic": "Đi bước ngắn (xích 彳) tìm mặt trời (nhật 日) và đo một thốn (thốn 寸), làm việc cần cù thì sẽ được kết quả."
    }
}

def main():
    print("=== Cập nhật từ vựng HSK1 Bài 12 ===")

    # 1. Update hsk1_hanzi_details.json
    if os.path.exists(hanzi_details_path):
        with open(hanzi_details_path, 'r', encoding='utf-8') as f:
            details_data = json.load(f)
        for char, info in additional_hanzi_details.items():
            if char not in details_data:
                details_data[char] = info
        with open(hanzi_details_path, 'w', encoding='utf-8') as f:
            json.dump(details_data, f, ensure_ascii=False, indent=2)
        print("✅ Đã cập nhật hsk1_hanzi_details.json với các chữ Hán bổ sung.")

    # 2. Update hsk1_vocab_data.json
    with open(hsk1_path, 'r', encoding='utf-8') as f:
        hsk1_data = json.load(f)

    # Filter out existing Lesson 12 words
    filtered_data = [item for item in hsk1_data if str(item.get('lesson')) != '12']

    # Split before lesson 12 and after lesson 12
    before_l12 = [item for item in filtered_data if int(item.get('lesson', 0)) < 12]
    after_l12 = [item for item in filtered_data if int(item.get('lesson', 0)) > 12]

    # Combine: Lessons 1-11, new Lesson 12, then Lessons 13+
    updated_hsk1 = before_l12 + lesson12_words + after_l12

    with open(hsk1_path, 'w', encoding='utf-8') as f:
        json.dump(updated_hsk1, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã lưu {len(updated_hsk1)} từ vựng vào {hsk1_path} (Bài 12: {len(lesson12_words)} từ).")

    # 3. Update all_hanzi.json
    all_hanzi_chars = set()
    for lvl in range(1, 7):
        v_file = f'hsk{lvl}_vocab_data.json'
        if os.path.exists(v_file):
            with open(v_file, 'r', encoding='utf-8') as vf:
                v_data = json.load(vf)
                for item in v_data:
                    for char in item['hanzi']:
                        if '\u4e00' <= char <= '\u9fff':
                            all_hanzi_chars.add(char)

    all_hanzi_list = sorted(list(all_hanzi_chars))
    with open('all_hanzi.json', 'w', encoding='utf-8') as f:
        json.dump(all_hanzi_list, f, ensure_ascii=False)
    print(f"✅ Đã cập nhật all_hanzi.json: {len(all_hanzi_list)} ký tự chữ Hán.")

    # 4. Regenerate HSK 1 game pages
    print("Đang tạo lại các trang game cho HSK 1...")
    from generate_games import generate_hsk_games
    generate_hsk_games(1)
    print("✅ Hoàn tất tạo lại game cho HSK 1!")

if __name__ == '__main__':
    main()
