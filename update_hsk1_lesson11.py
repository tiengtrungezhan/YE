import json
import os
import subprocess

# Paths
hsk1_path = 'hsk1_vocab_data.json'
hanzi_details_path = 'hsk1_hanzi_details.json'

# 19 target words for HSK1 Lesson 11
lesson11_words = [
    {
        "hanzi": "时候",
        "pinyin": "shíhou",
        "meaning": "lúc, khi (thời gian)",
        "lesson": "11",
        "type": "danh từ",
        "ex_cn": "弟弟吃饭的时候喜欢玩手机。",
        "ex_py": "Dìdi chī fàn de shíhou xǐhuan wán shǒujī.",
        "ex_vn": "Em trai vừa ăn cơm vừa thích nghịch điện thoại."
    },
    {
        "hanzi": "饭店",
        "pinyin": "fàndiàn",
        "meaning": "nhà hàng, quán ăn, khách sạn",
        "lesson": "11",
        "type": "danh từ",
        "ex_cn": "这个饭店的菜很好吃。",
        "ex_py": "Zhè ge fàndiàn de cài hěn hǎochī.",
        "ex_vn": "Món ăn của nhà hàng này rất ngon."
    },
    {
        "hanzi": "知道",
        "pinyin": "zhīdào",
        "meaning": "biết",
        "lesson": "11",
        "type": "động từ",
        "ex_cn": "你知道他的名字吗？",
        "ex_py": "Nǐ zhīdào tā de míngzi ma?",
        "ex_vn": "Bạn có biết tên của anh ấy không?"
    },
    {
        "hanzi": "正在",
        "pinyin": "zhèngzài",
        "meaning": "đang (chỉ hành động đang diễn ra)",
        "lesson": "11",
        "type": "phó từ",
        "ex_cn": "我正在看书。",
        "ex_py": "Wǒ zhèngzài kàn shū.",
        "ex_vn": "Tôi đang đọc sách."
    },
    {
        "hanzi": "那里",
        "pinyin": "nàli",
        "meaning": "chỗ đó, nơi đó, đằng kia",
        "lesson": "11",
        "type": "đại từ chỉ nơi chốn",
        "ex_cn": "我们去那里吧。",
        "ex_py": "Wǒmen qù nàli ba.",
        "ex_vn": "Chúng ta đến đó đi nhé."
    },
    {
        "hanzi": "找",
        "pinyin": "zhǎo",
        "meaning": "tìm, kiếm",
        "lesson": "11",
        "type": "động từ",
        "ex_cn": "我在找我的手机呢。",
        "ex_py": "Wǒ zài zhǎo wǒ de shǒujī ne.",
        "ex_vn": "Tôi đang tìm điện thoại của mình đây."
    },
    {
        "hanzi": "开车",
        "pinyin": "kāichē",
        "meaning": "lái xe",
        "lesson": "11",
        "type": "động từ",
        "ex_cn": "你会开车吗？",
        "ex_py": "Nǐ huì kāichē ma?",
        "ex_vn": "Bạn biết lái xe không?"
    },
    {
        "hanzi": "读",
        "pinyin": "dú",
        "meaning": "học, theo học (đại học)",
        "lesson": "11",
        "type": "động từ",
        "ex_cn": "我在读大学。",
        "ex_py": "Wǒ zài dú dàxué.",
        "ex_vn": "Tôi đang học đại học."
    },
    {
        "hanzi": "大学",
        "pinyin": "dàxué",
        "meaning": "trường đại học",
        "lesson": "11",
        "type": "danh từ",
        "ex_cn": "你在什么大学学习？",
        "ex_py": "Nǐ zài shénme dàxué xuéxí?",
        "ex_vn": "Bạn đang học ở trường đại học nào?"
    },
    {
        "hanzi": "医",
        "pinyin": "yī",
        "meaning": "y học, ngành y",
        "lesson": "11",
        "type": "danh từ",
        "ex_cn": "我在学医。",
        "ex_py": "Wǒ zài xué yī.",
        "ex_vn": "Tôi đang học y."
    },
    {
        "hanzi": "哪里",
        "pinyin": "nǎli",
        "meaning": "đâu, ở đâu",
        "lesson": "11",
        "type": "đại từ nghi vấn",
        "ex_cn": "你在哪里？",
        "ex_py": "Nǐ zài nǎli?",
        "ex_vn": "Bạn ở đâu vậy?"
    },
    {
        "hanzi": "说",
        "pinyin": "shuō",
        "meaning": "nói",
        "lesson": "11",
        "type": "động từ",
        "ex_cn": "你说什么？",
        "ex_py": "Nǐ shuō shénme?",
        "ex_vn": "Bạn nói gì cơ?"
    },
    {
        "hanzi": "对",
        "pinyin": "duì",
        "meaning": "với, đối với",
        "lesson": "11",
        "type": "giới từ",
        "ex_cn": "医生对你说什么？",
        "ex_py": "Yīshēng duì nǐ shuō shénme?",
        "ex_vn": "Bác sĩ đã nói gì với bạn?"
    },
    {
        "hanzi": "要",
        "pinyin": "yào",
        "meaning": "muốn, cần, phải",
        "lesson": "11",
        "type": "động từ năng nguyện",
        "ex_cn": "我要和小朋友玩儿。",
        "ex_py": "Wǒ yào hé xiǎopéngyou wánr.",
        "ex_vn": "Tôi muốn chơi với các bé nhỏ."
    },
    {
        "hanzi": "大学生",
        "pinyin": "dàxuéshēng",
        "meaning": "sinh viên đại học",
        "lesson": "11",
        "type": "danh từ",
        "ex_cn": "我们都是大学生。",
        "ex_py": "Wǒmen dōu shì dàxuéshēng.",
        "ex_vn": "Chúng tôi đều là sinh viên đại học."
    },
    {
        "hanzi": "起床",
        "pinyin": "qǐchuáng",
        "meaning": "thức dậy, rời giường",
        "lesson": "11",
        "type": "động từ",
        "ex_cn": "弟弟还没起床。",
        "ex_py": "Dìdi hái méi qǐchuáng.",
        "ex_vn": "Em trai vẫn chưa dậy."
    },
    {
        "hanzi": "睡觉",
        "pinyin": "shuìjiào",
        "meaning": "ngủ, đi ngủ",
        "lesson": "11",
        "type": "động từ",
        "ex_cn": "他还在睡觉呢。",
        "ex_py": "Tā hái zài shuìjiào ne.",
        "ex_vn": "Cậu ấy vẫn đang ngủ đấy."
    },
    {
        "hanzi": "睡",
        "pinyin": "shuì",
        "meaning": "ngủ",
        "lesson": "11",
        "type": "động từ",
        "ex_cn": "你睡了吗？",
        "ex_py": "Nǐ shuì le ma?",
        "ex_vn": "Bạn đã ngủ chưa?"
    },
    {
        "hanzi": "小朋友",
        "pinyin": "xiǎopéngyou",
        "meaning": "em nhỏ, bé nhỏ, bạn nhỏ",
        "lesson": "11",
        "type": "danh từ",
        "ex_cn": "我喜欢和小朋友玩儿。",
        "ex_py": "Wǒ xǐhuan hé xiǎopéngyou wánr.",
        "ex_vn": "Tôi thích chơi với các bé nhỏ."
    }
]

