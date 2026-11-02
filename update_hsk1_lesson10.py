import json
import os
import subprocess

# Paths
hsk1_path = 'hsk1_vocab_data.json'
hanzi_details_path = 'hsk1_hanzi_details.json'

# 15 target words for HSK1 Lesson 10
lesson10_words = [
    {
        "hanzi": "杯子",
        "pinyin": "bēizi",
        "meaning": "cốc, ly",
        "lesson": "10",
        "type": "danh từ",
        "ex_cn": "我想买杯子。",
        "ex_py": "Wǒ xiǎng mǎi bēizi.",
        "ex_vn": "Tôi muốn mua cốc/ly."
    },
    {
        "hanzi": "售货员",
        "pinyin": "shòuhuòyuán",
        "meaning": "nhân viên bán hàng",
        "lesson": "10",
        "type": "danh từ",
        "ex_cn": "我姐姐是售货员。",
        "ex_py": "Wǒ jiějie shì shòuhuòyuán.",
        "ex_vn": "Chị gái tôi là nhân viên bán hàng."
    },
    {
        "hanzi": "钱",
        "pinyin": "qián",
        "meaning": "tiền",
        "lesson": "10",
        "type": "danh từ",
        "ex_cn": "这个多少钱？",
        "ex_py": "Zhè ge duōshao qián?",
        "ex_vn": "Cái này bao nhiêu tiền?"
    },
    {
        "hanzi": "块 / 元",
        "pinyin": "kuài / yuán",
        "meaning": "tệ, đồng (đơn vị tiền tệ)",
        "lesson": "10",
        "type": "lượng từ",
        "ex_cn": "这个十块钱。",
        "ex_py": "Zhè ge shí kuài qián.",
        "ex_vn": "Cái này 10 tệ."
    },
    {
        "hanzi": "水果",
        "pinyin": "shuǐguǒ",
        "meaning": "hoa quả, trái cây",
        "lesson": "10",
        "type": "danh từ",
        "ex_cn": "我想买水果。",
        "ex_py": "Wǒ xiǎng mǎi shuǐguǒ.",
        "ex_vn": "Tôi muốn mua hoa quả."
    },
    {
        "hanzi": "水",
        "pinyin": "shuǐ",
        "meaning": "nước",
        "lesson": "10",
        "type": "danh từ",
        "ex_cn": "我想喝水。",
        "ex_py": "Wǒ xiǎng hē shuǐ.",
        "ex_vn": "Tôi muốn uống nước."
    },
    {
        "hanzi": "衣服",
        "pinyin": "yīfu",
        "meaning": "quần áo, trang phục",
        "lesson": "10",
        "type": "danh từ",
        "ex_cn": "这件衣服是我的。",
        "ex_py": "Zhè jiàn yīfu shì wǒ de.",
        "ex_vn": "Bộ quần áo này là của tôi."
    },
    {
        "hanzi": "穿",
        "pinyin": "chuān",
        "meaning": "mặc, xỏ",
        "lesson": "10",
        "type": "động từ",
        "ex_cn": "我穿这件好看吗？",
        "ex_py": "Wǒ chuān zhè jiàn hǎokàn ma?",
        "ex_vn": "Tôi mặc bộ này đẹp không?"
    },
    {
        "hanzi": "苹果",
        "pinyin": "píngguǒ",
        "meaning": "táo, quả táo",
        "lesson": "10",
        "type": "danh từ",
        "ex_cn": "我想买一些苹果。",
        "ex_py": "Wǒ xiǎng mǎi yìxiē píngguǒ.",
        "ex_vn": "Tôi muốn mua một ít táo."
    },
    {
        "hanzi": "斤 / 公斤",
        "pinyin": "jīn / gōngjīn",
        "meaning": "cân (0.5kg) / kg (ki-lô-gam)",
        "lesson": "10",
        "type": "lượng từ",
        "ex_cn": "苹果多少钱一斤？",
        "ex_py": "Píngguǒ duōshao qián yì jīn?",
        "ex_vn": "Táo bao nhiêu tiền một cân?"
    },
    {
        "hanzi": "便宜",
        "pinyin": "piányi",
        "meaning": "rẻ",
        "lesson": "10",
        "type": "tính từ",
        "ex_cn": "这里的水果很便宜。",
        "ex_py": "Zhèlǐ de shuǐguǒ hěn piányi.",
        "ex_vn": "Hoa quả ở đây rất rẻ."
    },
    {
        "hanzi": "贵",
        "pinyin": "guì",
        "meaning": "đắt, quý",
        "lesson": "10",
        "type": "tính từ",
        "ex_cn": "这个太贵了。",
        "ex_py": "Zhè ge tài guì le.",
        "ex_vn": "Cái này đắt quá."
    },
    {
        "hanzi": "商店",
        "pinyin": "shāngdiàn",
        "meaning": "cửa hàng",
        "lesson": "10",
        "type": "danh từ",
        "ex_cn": "商店里有很多人。",
        "ex_py": "Shāngdiàn lǐ yǒu hěn duō rén.",
        "ex_vn": "Trong cửa hàng có rất nhiều người."
    },
    {
        "hanzi": "件",
        "pinyin": "jiàn",
        "meaning": "chiếc, bộ (quần áo), kiện",
        "lesson": "10",
        "type": "lượng từ",
        "ex_cn": "这件衣服是我的。",
        "ex_py": "Zhè jiàn yīfu shì wǒ de.",
        "ex_vn": "Bộ quần áo này là của tôi."
    },
    {
        "hanzi": "怎么样",
        "pinyin": "zěnmeyàng",
        "meaning": "thế nào, ra sao",
        "lesson": "10",
        "type": "đại từ nghi vấn",
        "ex_cn": "你觉得这件怎么样？",
        "ex_py": "Nǐ juéde zhè jiàn zěnmeyàng?",
        "ex_vn": "Bạn thấy bộ này thế nào?"
    }
]

