import json
import os
import subprocess

# Paths
hsk1_path = 'hsk1_vocab_data.json'

# 22 target words for HSK1 Lesson 14
lesson14_words = [
    {
        "hanzi": "上",
        "pinyin": "shàng",
        "meaning": "lên, bước lên (xe, tàu)",
        "lesson": "14",
        "type": "động từ",
        "ex_cn": "你上车了吗？",
        "ex_py": "Nǐ shàng chē le ma?",
        "ex_vn": "Bạn lên xe chưa?"
    },
    {
        "hanzi": "火车",
        "pinyin": "huǒchē",
        "meaning": "tàu hỏa",
        "lesson": "14",
        "type": "danh từ",
        "ex_cn": "我上火车了。",
        "ex_py": "Wǒ shàng huǒchē le.",
        "ex_vn": "Tôi lên tàu hỏa rồi."
    },
    {
        "hanzi": "中午",
        "pinyin": "zhōngwǔ",
        "meaning": "buổi trưa",
        "lesson": "14",
        "type": "danh từ",
        "ex_cn": "中午你吃什么？",
        "ex_py": "Zhōngwǔ nǐ chī shénme?",
        "ex_vn": "Trưa nay bạn ăn gì?"
    },
    {
        "hanzi": "开",
        "pinyin": "kāi",
        "meaning": "chạy, xuất phát (xe), mở",
        "lesson": "14",
        "type": "động từ",
        "ex_cn": "车开了吗？",
        "ex_py": "Chē kāi le ma?",
        "ex_vn": "Xe xuất phát chưa?"
    },
    {
        "hanzi": "有些",
        "pinyin": "yǒuxiē",
        "meaning": "có một số, có những",
        "lesson": "14",
        "type": "đại từ",
        "ex_cn": "有些人喜欢中文，有些人喜欢英文。",
        "ex_py": "Yǒuxiē rén xǐhuan Zhōngwén, yǒuxiē rén xǐhuan Yīngwén.",
        "ex_vn": "Có người thích tiếng Trung, có người thích tiếng Anh."
    },
    {
        "hanzi": "有的",
        "pinyin": "yǒude",
        "meaning": "có người, có cái, một số",
        "lesson": "14",
        "type": "đại từ",
        "ex_cn": "我们班有的是越南人，有的是中国人。",
        "ex_py": "Wǒmen bān yǒude shì Yuènánrén, yǒude shì Zhōngguórén.",
        "ex_vn": "Lớp chúng tôi có người là người Việt Nam, có người là người Trung Quốc."
    },
    {
        "hanzi": "写",
        "pinyin": "xiě",
        "meaning": "viết",
        "lesson": "14",
        "type": "động từ",
        "ex_cn": "你会写汉字吗？",
        "ex_py": "Nǐ huì xiě hànzì ma?",
        "ex_vn": "Bạn có biết viết chữ Hán không?"
    },
    {
        "hanzi": "都",
        "pinyin": "dōu",
        "meaning": "đều, cũng",
        "lesson": "14",
        "type": "phó từ",
        "ex_cn": "我们都是越南人。",
        "ex_py": "Wǒmen dōu shì Yuènánrén.",
        "ex_vn": "Chúng tôi đều là người Việt Nam."
    },
    {
        "hanzi": "听",
        "pinyin": "tīng",
        "meaning": "nghe",
        "lesson": "14",
        "type": "động từ",
        "ex_cn": "你在听什么？",
        "ex_py": "Nǐ zài tīng shénme?",
        "ex_vn": "Bạn đang nghe gì thế?"
    },
    {
        "hanzi": "听见",
        "pinyin": "tīngjiàn",
        "meaning": "nghe thấy",
        "lesson": "14",
        "type": "động từ",
        "ex_cn": "你听见他在说什么吗？",
        "ex_py": "Nǐ tīngjiàn tā zài shuō shénme ma?",
        "ex_vn": "Bạn có nghe thấy anh ấy đang nói gì không?"
    },
    {
        "hanzi": "不要",
        "pinyin": "búyào",
        "meaning": "đừng, không được",
        "lesson": "14",
        "type": "phó từ",
        "ex_cn": "不要说话。",
        "ex_py": "Búyào shuōhuà.",
        "ex_vn": "Đừng nói chuyện."
    },
    {
        "hanzi": "哪些",
        "pinyin": "nǎxiē",
        "meaning": "những nào, những cái nào",
        "lesson": "14",
        "type": "đại từ nghi vấn",
        "ex_cn": "你会写哪些字？",
        "ex_py": "Nǐ huì xiě nǎxiē zì?",
        "ex_vn": "Bạn biết viết những chữ nào?"
    },
    {
        "hanzi": "汉语",
        "pinyin": "Hànyǔ",
        "meaning": "tiếng Hán, tiếng Trung",
        "lesson": "14",
        "type": "danh từ",
        "ex_cn": "我喜欢学汉语。",
        "ex_py": "Wǒ xǐhuan xué Hànyǔ.",
        "ex_vn": "Tôi thích học tiếng Trung."
    },
    {
        "hanzi": "明年",
        "pinyin": "míngnián",
        "meaning": "năm sau, sang năm",
        "lesson": "14",
        "type": "danh từ",
        "ex_cn": "明年我去中国玩儿。",
        "ex_py": "Míngnián wǒ qù Zhōngguó wánr.",
        "ex_vn": "Năm sau tôi đi Trung Quốc chơi."
    },
    {
        "hanzi": "中学",
        "pinyin": "zhōngxué",
        "meaning": "trường trung học, cấp hai",
        "lesson": "14",
        "type": "danh từ",
        "ex_cn": "弟弟在读中学。",
        "ex_py": "Dìdi zài dú zhōngxué.",
        "ex_vn": "Em trai đang học trung học."
    },
    {
        "hanzi": "说话",
        "pinyin": "shuōhuà",
        "meaning": "nói chuyện, trò chuyện",
        "lesson": "14",
        "type": "động từ",
        "ex_cn": "他们在说话。",
        "ex_py": "Tāmen zài shuōhuà.",
        "ex_vn": "Bọn họ đang nói chuyện."
    },
    {
        "hanzi": "字",
        "pinyin": "zì",
        "meaning": "chữ, từ",
        "lesson": "14",
        "type": "danh từ",
        "ex_cn": "我喜欢写汉字。",
        "ex_py": "Wǒ xǐhuan xiě hànzì.",
        "ex_vn": "Tôi thích viết chữ Hán."
    },
    {
        "hanzi": "汉字",
        "pinyin": "hànzì",
        "meaning": "chữ Hán",
        "lesson": "14",
        "type": "danh từ",
        "ex_cn": "你会写这个汉字吗？",
        "ex_py": "Nǐ huì xiě zhè ge hànzì ma?",
        "ex_vn": "Bạn có biết viết chữ Hán này không?"
    },
    {
        "hanzi": "小学",
        "pinyin": "xiǎoxué",
        "meaning": "trường tiểu học, cấp một",
        "lesson": "14",
        "type": "danh từ",
        "ex_cn": "妹妹在读小学。",
        "ex_py": "Mèimei zài dú xiǎoxué.",
        "ex_vn": "Em gái đang học tiểu học."
    },
    {
        "hanzi": "晚",
        "pinyin": "wǎn",
        "meaning": "muộn, trễ",
        "lesson": "14",
        "type": "tính từ",
        "ex_cn": "现在太晚了。",
        "ex_py": "Xiànzài tài wǎn le.",
        "ex_vn": "Bây giờ muộn quá rồi."
    },
    {
        "hanzi": "小学生",
        "pinyin": "xiǎoxuéshēng",
        "meaning": "học sinh tiểu học",
        "lesson": "14",
        "type": "danh từ",
        "ex_cn": "弟弟是小学生。",
        "ex_py": "Dìdi shì xiǎoxuéshēng.",
        "ex_vn": "Em trai là học sinh tiểu học."
    },
    {
        "hanzi": "中学生",
        "pinyin": "zhōngxuéshēng",
        "meaning": "học sinh trung học",
        "lesson": "14",
        "type": "danh từ",
        "ex_cn": "妹妹是中学生。",
        "ex_py": "Mèimei shì zhōngxuéshēng.",
        "ex_vn": "Em gái là học sinh trung học."
    }
]