# Additional Hanzi details needed for Lesson 11
additional_hanzi_details = {
    "道": {
        "strokes": 12,
        "radical": "辶",
        "pinyin": "dào",
        "meaning": "đường, đạo lý, biết (trong 知道)",
        "mnemonic": "Thủ (đầu 首) đi trên con đường (quai xước 辶), vừa đi vừa suy ngẫm để thấu hiểu đạo lý, tri thức."
    },
    "知": {
        "strokes": 8,
        "radical": "矢",
        "pinyin": "zhī",
        "meaning": "biết, hiểu biết, tri thức",
        "mnemonic": "Lời nói từ miệng (khẩu 口) nhanh và chuẩn xác như mũi tên (thỉ 矢), thể hiện sự hiểu biết sâu sắc."
    },
    "床": {
        "strokes": 7,
        "radical": "广",
        "pinyin": "chuáng",
        "meaning": "giường, cái giường",
        "mnemonic": "Chiếc giường bằng gỗ (mộc 木) đặt dưới mái nhà rộng (quảng 广) để nằm nghỉ ngơi."
    },
    "正": {
        "strokes": 5,
        "radical": "一",
        "pinyin": "zhèng",
        "meaning": "đúng, chính, đang (chỉ hành động đang diễn ra)",
        "mnemonic": "Một (nhất 一) nét dừng (chỉ 止) lại đúng nơi quy định, ngay thẳng chính trực."
    },
    "找": {
        "strokes": 7,
        "radical": "扌",
        "pinyin": "zhǎo",
        "meaning": "tìm kiếm, thối lại (tiền)",
        "mnemonic": "Dùng bàn tay (thủ 扌) cầm vũ khí (qua 戈) đi tìm kiếm mục tiêu."
    }
}

def main():
    print("=== Cập nhật từ vựng HSK1 Bài 11 ===")

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

    # Filter out existing Lesson 11 words
    filtered_data = [item for item in hsk1_data if str(item.get('lesson')) != '11']

    # Split before lesson 11 and after lesson 11
    before_l11 = [item for item in filtered_data if int(item.get('lesson', 0)) < 11]
    after_l11 = [item for item in filtered_data if int(item.get('lesson', 0)) > 11]

    # Combine: Lessons 1-10, new Lesson 11, then Lessons 12+
    updated_hsk1 = before_l11 + lesson11_words + after_l11

    with open(hsk1_path, 'w', encoding='utf-8') as f:
        json.dump(updated_hsk1, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã lưu {len(updated_hsk1)} từ vựng vào {hsk1_path} (Bài 11: {len(lesson11_words)} từ).")

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
