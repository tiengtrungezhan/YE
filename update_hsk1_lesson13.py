import json
import os
import subprocess

# Paths
hsk1_path = 'hsk1_vocab_data.json'
hanzi_details_path = 'hsk1_hanzi_details.json'

# 19 target words for HSK1 Lesson 13
lesson13_words = [
    {
        "hanzi": "可以",
        "pinyin": "kěyǐ",
        "meaning": "có thể, được",
        "lesson": "13",
        "type": "động từ năng nguyện",
        "ex_cn": "我可以坐在这里吗？",
        "ex_py": "Wǒ kěyǐ zuò zài zhèlǐ ma?",
        "ex_vn": "Tôi có thể ngồi ở đây không?"
    },
    {
        "hanzi": "再",
        "pinyin": "zài",
        "meaning": "thêm, lại, nữa",
        "lesson": "13",
        "type": "phó từ",
        "ex_cn": "再要一个饺子吧。",
        "ex_py": "Zài yào yí gè jiǎozi ba.",
        "ex_vn": "Lấy thêm một đĩa sủi cảo nữa đi."
    },
    {
        "hanzi": "问题",
        "pinyin": "wèntí",
        "meaning": "vấn đề, câu hỏi",
        "lesson": "13",
        "type": "danh từ",
        "ex_cn": "你有什么问题吗？",
        "ex_py": "Nǐ yǒu shénme wèntí ma?",
        "ex_vn": "Bạn có vấn đề gì không?"
    },
    {
        "hanzi": "卖",
        "pinyin": "mài",
        "meaning": "bán",
        "lesson": "13",
        "type": "động từ",
        "ex_cn": "我想卖这个。",
        "ex_py": "Wǒ xiǎng mài zhè ge.",
        "ex_vn": "Tôi muốn bán cái này."
    },
    {
        "hanzi": "打电话",
        "pinyin": "dǎ diànhuà",
        "meaning": "gọi điện thoại",
        "lesson": "13",
        "type": "động từ",
        "ex_cn": "你给老师打电话吧。",
        "ex_py": "Nǐ gěi lǎoshī dǎ diànhuà ba.",
        "ex_vn": "Bạn gọi điện thoại cho giáo viên đi."
    },
    {
        "hanzi": "一下",
        "pinyin": "yíxià",
        "meaning": "một chút, một lát",
        "lesson": "13",
        "type": "lượng từ",
        "ex_cn": "我想问你一下。",
        "ex_py": "Wǒ xiǎng wèn nǐ yíxià.",
        "ex_vn": "Tôi muốn hỏi bạn một chút."
    },
    {
        "hanzi": "服务员",
        "pinyin": "fúwùyuán",
        "meaning": "nhân viên phục vụ, bồi bàn",
        "lesson": "13",
        "type": "danh từ",
        "ex_cn": "我是这里的服务员。",
        "ex_py": "Wǒ shì zhèlǐ de fúwùyuán.",
        "ex_vn": "Tôi là nhân viên phục vụ ở đây."
    },
    {
        "hanzi": "女士",
        "pinyin": "nǚshì",
        "meaning": "quý cô, quý bà, tiểu thư",
        "lesson": "13",
        "type": "danh từ",
        "ex_cn": "王女士，请坐。",
        "ex_py": "Wáng nǚshì, qǐng zuò.",
        "ex_vn": "Vương tiểu thư, mời ngồi."
    },
    {
        "hanzi": "坐",
        "pinyin": "zuò",
        "meaning": "ngồi",
        "lesson": "13",
        "type": "động từ",
        "ex_cn": "你坐在这儿吧。",
        "ex_py": "Nǐ zuò zài zhèr ba.",
        "ex_vn": "Bạn ngồi ở đây đi."
    },
    {
        "hanzi": "请",
        "pinyin": "qǐng",
        "meaning": "xin, mời, làm ơn",
        "lesson": "13",
        "type": "động từ",
        "ex_cn": "请给我一杯热茶。",
        "ex_py": "Qǐng gěi wǒ yì bēi rè chá.",
        "ex_vn": "Làm ơn cho tôi một cốc trà nóng."
    },
    {
        "hanzi": "给",
        "pinyin": "gěi",
        "meaning": "cho, đưa cho",
        "lesson": "13",
        "type": "động từ",
        "ex_cn": "给我一杯水吧。",
        "ex_py": "Gěi wǒ yì bēi shuǐ ba.",
        "ex_vn": "Cho tôi một cốc nước nhé."
    },
    {
        "hanzi": "杯",
        "pinyin": "bēi",
        "meaning": "cốc, ly (lượng từ)",
        "lesson": "13",
        "type": "lượng từ",
        "ex_cn": "我要一杯奶茶。",
        "ex_py": "Wǒ yào yì bēi nǎichá.",
        "ex_vn": "Tôi muốn một cốc trà sữa."
    },
    {
        "hanzi": "要",
        "pinyin": "yào",
        "meaning": "muốn, lấy, cần",
        "lesson": "13",
        "type": "động từ",
        "ex_cn": "我要两个包子。",
        "ex_py": "Wǒ yào liǎng gè bāozi.",
        "ex_vn": "Tôi lấy hai cái bánh bao."
    },
    {
        "hanzi": "早饭",
        "pinyin": "zǎofàn",
        "meaning": "bữa sáng, cơm sáng",
        "lesson": "13",
        "type": "danh từ",
        "ex_cn": "我还没吃早饭。",
        "ex_py": "Wǒ hái méi chī zǎofàn.",
        "ex_vn": "Tôi vẫn chưa ăn sáng."
    },
    {
        "hanzi": "面包",
        "pinyin": "miànbāo",
        "meaning": "bánh mì",
        "lesson": "13",
        "type": "danh từ",
        "ex_cn": "我想吃面包。",
        "ex_py": "Wǒ xiǎng chī miànbāo.",
        "ex_vn": "Tôi muốn ăn bánh mì."
    },
    {
        "hanzi": "鸡蛋",
        "pinyin": "jīdàn",
        "meaning": "trứng gà",
        "lesson": "13",
        "type": "danh từ",
        "ex_cn": "我要两个鸡蛋。",
        "ex_py": "Wǒ yào liǎng gè jīdàn.",
        "ex_vn": "Tôi lấy hai quả trứng gà."
    },
    {
        "hanzi": "先生",
        "pinyin": "xiānsheng",
        "meaning": "ông, ngài, tiên sinh",
        "lesson": "13",
        "type": "danh từ",
        "ex_cn": "先生，请问你要喝什么？",
        "ex_py": "Xiānsheng, qǐngwèn nǐ yào hē shénme?",
        "ex_vn": "Thưa tiên sinh, xin hỏi anh muốn uống gì?"
    },
    {
        "hanzi": "一半",
        "pinyin": "yíbàn",
        "meaning": "một nửa, nửa",
        "lesson": "13",
        "type": "số lượng từ",
        "ex_cn": "一半饺子多少钱？",
        "ex_py": "Yíbàn jiǎozi duōshao qián?",
        "ex_vn": "Nửa phần sủi cảo giá bao nhiêu tiền?"
    },
    {
        "hanzi": "茶",
        "pinyin": "chá",
        "meaning": "trà, chè",
        "lesson": "13",
        "type": "danh từ",
        "ex_cn": "我要一杯茶。",
        "ex_py": "Wǒ yào yì bēi chá.",
        "ex_vn": "Tôi muốn một cốc trà."
    }
]

