import json
import os
import subprocess

# Paths
hsk1_path = 'hsk1_vocab_data.json'
hanzi_details_path = 'hsk1_hanzi_details.json'

# 16 target words for HSK1 Lesson 8
lesson8_words = [
    {
        "hanzi": "房间",
        "pinyin": "fángjiān",
        "meaning": "phòng, căn phòng",
        "lesson": "8",
        "type": "danh từ",
        "ex_cn": "我在房间里呢。",
        "ex_py": "Wǒ zài fángjiān lǐ ne.",
        "ex_vn": "Tôi đang ở trong phòng nè."
    },
    {
        "hanzi": "外",
        "pinyin": "wài",
        "meaning": "ngoài, bên ngoài",
        "lesson": "8",
        "type": "danh từ",
        "ex_cn": "房间外有很多人。",
        "ex_py": "Fángjiān wài yǒu hěn duō rén.",
        "ex_vn": "Bên ngoài phòng có rất nhiều người."
    },
    {
        "hanzi": "猫",
        "pinyin": "māo",
        "meaning": "mèo, con mèo",
        "lesson": "8",
        "type": "danh từ",
        "ex_cn": "我有一只猫。",
        "ex_py": "Wǒ yǒu yì zhī māo.",
        "ex_vn": "Tôi có một con mèo."
    },
    {
        "hanzi": "小",
        "pinyin": "xiǎo",
        "meaning": "nhỏ, bé",
        "lesson": "8",
        "type": "tính từ",
        "ex_cn": "这只小猫是我的。",
        "ex_py": "Zhè zhī xiǎomāo shì wǒ de.",
        "ex_vn": "Con mèo nhỏ này là của tôi."
    },
    {
        "hanzi": "只",
        "pinyin": "zhī",
        "meaning": "con (lượng từ)",
        "lesson": "8",
        "type": "lượng từ",
        "ex_cn": "这只狗是你的吗？",
        "ex_py": "Zhè zhī gǒu shì nǐ de ma?",
        "ex_vn": "Con chó này là của bạn phải không?"
    },
    {
        "hanzi": "没",
        "pinyin": "méi",
        "meaning": "không, chưa",
        "lesson": "8",
        "type": "phó từ",
        "ex_cn": "我没看见他。",
        "ex_py": "Wǒ méi kànjiàn tā.",
        "ex_vn": "Tôi không nhìn thấy anh ấy."
    },
    {
        "hanzi": "看见",
        "pinyin": "kànjiàn",
        "meaning": "nhìn thấy, thấy",
        "lesson": "8",
        "type": "động từ",
        "ex_cn": "你看见我的猫吗？",
        "ex_py": "Nǐ kànjiàn wǒ de māo ma?",
        "ex_vn": "Bạn có nhìn thấy con mèo của tôi không?"
    },
    {
        "hanzi": "漂亮",
        "pinyin": "piàoliang",
        "meaning": "đẹp, xinh đẹp",
        "lesson": "8",
        "type": "tính từ",
        "ex_cn": "她很漂亮。",
        "ex_py": "Tā hěn piàoliang.",
        "ex_vn": "Cô ấy rất đẹp."
    },
    {
        "hanzi": "桌子",
        "pinyin": "zhuōzi",
        "meaning": "cái bàn",
        "lesson": "8",
        "type": "danh từ",
        "ex_cn": "桌子上有一台电脑。",
        "ex_py": "Zhuōzi shang yǒu yì tái diànnǎo.",
        "ex_vn": "Trên bàn có một chiếc máy tính."
    },
    {
        "hanzi": "前",
        "pinyin": "qián",
        "meaning": "trước, phía trước",
        "lesson": "8",
        "type": "danh từ",
        "ex_cn": "学校前有一家超市。",
        "ex_py": "Xuéxiào qián yǒu yì jiā chāoshì.",
        "ex_vn": "Phía trước trường học có một siêu thị."
    },
    {
        "hanzi": "学校",
        "pinyin": "xuéxiào",
        "meaning": "trường học",
        "lesson": "8",
        "type": "danh từ",
        "ex_cn": "我在学校学中文。",
        "ex_py": "Wǒ zài xuéxiào xué Zhōngwén.",
        "ex_vn": "Tôi học tiếng Trung ở trường."
    },
    {
        "hanzi": "书店",
        "pinyin": "shūdiàn",
        "meaning": "hiệu sách, nhà sách",
        "lesson": "8",
        "type": "danh từ",
        "ex_cn": "我去书店买书。",
        "ex_py": "Wǒ qù shūdiàn mǎi shū.",
        "ex_vn": "Tôi đi hiệu sách mua sách."
    },
    {
        "hanzi": "能",
        "pinyin": "néng",
        "meaning": "có thể",
        "lesson": "8",
        "type": "động từ năng nguyện",
        "ex_cn": "你下午4点能回家吗？",
        "ex_py": "Nǐ xiàwǔ sì diǎn néng huíjiā ma?",
        "ex_vn": "Chiều 4 giờ bạn có thể về nhà không?"
    },
    {
        "hanzi": "到",
        "pinyin": "dào",
        "meaning": "đến, tới",
        "lesson": "8",
        "type": "động từ",
        "ex_cn": "你到中国了吗？",
        "ex_py": "Nǐ dào Zhōngguó le ma?",
        "ex_vn": "Bạn đã đến Trung Quốc chưa?"
    },
    {
        "hanzi": "病人",
        "pinyin": "bìngrén",
        "meaning": "bệnh nhân, người bệnh",
        "lesson": "8",
        "type": "danh từ",
        "ex_cn": "大医院有很多病人。",
        "ex_py": "Dà yīyuàn yǒu hěn duō bìngrén.",
        "ex_vn": "Bệnh viện lớn có rất nhiều bệnh nhân."
    },
    {
        "hanzi": "看病",
        "pinyin": "kànbìng",
        "meaning": "khám bệnh, chữa bệnh",
        "lesson": "8",
        "type": "động từ",
        "ex_cn": "医生在给我看病。",
        "ex_py": "Yīshēng zài gěi wǒ kànbìng.",
        "ex_vn": "Bác sĩ đang khám bệnh cho tôi."
    }
]

