import json
import os
import subprocess

# Paths
hsk1_path = 'hsk1_vocab_data.json'

# 20 target words for HSK1 Lesson 7
lesson7_words = [
    {
        "hanzi": "现在",
        "pinyin": "xiànzài",
        "meaning": "hiện tại, bây giờ",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "现在几点？",
        "ex_py": "Xiànzài jǐ diǎn?",
        "ex_vn": "Bây giờ mấy giờ?"
    },
    {
        "hanzi": "点",
        "pinyin": "diǎn",
        "meaning": "giờ",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "现在8点。",
        "ex_py": "Xiànzài bā diǎn.",
        "ex_vn": "Bây giờ 8 giờ."
    },
    {
        "hanzi": "分",
        "pinyin": "fēn",
        "meaning": "phút",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "8点15分。",
        "ex_py": "Bā diǎn shíwǔ fēn.",
        "ex_vn": "8 giờ 15 phút."
    },
    {
        "hanzi": "分钟",
        "pinyin": "fēnzhōng",
        "meaning": "phút",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "我5分钟后回家。",
        "ex_py": "Wǒ wǔ fēnzhōng hòu huíjiā.",
        "ex_vn": "5 phút nữa tôi về nhà."
    },
    {
        "hanzi": "上午",
        "pinyin": "shàngwǔ",
        "meaning": "buổi sáng",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "上午我吃一个包子。",
        "ex_py": "Shàngwǔ wǒ chī yí gè bāozi.",
        "ex_vn": "Buổi sáng tôi ăn một cái bánh bao."
    },
    {
        "hanzi": "下午",
        "pinyin": "xiàwǔ",
        "meaning": "buổi chiều",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "下午你去玩吗？",
        "ex_py": "Xiàwǔ nǐ qù wán ma?",
        "ex_vn": "Buổi chiều bạn đi chơi không?"
    },
    {
        "hanzi": "上课",
        "pinyin": "shàngkè",
        "meaning": "lên lớp, vào học",
        "lesson": "7",
        "type": "động từ",
        "ex_cn": "明天你上课吗？",
        "ex_py": "Míngtiān nǐ shàngkè ma?",
        "ex_vn": "Ngày mai bạn có đi học không?"
    },
    {
        "hanzi": "下课",
        "pinyin": "xiàkè",
        "meaning": "tan học, hết giờ",
        "lesson": "7",
        "type": "động từ",
        "ex_cn": "你几点下课？",
        "ex_py": "Nǐ jǐ diǎn xiàkè?",
        "ex_vn": "Mấy giờ bạn tan học?"
    },
    {
        "hanzi": "见",
        "pinyin": "jiàn",
        "meaning": "gặp, thấy",
        "lesson": "7",
        "type": "động từ",
        "ex_cn": "明天见。",
        "ex_py": "Míngtiān jiàn.",
        "ex_vn": "Ngày mai gặp lại."
    },
    {
        "hanzi": "吧",
        "pinyin": "ba",
        "meaning": "trợ từ (nhé, đi, thôi)",
        "lesson": "7",
        "type": "trợ từ ngữ khí",
        "ex_cn": "我们去看电影吧。",
        "ex_py": "Wǒmen qù kàn diànyǐng ba.",
        "ex_vn": "Chúng mình đi xem phim đi."
    },
    {
        "hanzi": "电影",
        "pinyin": "diànyǐng",
        "meaning": "phim",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "你喜欢看电影吗？",
        "ex_py": "Nǐ xǐhuan kàn diànyǐng ma?",
        "ex_vn": "Bạn thích xem phim không?"
    },
    {
        "hanzi": "电影院",
        "pinyin": "diànyǐngyuàn",
        "meaning": "rạp chiếu phim",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "我们在电影院见吧。",
        "ex_py": "Wǒmen zài diànyǐngyuàn jiàn ba.",
        "ex_vn": "Chúng ta gặp nhau ở rạp chiếu phim nhé."
    },
    {
        "hanzi": "事",
        "pinyin": "shì",
        "meaning": "việc, chuyện",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "下午我有事儿了。",
        "ex_py": "Xiàwǔ wǒ yǒu shìr le.",
        "ex_vn": "Buổi chiều tôi có việc rồi."
    },
    {
        "hanzi": "半",
        "pinyin": "bàn",
        "meaning": "nửa, rưỡi",
        "lesson": "7",
        "type": "số từ",
        "ex_cn": "我四点半下课。",
        "ex_py": "Wǒ sì diǎn bàn xiàkè.",
        "ex_vn": "Tôi tan học lúc 4 giờ rưỡi."
    },
    {
        "hanzi": "在",
        "pinyin": "zài",
        "meaning": "ở, tại",
        "lesson": "7",
        "type": "giới từ / động từ",
        "ex_cn": "我在房间里看书。",
        "ex_py": "Wǒ zài fángjiān lǐ kànshū.",
        "ex_vn": "Tôi đang đọc sách trong phòng."
    },
    {
        "hanzi": "医院",
        "pinyin": "yīyuàn",
        "meaning": "bệnh viện",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "爸爸在医院工作。",
        "ex_py": "Bàba zài yīyuàn gōngzuò.",
        "ex_vn": "Bố làm việc ở bệnh viện."
    },
    {
        "hanzi": "医生",
        "pinyin": "yīshēng",
        "meaning": "bác sĩ",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "我爸爸是医生。",
        "ex_py": "Wǒ bàba shì yīshēng.",
        "ex_vn": "Bố tôi là bác sĩ."
    },
    {
        "hanzi": "店",
        "pinyin": "diàn",
        "meaning": "tiệm",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "我去店里买东西。",
        "ex_py": "Wǒ qù diàn lǐ mǎi dōngxi.",
        "ex_vn": "Tôi đi cửa hàng mua đồ."
    },
    {
        "hanzi": "菜 / 蔬菜",
        "pinyin": "cài / shūcài",
        "meaning": "món ăn, rau",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "弟弟不喜欢吃蔬菜。",
        "ex_py": "Dìdi bù xǐhuan chī shūcài.",
        "ex_vn": "Em trai không thích ăn rau."
    },
    {
        "hanzi": "后",
        "pinyin": "hòu",
        "meaning": "sau, sau khi",
        "lesson": "7",
        "type": "danh từ",
        "ex_cn": "学校后有一家超市。",
        "ex_py": "Xuéxiào hòu yǒu yì jiā chāoshì.",
        "ex_vn": "Sau trường học có một siêu thị."
    }
]

def main():
    print("=== Cập nhật từ vựng HSK1 Bài 7 ===")
    with open(hsk1_path, 'r', encoding='utf-8') as f:
        hsk1_data = json.load(f)

    # Filter out existing Lesson 7 words
    before_l7 = [item for item in hsk1_data if str(item.get('lesson')) in {'1', '2', '3', '4', '5', '6'}]
    after_l7 = [item for item in hsk1_data if str(item.get('lesson')) not in {'1', '2', '3', '4', '5', '6', '7'}]

    # Combine: Lessons 1-6, new Lesson 7, then Lessons 8+
    updated_hsk1 = before_l7 + lesson7_words + after_l7

    with open(hsk1_path, 'w', encoding='utf-8') as f:
        json.dump(updated_hsk1, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã lưu {len(updated_hsk1)} từ vựng vào {hsk1_path} (Bài 7: {len(lesson7_words)} từ).")

    # Update all_hanzi.json
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

    # Regenerate HSK 1 game pages
    print("Đang tạo lại các trang game cho HSK 1...")
    from generate_games import generate_hsk_games
    generate_hsk_games(1)
    print("✅ Hoàn tất tạo lại game cho HSK 1!")

if __name__ == '__main__':
    main()
