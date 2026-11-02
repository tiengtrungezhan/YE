import json
import os
import subprocess

# 14 vocabulary items for HSK2 Lesson 6
lesson6_vocab = [
    {
        "hanzi": "生日",
        "pinyin": "shēngrì",
        "meaning": "sinh nhật, ngày sinh",
        "lesson": "6",
        "type": "Danh từ",
        "ex_cn": "今天是我的生日。",
        "ex_py": "Jīntiān shì wǒ de shēngrì.",
        "ex_vn": "Hôm nay là sinh nhật của tôi."
    },
    {
        "hanzi": "忘",
        "pinyin": "wàng",
        "meaning": "quên",
        "lesson": "6",
        "type": "Động từ",
        "ex_cn": "我忘了他的名字。",
        "ex_py": "Wǒ wàng le tā de míngzi.",
        "ex_vn": "Tôi quên tên của anh ấy rồi."
    },
    {
        "hanzi": "画",
        "pinyin": "huà",
        "meaning": "vẽ, bức vẽ, tranh",
        "lesson": "6",
        "type": "Động từ / Danh từ",
        "ex_cn": "你在画什么呢？",
        "ex_py": "Nǐ zài huà shénme ne?",
        "ex_vn": "Bạn đang vẽ cái gì thế?"
    },
    {
        "hanzi": "画笔",
        "pinyin": "huàbǐ",
        "meaning": "bút vẽ, cọ vẽ",
        "lesson": "6",
        "type": "Danh từ",
        "ex_cn": "我想买一套新画笔。",
        "ex_py": "Wǒ xiǎng mǎi yí tào xīn huàbǐ.",
        "ex_vn": "Tôi muốn mua một bộ bút vẽ mới."
    },
    {
        "hanzi": "蛋糕",
        "pinyin": "dàngāo",
        "meaning": "bánh ngọt, bánh kem",
        "lesson": "6",
        "type": "Danh từ",
        "ex_cn": "这个生日蛋糕真好吃。",
        "ex_py": "Zhè ge shēngrì dàngāo zhēn hǎochī.",
        "ex_vn": "Chiếc bánh sinh nhật này thật là ngon."
    },
    {
        "hanzi": "快乐",
        "pinyin": "kuàilè",
        "meaning": "vui vẻ, hạnh phúc",
        "lesson": "6",
        "type": "Tính từ",
        "ex_cn": "祝你生日快乐！",
        "ex_py": "Zhù nǐ shēngrì kuàilè!",
        "ex_vn": "Chúc bạn sinh nhật vui vẻ!"
    },
    {
        "hanzi": "打开",
        "pinyin": "dǎkāi",
        "meaning": "mở ra, mở",
        "lesson": "6",
        "type": "Động từ",
        "ex_cn": "请打开门，我想出去。",
        "ex_py": "Qǐng dǎkāi mén, wǒ xiǎng chūqù.",
        "ex_vn": "Xin hãy mở cửa ra, tôi muốn đi ra ngoài."
    },
    {
        "hanzi": "长",
        "pinyin": "cháng",
        "meaning": "dài",
        "lesson": "6",
        "type": "Tính từ",
        "ex_cn": "她的头发很长。",
        "ex_py": "Tā de tóufa hěn cháng.",
        "ex_vn": "Tóc của cô ấy rất dài."
    },
    {
        "hanzi": "鱼",
        "pinyin": "yú",
        "meaning": "cá, con cá",
        "lesson": "6",
        "type": "Danh từ",
        "ex_cn": "我很喜欢吃鱼。",
        "ex_py": "Wǒ hěn xǐhuan chī yú.",
        "ex_vn": "Tôi rất thích ăn cá."
    },
    {
        "hanzi": "肉",
        "pinyin": "ròu",
        "meaning": "thịt",
        "lesson": "6",
        "type": "Danh từ",
        "ex_cn": "我今天不吃肉。",
        "ex_py": "Wǒ jīntiān bù chī ròu.",
        "ex_vn": "Hôm nay tôi không ăn thịt."
    },
    {
        "hanzi": "过",
        "pinyin": "guò",
        "meaning": "đón, trải qua (sinh nhật, ngày lễ)",
        "lesson": "6",
        "type": "Động từ",
        "ex_cn": "你想怎么过生日？",
        "ex_py": "Nǐ xiǎng zěnme guò shēngrì?",
        "ex_vn": "Bạn muốn đón sinh nhật như thế nào?"
    },
    {
        "hanzi": "地",
        "pinyin": "de",
        "meaning": "(trợ từ đứng sau phó từ/tính từ bổ nghĩa cho động từ)",
        "lesson": "6",
        "type": "Trợ từ",
        "ex_cn": "她高兴地笑了。",
        "ex_py": "Tā gāoxìng de xiào le.",
        "ex_vn": "Cô ấy cười một cách vui vẻ."
    },
    {
        "hanzi": "床",
        "pinyin": "chuáng",
        "meaning": "giường, cái giường",
        "lesson": "6",
        "type": "Danh từ",
        "ex_cn": "这张床很大。",
        "ex_py": "Zhè zhāng chuáng hěn dà.",
        "ex_vn": "Chiếc giường này rất to."
    },
    {
        "hanzi": "舒服",
        "pinyin": "shūfu",
        "meaning": "thoải mái, dễ chịu",
        "lesson": "6",
        "type": "Tính từ",
        "ex_cn": "睡在这张床上很舒服。",
        "ex_py": "Shuì zài zhè zhāng chuáng shang hěn shūfu.",
        "ex_vn": "Ngủ trên chiếc giường này rất thoải mái."
    }
]

def main():
    hsk2_path = 'hsk2_vocab_data.json'
    with open(hsk2_path, 'r', encoding='utf-8') as f:
        vocab_data = json.load(f)

    # Filter out old lesson 6 items
    vocab_data = [item for item in vocab_data if str(item.get('lesson')) != '6']

    # Find insertion index (after lesson 5 items)
    insert_idx = 0
    for idx, item in enumerate(vocab_data):
        if str(item.get('lesson')) == '5':
            insert_idx = idx + 1

    # Insert new lesson 6 items
    vocab_data[insert_idx:insert_idx] = lesson6_vocab

    with open(hsk2_path, 'w', encoding='utf-8') as f:
        json.dump(vocab_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã cập nhật {hsk2_path} với {len(lesson6_vocab)} từ vựng HSK 2 Bài 6.")

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

    # Regenerate HSK 2 game pages via generate_hsk2_games.py
    print("🚀 Đang chạy generate_hsk2_games.py...")
    subprocess.run(['python3', 'generate_hsk2_games.py'], check=True)

    # Regenerate via generate_games.py
    print("🚀 Đang chạy generate_games.py cho HSK 2...")
    from generate_games import generate_hsk_games
    generate_hsk_games(2)

    print("🎉 Hoàn tất toàn bộ cập nhật HSK 2 Bài 6!")

if __name__ == '__main__':
    main()
