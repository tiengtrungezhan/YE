import json
import os
import subprocess

# Paths
hsk1_path = 'hsk1_vocab_data.json'
hanzi_details_path = 'hsk1_hanzi_details.json'

# 19 target words for HSK1 Lesson 15
lesson15_words = [
    {
        "hanzi": "爱",
        "pinyin": "ài",
        "meaning": "yêu, thích",
        "lesson": "15",
        "type": "động từ",
        "ex_cn": "我爱爸爸妈妈。",
        "ex_py": "Wǒ ài bàba māma.",
        "ex_vn": "Tôi yêu bố mẹ."
    },
    {
        "hanzi": "哪个",
        "pinyin": "nǎge",
        "meaning": "cái nào, người nào",
        "lesson": "15",
        "type": "đại từ nghi vấn",
        "ex_cn": "哪个是你的？",
        "ex_py": "Nǎge shì nǐ de?",
        "ex_vn": "Cái nào là của bạn?"
    },
    {
        "hanzi": "去年",
        "pinyin": "qùnián",
        "meaning": "năm ngoái",
        "lesson": "15",
        "type": "danh từ",
        "ex_cn": "去年我去了北京。",
        "ex_py": "Qùnián wǒ qù le Běijīng.",
        "ex_vn": "Năm ngoái tôi đã đi Bắc Kinh."
    },
    {
        "hanzi": "男朋友",
        "pinyin": "nánpéngyou",
        "meaning": "bạn trai",
        "lesson": "15",
        "type": "danh từ",
        "ex_cn": "你有男朋友了吗？",
        "ex_py": "Nǐ yǒu nánpéngyou le ma?",
        "ex_vn": "Bạn có bạn trai chưa?"
    },
    {
        "hanzi": "几",
        "pinyin": "jǐ",
        "meaning": "mấy, vài",
        "lesson": "15",
        "type": "đại từ nghi vấn",
        "ex_cn": "我有几本书？",
        "ex_py": "Wǒ yǒu jǐ běn shū?",
        "ex_vn": "Tôi có mấy quyển sách?"
    },
    {
        "hanzi": "年",
        "pinyin": "nián",
        "meaning": "năm",
        "lesson": "15",
        "type": "lượng từ",
        "ex_cn": "今年是2026年。",
        "ex_py": "Jīnnián shì èr líng èr liù nián.",
        "ex_vn": "Năm nay là năm 2026."
    },
    {
        "hanzi": "好玩儿",
        "pinyin": "hǎowánr",
        "meaning": "vui, thú vị",
        "lesson": "15",
        "type": "tính từ",
        "ex_cn": "北京非常好玩儿。",
        "ex_py": "Běijīng fēicháng hǎowánr.",
        "ex_vn": "Bắc Kinh rất thú vị."
    },
    {
        "hanzi": "北京",
        "pinyin": "Běijīng",
        "meaning": "Bắc Kinh",
        "lesson": "15",
        "type": "danh từ riêng",
        "ex_cn": "我住在北京。",
        "ex_py": "Wǒ zhù zài Běijīng.",
        "ex_vn": "Tôi sống ở Bắc Kinh."
    },
    {
        "hanzi": "西安",
        "pinyin": "Xī'ān",
        "meaning": "Tây An",
        "lesson": "15",
        "type": "danh từ riêng",
        "ex_cn": "他住在西安。",
        "ex_py": "Tā zhù zài Xī'ān.",
        "ex_vn": "Anh ấy sống ở Tây An."
    },
    {
        "hanzi": "飞机",
        "pinyin": "fēijī",
        "meaning": "máy bay",
        "lesson": "15",
        "type": "danh từ",
        "ex_cn": "我坐飞机去北京。",
        "ex_py": "Wǒ zuò fēijī qù Běijīng.",
        "ex_vn": "Tôi đi máy bay đến Bắc Kinh."
    },
    {
        "hanzi": "要",
        "pinyin": "yào",
        "meaning": "cần, mất (thời gian)",
        "lesson": "15",
        "type": "động từ",
        "ex_cn": "去北京要两个小时。",
        "ex_py": "Qù Běijīng yào liǎng gè xiǎoshí.",
        "ex_vn": "Đi Bắc Kinh mất hai tiếng đồng hồ."
    },
    {
        "hanzi": "小时",
        "pinyin": "xiǎoshí",
        "meaning": "tiếng đồng hồ, giờ",
        "lesson": "15",
        "type": "lượng từ",
        "ex_cn": "坐车去西安要几个小时？",
        "ex_py": "Zuò chē qù Xī'ān yào jǐ gè xiǎoshí?",
        "ex_vn": "Ngồi xe đi Tây An mất mấy tiếng đồng hồ?"
    },
    {
        "hanzi": "家人",
        "pinyin": "jiārén",
        "meaning": "người nhà, gia đình",
        "lesson": "15",
        "type": "danh từ",
        "ex_cn": "这是你家人吗？",
        "ex_py": "Zhè shì nǐ jiārén ma?",
        "ex_vn": "Đây là người nhà của bạn à?"
    },
    {
        "hanzi": "时间",
        "pinyin": "shíjiān",
        "meaning": "thời gian",
        "lesson": "15",
        "type": "danh từ",
        "ex_cn": "你有时间吗？",
        "ex_py": "Nǐ yǒu shíjiān ma?",
        "ex_vn": "Bạn có thời gian không?"
    },
    {
        "hanzi": "机场",
        "pinyin": "jīchǎng",
        "meaning": "sân bay",
        "lesson": "15",
        "type": "danh từ",
        "ex_cn": "我现在要去机场。",
        "ex_py": "Wǒ xiànzài yào qù jīchǎng.",
        "ex_vn": "Bây giờ tôi phải đi sân bay."
    },
    {
        "hanzi": "接",
        "pinyin": "jiē",
        "meaning": "đón",
        "lesson": "15",
        "type": "động từ",
        "ex_cn": "我要去机场接朋友。",
        "ex_py": "Wǒ yào qù jīchǎng jiē péngyou.",
        "ex_vn": "Tôi muốn đi sân bay đón bạn."
    },
    {
        "hanzi": "住",
        "pinyin": "zhù",
        "meaning": "ở, sống, cư trú",
        "lesson": "15",
        "type": "động từ",
        "ex_cn": "我住在河内。",
        "ex_py": "Wǒ zhù zài Hénèi.",
        "ex_vn": "Tôi sống ở Hà Nội."
    },
    {
        "hanzi": "早",
        "pinyin": "zǎo",
        "meaning": "sớm",
        "lesson": "15",
        "type": "tính từ",
        "ex_cn": "太早了。",
        "ex_py": "Tài zǎo le.",
        "ex_vn": "Sớm quá rồi."
    },
    {
        "hanzi": "那",
        "pinyin": "nà",
        "meaning": "vậy, vậy thì",
        "lesson": "15",
        "type": "liên từ",
        "ex_cn": "那你休息一下吧。",
        "ex_py": "Nà nǐ xiūxi yíxià ba.",
        "ex_vn": "Vậy bạn nghỉ ngơi một lát đi."
    }
]