# Additional Hanzi details needed for Lesson 13
additional_hanzi_details = {
    "可": {
        "strokes": 5,
        "radical": "口",
        "pinyin": "kě",
        "meaning": "có thể, khả dĩ",
        "mnemonic": "Miệng (khẩu 口) có thể nói lời thuận tai, biểu thị sự cho phép, tán thành."
    },
    "以": {
        "strokes": 4,
        "radical": "人",
        "pinyin": "yǐ",
        "meaning": "lấy, dùng, có thể (trong 可以)",
        "mnemonic": "Dáng người cầm cái cày làm việc, biểu thị dựa vào, dùng vào việc gì."
    },
    "题": {
        "strokes": 15,
        "radical": "页",
        "pinyin": "tí",
        "meaning": "đề tài, vấn đề, câu hỏi",
        "mnemonic": "Đứng dưới ánh mặt trời (nhật 日) đúng đắn (thị 是) suy nghĩ bằng đầu óc (hiệt 页) để giải quyết đề thi, câu hỏi."
    },
    "卖": {
        "strokes": 8,
        "radical": "十",
        "pinyin": "mài",
        "meaning": "bán, tiêu thụ",
        "mnemonic": "Chữ thập (thập 十) trên chữ mãi (买 - mua), mang đồ mua về đi bán lại để kiếm lời."
    },
    "务": {
        "strokes": 5,
        "radical": "力",
        "pinyin": "wù",
        "meaning": "công việc, phục vụ (trong 服务)",
        "mnemonic": "Dùng mâu giáo và ra sức lực (lực 力) làm nhiệm vụ, phục vụ."
    },
    "给": {
        "strokes": 9,
        "radical": "纟",
        "pinyin": "gěi",
        "meaning": "cho, tặng, đưa cho",
        "mnemonic": "Dùng sợi tơ (mịch 纟) kết hợp (hợp 合) lại đem biếu tặng, đưa cho người khác."
    },
    "鸡": {
        "strokes": 7,
        "radical": "鸟",
        "pinyin": "jī",
        "meaning": "con gà",
        "mnemonic": "Con chim/gia cầm (điểu 鸟) có nét chữ hữu (又), gáy sáng sớm chính là con gà."
    },
    "蛋": {
        "strokes": 11,
        "radical": "虫",
        "pinyin": "dàn",
        "meaning": "quả trứng",
        "mnemonic": "Dưới chân (疋) sinh ra quả trứng nằm trên loài sâu bọ (trùng 虫), biểu thị trứng sinh nở."
    }
}

def main():
    print("=== Cập nhật từ vựng HSK1 Bài 13 ===")

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

    # Filter out existing Lesson 13 words
    filtered_data = [item for item in hsk1_data if str(item.get('lesson')) != '13']

    # Split before lesson 13 and after lesson 13
    before_l13 = [item for item in filtered_data if int(item.get('lesson', 0)) < 13]
    after_l13 = [item for item in filtered_data if int(item.get('lesson', 0)) > 13]

    # Combine: Lessons 1-12, new Lesson 13, then Lessons 14+
    updated_hsk1 = before_l13 + lesson13_words + after_l13

    with open(hsk1_path, 'w', encoding='utf-8') as f:
        json.dump(updated_hsk1, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã lưu {len(updated_hsk1)} từ vựng vào {hsk1_path} (Bài 13: {len(lesson13_words)} từ).")

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
