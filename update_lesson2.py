import json
import os
import subprocess

# 1. Lesson 2 vocabulary list
lesson2_vocab = [
    {
        "hanzi": "公交车",
        "pinyin": "gōngjiāochē",
        "meaning": "xe buýt",
        "lesson": "2",
        "type": "Danh từ",
        "ex_cn": "我坐公交车去学校。",
        "ex_py": "Wǒ zuò gōngjiāochē qù xuéxiào.",
        "ex_vn": "Tôi đi xe buýt đến trường."
    },
    {
        "hanzi": "但",
        "pinyin": "dàn",
        "meaning": "nhưng",
        "lesson": "2",
        "type": "Liên từ",
        "ex_cn": "这个苹果很好吃，但太贵了。",
        "ex_py": "Zhège píngguǒ hěn hǎochī, dàn tài guì le.",
        "ex_vn": "Quả táo này rất ngon, nhưng đắt quá."
    },
    {
        "hanzi": "车站",
        "pinyin": "chēzhàn",
        "meaning": "bến xe, trạm xe",
        "lesson": "2",
        "type": "Danh từ",
        "ex_cn": "我在车站等你。",
        "ex_py": "Wǒ zài chēzhàn děng nǐ.",
        "ex_vn": "Tôi ở trạm xe đợi bạn."
    },
    {
        "hanzi": "远",
        "pinyin": "yuǎn",
        "meaning": "xa",
        "lesson": "2",
        "type": "Tính từ",
        "ex_cn": "我家离学校不远。",
        "ex_py": "Wǒ jiā lí xuéxiào bù yuǎn.",
        "ex_vn": "Nhà tôi cách trường không xa."
    },
    {
        "hanzi": "打车",
        "pinyin": "dǎ chē",
        "meaning": "bắt xe taxi",
        "lesson": "2",
        "type": "Động từ",
        "ex_cn": "今天太冷了，我们打车去饭店吧。",
        "ex_py": "Jīntiān tài lěng le, wǒmen dǎchē qù fàndiàn ba.",
        "ex_vn": "Hôm nay lạnh quá, chúng mình đi taxi đến nhà hàng nhé."
    },
    {
        "hanzi": "还是",
        "pinyin": "háishi",
        "meaning": "hay là / hoặc",
        "lesson": "2",
        "type": "Liên từ",
        "ex_cn": "你想喝茶还是喝水？",
        "ex_py": "Nǐ xiǎng hē chá háishi hē shuǐ?",
        "ex_vn": "Bạn muốn uống trà hay uống nước?"
    },
    {
        "hanzi": "啊",
        "pinyin": "a",
        "meaning": "à, ơi, chao ôi",
        "lesson": "2",
        "type": "Trợ từ",
        "ex_cn": "今天天气真好啊！",
        "ex_py": "Jīntiān tiānqì zhēn hǎo a!",
        "ex_vn": "Thời tiết hôm nay thật là tốt!"
    },
    {
        "hanzi": "万",
        "pinyin": "wàn",
        "meaning": "vạn, mười nghìn",
        "lesson": "2",
        "type": "Số từ",
        "ex_cn": "那个学校有一万名学生。",
        "ex_py": "Nàge xuéxiào yǒu yí wàn míng xuésheng.",
        "ex_vn": "Trường học đó có 10.000 học sinh."
    },
    {
        "hanzi": "名",
        "pinyin": "míng",
        "meaning": "danh, vị (lượng từ chỉ người)",
        "lesson": "2",
        "type": "Lượng từ",
        "ex_cn": "我们学校有三十名老师。",
        "ex_py": "Wǒmen xuéxiào yǒu sānshí míng lǎoshī.",
        "ex_vn": "Trường chúng tôi có 30 giáo viên."
    },
    {
        "hanzi": "网上",
        "pinyin": "wǎngshang",
        "meaning": "trên mạng",
        "lesson": "2",
        "type": "Danh từ",
        "ex_cn": "我在网上买了一本书。",
        "ex_py": "Wǒ zài wǎngshang mǎi le yì běn shū.",
        "ex_vn": "Tôi đã mua một cuốn sách trên mạng."
    },
    {
        "hanzi": "外国",
        "pinyin": "wàiguó",
        "meaning": "nước ngoài",
        "lesson": "2",
        "type": "Danh từ",
        "ex_cn": "他有很多外国朋友。",
        "ex_py": "Tā yǒu hěn duō wàiguó péngyou.",
        "ex_vn": "Anh ấy có rất nhiều bạn nước ngoài."
    },
    {
        "hanzi": "间",
        "pinyin": "jiān",
        "meaning": "gian (lượng từ chỉ phòng, lớp học)",
        "lesson": "2",
        "type": "Lượng từ",
        "ex_cn": "这个学校有二十间教室。",
        "ex_py": "Zhège xuéxiào yǒu èrshí jiān jiàoshì.",
        "ex_vn": "Trường học này có 20 phòng học."
    },
    {
        "hanzi": "教室",
        "pinyin": "jiàoshì",
        "meaning": "phòng học, lớp học",
        "lesson": "2",
        "type": "Danh từ",
        "ex_cn": "老师和学生都在教室里。",
        "ex_py": "Lǎoshī hé xuésheng dōu zài jiàoshì lǐ.",
        "ex_vn": "Thầy giáo và học sinh đều ở trong phòng học."
    },
    {
        "hanzi": "票",
        "pinyin": "piào",
        "meaning": "vé",
        "lesson": "2",
        "type": "Danh từ",
        "ex_cn": "请问，去北京的火车票多少钱？",
        "ex_py": "Qǐngwèn, qù Běijīng de huǒchēpiào duōshao qián?",
        "ex_vn": "Xin hỏi, vé tàu hỏa đi Bắc Kinh bao nhiêu tiền?"
    },
    {
        "hanzi": "别",
        "pinyin": "bié",
        "meaning": "đừng",
        "lesson": "2",
        "type": "Phó từ",
        "ex_cn": "太晚了，你别看电视了。",
        "ex_py": "Tài wǎn le, nǐ bié kàn diànshì le.",
        "ex_vn": "Muộn quá rồi, bạn đừng xem tivi nữa."
    },
    {
        "hanzi": "过来",
        "pinyin": "guòlái",
        "meaning": "qua đây, tới đây",
        "lesson": "2",
        "type": "Động từ",
        "ex_cn": "你过来，我有话对你说。",
        "ex_py": "Nǐ guòlái, wǒ yǒu huà duì nǐ shuō.",
        "ex_vn": "Bạn qua đây, tôi có lời muốn nói với bạn."
    }
]

# Update hsk2_vocab_data.json
hsk2_path = 'hsk2_vocab_data.json'
with open(hsk2_path, 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

# Filter out old lesson 2 items
vocab_data = [item for item in vocab_data if str(item.get('lesson')) != '2']

# Find insertion index (after lesson 1 items)
insert_idx = 0
for idx, item in enumerate(vocab_data):
    if str(item.get('lesson')) == '1':
        insert_idx = idx + 1

# Insert new lesson 2 items
vocab_data[insert_idx:insert_idx] = lesson2_vocab

with open(hsk2_path, 'w', encoding='utf-8') as f:
    json.dump(vocab_data, f, ensure_ascii=False, indent=2)

print(f"Updated {hsk2_path} with {len(lesson2_vocab)} words for Lesson 2.")
