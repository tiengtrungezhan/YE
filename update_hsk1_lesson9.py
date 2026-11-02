import json
import os
import subprocess

# Paths
hsk1_path = 'hsk1_vocab_data.json'

# 18 target words for HSK1 Lesson 9
lesson9_words = [
    {
        "hanzi": "前边",
        "pinyin": "qiánbiān",
        "meaning": "phía trước, đằng trước",
        "lesson": "9",
        "type": "danh từ chỉ phương vị",
        "ex_cn": "前边的那个人是谁？",
        "ex_py": "Qiánbiān de nà ge rén shì shéi?",
        "ex_vn": "Người phía trước là ai?"
    },
    {
        "hanzi": "外边",
        "pinyin": "wàibiān",
        "meaning": "bên ngoài, phía ngoài",
        "lesson": "9",
        "type": "danh từ chỉ phương vị",
        "ex_cn": "我们去外边吃饭吧。",
        "ex_py": "Wǒmen qù wàibiān chī fàn ba.",
        "ex_vn": "Chúng mình ra bên ngoài ăn cơm đi."
    },
    {
        "hanzi": "椅子",
        "pinyin": "yǐzi",
        "meaning": "ghế, cái ghế",
        "lesson": "9",
        "type": "danh từ",
        "ex_cn": "椅子下有一只小猫。",
        "ex_py": "Yǐzi xià yǒu yì zhī xiǎomāo.",
        "ex_vn": "Dưới ghế có một con mèo nhỏ."
    },
    {
        "hanzi": "本",
        "pinyin": "běn",
        "meaning": "cuốn, quyển (lượng từ)",
        "lesson": "9",
        "type": "lượng từ",
        "ex_cn": "这本书是我的。",
        "ex_py": "Zhè běn shū shì wǒ de.",
        "ex_vn": "Cuốn sách này là của tôi."
    },
    {
        "hanzi": "第",
        "pinyin": "dì",
        "meaning": "thứ (chỉ thứ tự)",
        "lesson": "9",
        "type": "tiền tố",
        "ex_cn": "这是我的第二本书。",
        "ex_py": "Zhè shì wǒ de dì-èr běn shū.",
        "ex_vn": "Đây là cuốn sách thứ hai của tôi."
    },
    {
        "hanzi": "电视",
        "pinyin": "diànshì",
        "meaning": "ti vi, truyền hình",
        "lesson": "9",
        "type": "danh từ",
        "ex_cn": "我喜欢看电视。",
        "ex_py": "Wǒ xǐhuan kàn diànshì.",
        "ex_vn": "Tôi thích xem tivi."
    },
    {
        "hanzi": "狗",
        "pinyin": "gǒu",
        "meaning": "chó, con chó",
        "lesson": "9",
        "type": "danh từ",
        "ex_cn": "这只狗是我的。",
        "ex_py": "Zhè zhī gǒu shì wǒ de.",
        "ex_vn": "Con chó này là của tôi."
    },
    {
        "hanzi": "学习",
        "pinyin": "xuéxí",
        "meaning": "học tập, học bài",
        "lesson": "9",
        "type": "động từ",
        "ex_cn": "我在学习呢。",
        "ex_py": "Wǒ zài xuéxí ne.",
        "ex_vn": "Tôi đang học bài nè."
    },
    {
        "hanzi": "白天",
        "pinyin": "báitiān",
        "meaning": "ban ngày",
        "lesson": "9",
        "type": "danh từ",
        "ex_cn": "她白天上班，晚上休息。",
        "ex_py": "Tā báitiān shàngbān, wǎnshang xiūxi.",
        "ex_vn": "Ban ngày cô ấy đi làm, buổi tối nghỉ ngơi."
    },
    {
        "hanzi": "读书",
        "pinyin": "dúshū",
        "meaning": "đọc sách, đi học",
        "lesson": "9",
        "type": "động từ",
        "ex_cn": "弟弟在房间里读书呢。",
        "ex_py": "Dìdi zài fángjiān lǐ dúshū ne.",
        "ex_vn": "Em trai đang đọc sách trong phòng."
    },
    {
        "hanzi": "读",
        "pinyin": "dú",
        "meaning": "đọc",
        "lesson": "9",
        "type": "động từ",
        "ex_cn": "这个怎么读？",
        "ex_py": "Zhè ge zěnme dú?",
        "ex_vn": "Cái này đọc như thế nào?"
    },
    {
        "hanzi": "书",
        "pinyin": "shū",
        "meaning": "sách",
        "lesson": "9",
        "type": "danh từ",
        "ex_cn": "这是我的书。",
        "ex_py": "Zhè shì wǒ de shū.",
        "ex_vn": "Đây là sách của tôi."
    },
    {
        "hanzi": "唱歌",
        "pinyin": "chànggē",
        "meaning": "ca hát, hát",
        "lesson": "9",
        "type": "động từ",
        "ex_cn": "我喜欢唱歌。",
        "ex_py": "Wǒ xǐhuan chànggē.",
        "ex_vn": "Tôi thích hát."
    },
    {
        "hanzi": "唱",
        "pinyin": "chàng",
        "meaning": "hát",
        "lesson": "9",
        "type": "động từ",
        "ex_cn": "你在唱什么？",
        "ex_py": "Nǐ zài chàng shénme?",
        "ex_vn": "Bạn đang hát gì vậy?"
    },
    {
        "hanzi": "歌",
        "pinyin": "gē",
        "meaning": "bài hát",
        "lesson": "9",
        "type": "danh từ",
        "ex_cn": "这是什么歌？",
        "ex_py": "Zhè shì shénme gē?",
        "ex_vn": "Đây là bài gì vậy?"
    },
    {
        "hanzi": "好听",
        "pinyin": "hǎotīng",
        "meaning": "hay (âm thanh, bài hát), dễ nghe",
        "lesson": "9",
        "type": "tính từ",
        "ex_cn": "这首歌很好听。",
        "ex_py": "Zhè shǒu gē hěn hǎotīng.",
        "ex_vn": "Bài hát này rất hay."
    },
    {
        "hanzi": "听",
        "pinyin": "tīng",
        "meaning": "nghe",
        "lesson": "9",
        "type": "động từ",
        "ex_cn": "你在听什么？",
        "ex_py": "Nǐ zài tīng shénme?",
        "ex_vn": "Bạn đang nghe gì vậy?"
    },
    {
        "hanzi": "玩",
        "pinyin": "wán",
        "meaning": "chơi",
        "lesson": "9",
        "type": "động từ",
        "ex_cn": "我们去玩儿吧。",
        "ex_py": "Wǒmen qù wánr ba.",
        "ex_vn": "Chúng ta đi chơi đi."
    }
]

def main():
    print("=== Cập nhật từ vựng HSK1 Bài 9 ===")

    # 1. Update hsk1_vocab_data.json
    with open(hsk1_path, 'r', encoding='utf-8') as f:
        hsk1_data = json.load(f)

    # Filter out existing Lesson 9 words and remove '读' from Lesson 11 to avoid duplicate
    filtered_data = []
    for item in hsk1_data:
        l_str = str(item.get('lesson'))
        h = item.get('hanzi')
        if l_str == '9':
            continue
        if l_str == '11' and h == '读':
            continue
        filtered_data.append(item)

    # Split before lesson 9 and after lesson 9
    before_l9 = [item for item in filtered_data if int(item.get('lesson', 0)) < 9]
    after_l9 = [item for item in filtered_data if int(item.get('lesson', 0)) > 9]

    # Combine: Lessons 1-8, new Lesson 9, then Lessons 10+
    updated_hsk1 = before_l9 + lesson9_words + after_l9

    with open(hsk1_path, 'w', encoding='utf-8') as f:
        json.dump(updated_hsk1, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã lưu {len(updated_hsk1)} từ vựng vào {hsk1_path} (Bài 9: {len(lesson9_words)} từ).")

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