# Additional Hanzi details needed for Lesson 15
additional_hanzi_details = {
    "北": {
        "strokes": 5,
        "radical": "匕",
        "pinyin": "běi",
        "meaning": "hướng bắc, phía bắc",
        "mnemonic": "Hai người ngồi quay lưng lại với nhau (bối 背) tránh gió lạnh từ phương bắc."
    },
    "京": {
        "strokes": 8,
        "radical": "亠",
        "pinyin": "jīng",
        "meaning": "kinh đô, thủ đô, to lớn",
        "mnemonic": "Hình ảnh toà lầu cao lớn xây dựng trên gò đất cao tại kinh đô nguy nga."
    },
    "安": {
        "strokes": 6,
        "radical": "宀",
        "pinyin": "ān",
        "meaning": "an toàn, yên bình",
        "mnemonic": "Dưới mái nhà (miên 宀) có người phụ nữ (nữ 女) chăm lo gia đình thì mọi sự đều yên ấm, bình an."
    },
    "场": {
        "strokes": 6,
        "radical": "土",
        "pinyin": "chǎng",
        "meaning": "sân, bãi, quảng trường",
        "mnemonic": "Đất đai (thổ 土) rộng mở dưới ánh nắng mặt trời chiếu rọi (dương 𠃓), tạo thành khoảng sân bãi."
    },
    "接": {
        "strokes": 11,
        "radical": "扌",
        "pinyin": "jiē",
        "meaning": "đón, nhận, tiếp xúc",
        "mnemonic": "Bàn tay (thủ 扌) vươn ra đón nhận người phụ nữ (thiếp 妾), biểu thị việc đón tiếp, nhận lấy."
    }
}

def main():
    print("=== Cập nhật từ vựng HSK1 Bài 15 ===")

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

    # Filter out existing Lesson 15 words
    filtered_data = [item for item in hsk1_data if str(item.get('lesson')) != '15']

    # Split before lesson 15
    before_l15 = [item for item in filtered_data if int(item.get('lesson', 0)) < 15]

    # Combine: Lessons 1-14, new Lesson 15
    updated_hsk1 = before_l15 + lesson15_words

    with open(hsk1_path, 'w', encoding='utf-8') as f:
        json.dump(updated_hsk1, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã lưu {len(updated_hsk1)} từ vựng vào {hsk1_path} (Bài 15: {len(lesson15_words)} từ).")

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
