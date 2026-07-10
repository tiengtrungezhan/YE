import json

with open('hsk1_vocab_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Words to move to lesson 3 (currently in other lessons)
# Format: hanzi -> new lesson
move_to_3 = {
    '那': '3',   # currently lesson 6
    '也': '3',   # currently lesson 2
    '是': '3',   # currently lesson 2
    '的': '3',   # currently lesson 6
    '朋友': '3', # currently lesson 9
    '工作': '3', # currently lesson 8
    '人': '3',   # currently lesson 12
    '谁': '3',   # currently lesson 10
    '汉语': '3', # currently lesson 14
}

# Update lesson for existing words
for item in data:
    if item['hanzi'] in move_to_3:
        print(f"Moving {item['hanzi']} from lesson {item.get('lesson', 'N/A')} to lesson 3")
        item['lesson'] = '3'

# New words to add to lesson 3
new_words = [
    {
        "hanzi": "越南",
        "pinyin": "Yuènán",
        "meaning": "Việt Nam",
        "lesson": "3",
        "type": "Danh từ",
        "ex_cn": "我是越南人。",
        "ex_py": "Wǒ shì Yuènán rén.",
        "ex_vn": "Tôi là người Việt Nam."
    },
    {
        "hanzi": "英国",
        "pinyin": "Yīngguó",
        "meaning": "Anh (quốc)",
        "lesson": "3",
        "type": "Danh từ",
        "ex_cn": "他是英国人。",
        "ex_py": "Tā shì Yīngguó rén.",
        "ex_vn": "Anh ấy là người Anh."
    },
    {
        "hanzi": "美国",
        "pinyin": "Měiguó",
        "meaning": "Mỹ",
        "lesson": "3",
        "type": "Danh từ",
        "ex_cn": "她来自美国。",
        "ex_py": "Tā láizì Měiguó.",
        "ex_vn": "Cô ấy đến từ Mỹ."
    },
    {
        "hanzi": "日本",
        "pinyin": "Rìběn",
        "meaning": "Nhật Bản",
        "lesson": "3",
        "type": "Danh từ",
        "ex_cn": "日本在中国旁边。",
        "ex_py": "Rìběn zài Zhōngguó pángbiān.",
        "ex_vn": "Nhật Bản ở cạnh Trung Quốc."
    },
    {
        "hanzi": "朋友",
        "pinyin": "péngyou",
        "meaning": "bạn bè",
        "lesson": "3",
        "type": "Danh từ",
        "ex_cn": "他是我的好朋友。",
        "ex_py": "Tā shì wǒ de hǎo péngyou.",
        "ex_vn": "Anh ấy là người bạn tốt của tôi."
    } if not any(d['hanzi'] == '朋友' for d in data) else None,
    {
        "hanzi": "女朋友",
        "pinyin": "nǚpéngyou",
        "meaning": "bạn gái",
        "lesson": "3",
        "type": "Danh từ",
        "ex_cn": "她是我的女朋友。",
        "ex_py": "Tā shì wǒ de nǚpéngyou.",
        "ex_vn": "Cô ấy là bạn gái của tôi."
    },
    {
        "hanzi": "男朋友",
        "pinyin": "nánpéngyou",
        "meaning": "bạn trai",
        "lesson": "3",
        "type": "Danh từ",
        "ex_cn": "他是我的男朋友。",
        "ex_py": "Tā shì wǒ de nánpéngyou.",
        "ex_vn": "Anh ấy là bạn trai của tôi."
    },
    {
        "hanzi": "哪",
        "pinyin": "nǎ",
        "meaning": "nào, đâu",
        "lesson": "3",
        "type": "Đại từ",
        "ex_cn": "你是哪国人？",
        "ex_py": "Nǐ shì nǎ guó rén?",
        "ex_vn": "Bạn là người nước nào?"
    },
    {
        "hanzi": "吗",
        "pinyin": "ma",
        "meaning": "không? (trợ từ câu hỏi)",
        "lesson": "3",
        "type": "Trợ từ",
        "ex_cn": "你是学生吗？",
        "ex_py": "Nǐ shì xuésheng ma?",
        "ex_vn": "Bạn có phải là học sinh không?"
    },
    {
        "hanzi": "是",
        "pinyin": "shì",
        "meaning": "là",
        "lesson": "3",
        "type": "Động từ",
        "ex_cn": "我是越南人。",
        "ex_py": "Wǒ shì Yuènán rén.",
        "ex_vn": "Tôi là người Việt Nam."
    } if not any(d['hanzi'] == '是' for d in data) else None,
    {
        "hanzi": "她",
        "pinyin": "tā",
        "meaning": "cô ấy, bà ấy",
        "lesson": "3",
        "type": "Đại từ",
        "ex_cn": "她是我的老师。",
        "ex_py": "Tā shì wǒ de lǎoshī.",
        "ex_vn": "Cô ấy là giáo viên của tôi."
    },
    {
        "hanzi": "姐姐",
        "pinyin": "jiějie",
        "meaning": "chị gái",
        "lesson": "3",
        "type": "Danh từ",
        "ex_cn": "我有一个姐姐。",
        "ex_py": "Wǒ yǒu yí gè jiějie.",
        "ex_vn": "Tôi có một người chị gái."
    },
    {
        "hanzi": "忙",
        "pinyin": "máng",
        "meaning": "bận",
        "lesson": "3",
        "type": "Tính từ",
        "ex_cn": "你今天忙吗？",
        "ex_py": "Nǐ jīntiān máng ma?",
        "ex_vn": "Hôm nay bạn có bận không?"
    },
    {
        "hanzi": "还",
        "pinyin": "hái",
        "meaning": "vẫn còn, cũng",
        "lesson": "3",
        "type": "Phó từ",
        "ex_cn": "她还在工作。",
        "ex_py": "Tā hái zài gōngzuò.",
        "ex_vn": "Cô ấy vẫn còn đang làm việc."
    },
    {
        "hanzi": "太",
        "pinyin": "tài",
        "meaning": "quá, rất",
        "lesson": "3",
        "type": "Phó từ",
        "ex_cn": "你太忙了。",
        "ex_py": "Nǐ tài máng le.",
        "ex_vn": "Bạn bận quá."
    },
]

# Filter out None entries (words that already existed and were moved)
new_words = [w for w in new_words if w is not None]

# Check which new words don't already exist in data
existing_hanzi = {item['hanzi'] for item in data}
words_to_add = []
for w in new_words:
    if w['hanzi'] not in existing_hanzi:
        print(f"Adding new word: {w['hanzi']}")
        words_to_add.append(w)
    else:
        print(f"Word already exists (will be moved): {w['hanzi']}")

data.extend(words_to_add)

# Save updated data
with open('hsk1_vocab_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ Done! Updated hsk1_vocab_data.json")

# Verify lesson 3 words
lesson3 = [item for item in data if item.get('lesson') == '3']
print(f"\nLesson 3 now has {len(lesson3)} words:")
for item in lesson3:
    print(f"  - {item['hanzi']} ({item['pinyin']}): {item['meaning']}")
