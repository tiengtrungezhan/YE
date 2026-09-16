import json
import os

# Lesson 3 vocabulary list (15 words)
lesson3_vocab = [
    {
        "hanzi": "回来",
        "pinyin": "huílái",
        "meaning": "trở về, về",
        "lesson": "3",
        "type": "Động từ",
        "ex_cn": "爸爸下午五点回来。",
        "ex_py": "Bàba xiàwǔ wǔ diǎn huílái.",
        "ex_vn": "Bố 5 giờ chiều quay về."
    },
    {
        "hanzi": "这么",
        "pinyin": "zhème",
        "meaning": "như thế này, thế này",
        "lesson": "3",
        "type": "Đại từ",
        "ex_cn": "今天回来这么晚啊！",
        "ex_py": "Jīntiān huílái zhème wǎn a!",
        "ex_vn": "Hôm nay về muộn thế này à!"
    },
    {
        "hanzi": "完",
        "pinyin": "wán",
        "meaning": "xong, hết",
        "lesson": "3",
        "type": "Động từ",
        "ex_cn": "工作太多了，下班的时候没做完。",
        "ex_py": "Gōngzuò tài duō le, xiàbān de shíhou méi zuò wán.",
        "ex_vn": "Công việc nhiều quá, lúc tan làm chưa làm xong."
    },
    {
        "hanzi": "一起",
        "pinyin": "yìqǐ",
        "meaning": "cùng nhau",
        "lesson": "3",
        "type": "Phó từ",
        "ex_cn": "我和朋友一起去商店。",
        "ex_py": "Wǒ hé péngyou yìqǐ qù shāngdiàn.",
        "ex_vn": "Tôi cùng bạn đi đến cửa hàng."
    },
    {
        "hanzi": "出去",
        "pinyin": "chūqù",
        "meaning": "đi ra ngoài",
        "lesson": "3",
        "type": "Động từ",
        "ex_cn": "今天天气不好，别出去了。",
        "ex_py": "Jīntiān tiānqì bù hǎo, bié chūqù le.",
        "ex_vn": "Hôm nay thời tiết không tốt, đừng đi ra ngoài nữa."
    },
    {
        "hanzi": "洗",
        "pinyin": "xǐ",
        "meaning": "rửa, giặt",
        "lesson": "3",
        "type": "Động từ",
        "ex_cn": "我去洗洗手。",
        "ex_py": "Wǒ qù xǐxǐ shǒu.",
        "ex_vn": "Tôi đi rửa tay một chút."
    },
    {
        "hanzi": "自己",
        "pinyin": "zìjǐ",
        "meaning": "bản thân, tự mình",
        "lesson": "3",
        "type": "Đại từ",
        "ex_cn": "这是我自己做的中国菜。",
        "ex_py": "Zhè shì wǒ zìjǐ zuò de Zhōngguócài.",
        "ex_vn": "Đây là món ăn Trung Quốc do tự tay tôi làm."
    },
    {
        "hanzi": "拿",
        "pinyin": "ná",
        "meaning": "cầm, lấy",
        "lesson": "3",
        "type": "Động từ",
        "ex_cn": "请拿桌子上的水喝。",
        "ex_py": "Qǐng ná zhuōzi shang de shuǐ hē.",
        "ex_vn": "Xin hãy lấy nước trên bàn uống."
    },
    {
        "hanzi": "手",
        "pinyin": "shǒu",
        "meaning": "tay",
        "lesson": "3",
        "type": "Danh từ",
        "ex_cn": "吃苹果前要洗手。",
        "ex_py": "Chī píngguǒ qián yào xǐ shǒu.",
        "ex_vn": "Trước khi ăn táo cần rửa tay."
    },
    {
        "hanzi": "为什么",
        "pinyin": "wèishénme",
        "meaning": "tại sao",
        "lesson": "3",
        "type": "Đại từ",
        "ex_cn": "你今天为什么没去学校？",
        "ex_py": "Nǐ jīntiān wèishénme méi qù xuéxiào?",
        "ex_vn": "Hôm nay tại sao bạn không đi học?"
    },
    {
        "hanzi": "不错",
        "pinyin": "búcuò",
        "meaning": "không tồi, khá tốt",
        "lesson": "3",
        "type": "Tính từ",
        "ex_cn": "这家饭店的菜很不错。",
        "ex_py": "Zhè jiā fàndiàn de cài hěn búcuò.",
        "ex_vn": "Món ăn của nhà hàng này rất khá."
    },
    {
        "hanzi": "送",
        "pinyin": "sòng",
        "meaning": "tặng, tiễn",
        "lesson": "3",
        "type": "Động từ",
        "ex_cn": "我送你一个大苹果。",
        "ex_py": "Wǒ sòng nǐ yí gè dà píngguǒ.",
        "ex_vn": "Tôi tặng bạn một quả táo lớn."
    },
    {
        "hanzi": "回去",
        "pinyin": "huíqù",
        "meaning": "đi về",
        "lesson": "3",
        "type": "Động từ",
        "ex_cn": "太晚了，我想回去了。",
        "ex_py": "Tài wǎn le, wǒ xiǎng huíqù le.",
        "ex_vn": "Muộn quá rồi, tôi muốn đi về rồi."
    },
    {
        "hanzi": "每",
        "pinyin": "měi",
        "meaning": "mỗi",
        "lesson": "3",
        "type": "Đại từ",
        "ex_cn": "我每天早上喝一杯牛奶。",
        "ex_py": "Wǒ měitiān zǎoshang hē yì bēi niúnǎi.",
        "ex_vn": "Tôi mỗi sáng uống một ly sữa tươi."
    },
    {
        "hanzi": "累",
        "pinyin": "lèi",
        "meaning": "mệt",
        "lesson": "3",
        "type": "Tính từ",
        "ex_cn": "我觉得他这个月每天都很累。",
        "ex_py": "Wǒ juéde tā zhè ge yuè měitiān dōu hěn lèi.",
        "ex_vn": "Tôi cảm thấy tháng này ngày nào anh ấy cũng rất mệt."
    }
]

# Update hsk2_vocab_data.json
hsk2_path = 'hsk2_vocab_data.json'
with open(hsk2_path, 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

# Filter out old lesson 3 items
vocab_data = [item for item in vocab_data if str(item.get('lesson')) != '3']

# Find insertion index (after lesson 2 items)
insert_idx = 0
for idx, item in enumerate(vocab_data):
    if str(item.get('lesson')) == '2':
        insert_idx = idx + 1

# Insert new lesson 3 items
vocab_data[insert_idx:insert_idx] = lesson3_vocab

with open(hsk2_path, 'w', encoding='utf-8') as f:
    json.dump(vocab_data, f, ensure_ascii=False, indent=2)

print(f"Updated {hsk2_path} with {len(lesson3_vocab)} words for Lesson 3.")