def main():
    print("=== Cập nhật từ vựng HSK1 Bài 14 ===")

    # 1. Update hsk1_vocab_data.json
    with open(hsk1_path, 'r', encoding='utf-8') as f:
        hsk1_data = json.load(f)

    # Filter out existing Lesson 14 words and remove '明年' from Lesson 15 to avoid duplicate
    filtered_data = []
    for item in hsk1_data:
        l_str = str(item.get('lesson'))
        h = item.get('hanzi')
        if l_str == '14':
            continue
        if l_str == '15' and h == '明年':
            continue
        filtered_data.append(item)

    # Split before lesson 14 and after lesson 14
    before_l14 = [item for item in filtered_data if int(item.get('lesson', 0)) < 14]
    after_l14 = [item for item in filtered_data if int(item.get('lesson', 0)) > 14]

    # Combine: Lessons 1-13, new Lesson 14, then Lessons 15+
    updated_hsk1 = before_l14 + lesson14_words + after_l14

    with open(hsk1_path, 'w', encoding='utf-8') as f:
        json.dump(updated_hsk1, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã lưu {len(updated_hsk1)} từ vựng vào {hsk1_path} (Bài 14: {len(lesson14_words)} từ).")

    # 2. Update all_hanzi.json
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

    # 3. Regenerate HSK 1 game pages
    print("Đang tạo lại các trang game cho HSK 1...")
    from generate_games import generate_hsk_games
    generate_hsk_games(1)
    print("✅ Hoàn tất tạo lại game cho HSK 1!")

if __name__ == '__main__':
    main()