# Additional Hanzi details needed for Lesson 10
additional_hanzi_details = {
    "穿": {
        "strokes": 9,
        "radical": "穴",
        "pinyin": "chuān",
        "meaning": "mặc, xỏ, xuyên qua",
        "mnemonic": "Dưới hang động (huyệt 穴), nha (răng 牙) xuyên qua cắn xé. Mặc đồ giống như chui người qua hang."
    },
    "货": {
        "strokes": 8,
        "radical": "贝",
        "pinyin": "huò",
        "meaning": "hàng hoá, của cải",
        "mnemonic": "Biến đổi (hóa 化) tài bảo/vỏ sò (bối 贝) thành hàng hóa trao đổi."
    },
    "斤": {
        "strokes": 4,
        "radical": "斤",
        "pinyin": "jīn",
        "meaning": "cân (0.5kg), rìu",
        "mnemonic": "Hình dạng chiếc rìu dùng để đẽo gọt và làm quả cân đo lường."
    },
    "便": {
        "strokes": 9,
        "radical": "亻",
        "pinyin": "biàn / pián",
        "meaning": "tiện lợi, rẻ (trong 便宜)",
        "mnemonic": "Người (nhân 亻) nói lời đổi mới (canh 更), giúp mọi việc trở nên thuận tiện, tiện lợi."
    },
    "售": {
        "strokes": 11,
        "radical": "口",
        "pinyin": "shòu",
        "meaning": "bán, bán hàng",
        "mnemonic": "Chim nhỏ (chuy 隹) mở miệng (khẩu 口) hót để chào bán hàng."
    },
    "宜": {
        "strokes": 8,
        "radical": "宀",
        "pinyin": "yí",
        "meaning": "thích hợp, vừa phải, rẻ",
        "mnemonic": "Dưới mái nhà (miên 宀) bày đồ thờ (thư thả 且), mọi việc đều tốt đẹp, thích hợp."
    },
    "件": {
        "strokes": 6,
        "radical": "亻",
        "pinyin": "jiàn",
        "meaning": "chiếc, bộ, kiện (quần áo, việc)",
        "mnemonic": "Con người (nhân 亻) dùng sức chia đôi con bò (ngưu 牛) thành từng phần, từng kiện."
    }
}

def main():
    print("=== Cập nhật từ vựng HSK1 Bài 10 ===")

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

    # Filter out existing Lesson 10 words
    filtered_data = [item for item in hsk1_data if str(item.get('lesson')) != '10']

    # Split before lesson 10 and after lesson 10
    before_l10 = [item for item in filtered_data if int(item.get('lesson', 0)) < 10]
    after_l10 = [item for item in filtered_data if int(item.get('lesson', 0)) > 10]

    # Combine: Lessons 1-9, new Lesson 10, then Lessons 11+
    updated_hsk1 = before_l10 + lesson10_words + after_l10

    with open(hsk1_path, 'w', encoding='utf-8') as f:
        json.dump(updated_hsk1, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã lưu {len(updated_hsk1)} từ vựng vào {hsk1_path} (Bài 10: {len(lesson10_words)} từ).")

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