# Additional Hanzi details needed for Lesson 8
additional_hanzi_details = {
    "房": {
        "strokes": 8,
        "radical": "户",
        "pinyin": "fáng",
        "meaning": "phòng, nhà",
        "mnemonic": "Dưới mái nhà (hộ 户) có phương hướng (phương 方), tạo nên gian phòng ấm cúng."
    },
    "间": {
        "strokes": 7,
        "radical": "门",
        "pinyin": "jiān",
        "meaning": "gian, phòng, khoảng giữa",
        "mnemonic": "Cánh cửa (môn 门) hé mở đón ánh sáng mặt trời (nhật 日), tức khoảng không gian bên trong."
    },
    "只": {
        "strokes": 5,
        "radical": "口",
        "pinyin": "zhī",
        "meaning": "con (lượng từ), chỉ",
        "mnemonic": "Miệng (khẩu 口) trên hai nét bát (八), biểu thị một con vật hoặc cá thể riêng biệt."
    },
    "到": {
        "strokes": 8,
        "radical": "刂",
        "pinyin": "dào",
        "meaning": "đến, tới",
        "mnemonic": "Đến nơi (chí 至) dùng dao (đao 刂) khắc ghi lại điểm mốc."
    }
}

def main():
    print("=== Cập nhật từ vựng HSK1 Bài 8 ===")

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

    # Filter out existing Lesson 8 words
    # Also remove '学校' from Lesson 9 and '看病' from Lesson 12 to avoid duplicates
    filtered_data = []
    for item in hsk1_data:
        l_str = str(item.get('lesson'))
        h = item.get('hanzi')
        if l_str == '8':
            continue
        if l_str == '9' and h == '学校':
            continue
        if l_str == '12' and h == '看病':
            continue
        filtered_data.append(item)

    # Split before lesson 8 and after lesson 8
    before_l8 = [item for item in filtered_data if int(item.get('lesson', 0)) < 8]
    after_l8 = [item for item in filtered_data if int(item.get('lesson', 0)) > 8]

    # Combine: Lessons 1-7, new Lesson 8, then Lessons 9+
    updated_hsk1 = before_l8 + lesson8_words + after_l8

    with open(hsk1_path, 'w', encoding='utf-8') as f:
        json.dump(updated_hsk1, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã lưu {len(updated_hsk1)} từ vựng vào {hsk1_path} (Bài 8: {len(lesson8_words)} từ).")

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
