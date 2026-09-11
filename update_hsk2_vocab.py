import json
import os
import re

# 1. Prepare exact Lesson 1 vocabulary
lesson1_vocab = [
    {
        "hanzi": "就",
        "pinyin": "jiù",
        "meaning": "thì, liền, chính",
        "lesson": "1",
        "type": "Phó từ",
        "ex_cn": "好的，那我给你打电话。",
        "ex_py": "Hǎo de, nà wǒ gěi nǐ dǎ diànhuà.",
        "ex_vn": "Được, vậy tôi sẽ gọi điện cho bạn."
    },
    {
        "hanzi": "给",
        "pinyin": "gěi",
        "meaning": "cho, đưa cho",
        "lesson": "1",
        "type": "Giới từ",
        "ex_cn": "她还给我们介绍了很多东西。",
        "ex_py": "Tā hái gěi wǒmen jièshào le hěn duō dōngxi.",
        "ex_vn": "Cô ấy còn giới thiệu cho chúng tôi rất nhiều thứ."
    },
    {
        "hanzi": "让",
        "pinyin": "ràng",
        "meaning": "bảo, để, nhường, cho phép",
        "lesson": "1",
        "type": "Động từ",
        "ex_cn": "她让我来接你们。",
        "ex_py": "Tā ràng wǒ lái jiē nǐmen.",
        "ex_vn": "Cô ấy bảo tôi đến đón các bạn."
    },
    {
        "hanzi": "接",
        "pinyin": "jiē",
        "meaning": "đón, nhận, nghe (điện thoại)",
        "lesson": "1",
        "type": "Động từ",
        "ex_cn": "不好意思，我接个电话。",
        "ex_py": "Bù hǎoyìsi, wǒ jiē gè diànhuà.",
        "ex_vn": "Ngại quá, tôi nghe một cuộc điện thoại."
    },
    {
        "hanzi": "次",
        "pinyin": "cì",
        "meaning": "lần",
        "lesson": "1",
        "type": "Lượng từ",
        "ex_cn": "你们是第一次来北京吗？",
        "ex_py": "Nǐmen shì dì yī cì lái Běijīng ma?",
        "ex_vn": "Các bạn là lần đầu tiên đến Bắc Kinh à?"
    },
    {
        "hanzi": "旅游",
        "pinyin": "lǚyóu",
        "meaning": "du lịch",
        "lesson": "1",
        "type": "Động từ",
        "ex_cn": "我们是来旅游的。",
        "ex_py": "Wǒmen shì lái lǚyóu de.",
        "ex_vn": "Chúng tôi đến để đi du lịch."
    },
    {
        "hanzi": "帮忙",
        "pinyin": "bāngmáng",
        "meaning": "giúp đỡ, giúp một tay",
        "lesson": "1",
        "type": "Động từ",
        "ex_cn": "我想请你帮个忙。",
        "ex_py": "Wǒ xiǎng qǐng nǐ bāng gè máng.",
        "ex_vn": "Tôi muốn nhờ bạn giúp một việc."
    },
    {
        "hanzi": "不好意思",
        "pinyin": "bù hǎoyìsi",
        "meaning": "ngại quá, xin lỗi",
        "lesson": "1",
        "type": "Cụm từ",
        "ex_cn": "不好意思，我接个电话。",
        "ex_py": "Bù hǎoyìsi, wǒ jiē gè diànhuà.",
        "ex_vn": "Ngại quá, tôi nghe một cuộc điện thoại."
    },
    {
        "hanzi": "已经",
        "pinyin": "yǐjīng",
        "meaning": "đã... rồi",
        "lesson": "1",
        "type": "Phó từ",
        "ex_cn": "我已经到北京了。",
        "ex_py": "Wǒ yǐjīng dào Běijīng le.",
        "ex_vn": "Tôi đã đến Bắc Kinh rồi."
    },
    {
        "hanzi": "那",
        "pinyin": "nà",
        "meaning": "thế thì, vậy thì",
        "lesson": "1",
        "type": "Liên từ",
        "ex_cn": "好的，那我给你打电话。",
        "ex_py": "Hǎo de, nà wǒ gěi nǐ dǎ diànhuà.",
        "ex_vn": "Được, vậy tôi sẽ gọi điện cho bạn."
    },
    {
        "hanzi": "介绍",
        "pinyin": "jièshào",
        "meaning": "giới thiệu",
        "lesson": "1",
        "type": "Động từ",
        "ex_cn": "她还给我们介绍了很多东西。",
        "ex_py": "Tā hái gěi wǒmen jièshào le hěn duō dōngxi.",
        "ex_vn": "Cô ấy còn giới thiệu cho chúng tôi rất nhiều thứ."
    },
    {
        "hanzi": "有时",
        "pinyin": "yǒushí",
        "meaning": "thỉnh thoảng, có lúc",
        "lesson": "1",
        "type": "Phó từ",
        "ex_cn": "我有时不太懂她的意思。",
        "ex_py": "Wǒ yǒushí bú tài dǒng tā de yìsi.",
        "ex_vn": "Thỉnh thoảng tôi không hiểu lắm ý của cô ấy."
    },
    {
        "hanzi": "懂",
        "pinyin": "dǒng",
        "meaning": "hiểu",
        "lesson": "1",
        "type": "Động từ",
        "ex_cn": "我有时不太懂她的意思。",
        "ex_py": "Wǒ yǒushí bú tài dǒng tā de yìsi.",
        "ex_vn": "Thỉnh thoảng tôi không hiểu lắm ý của cô ấy."
    },
    {
        "hanzi": "意思",
        "pinyin": "yìsi",
        "meaning": "ý nghĩa, ý",
        "lesson": "1",
        "type": "Danh từ",
        "ex_cn": "我有时不太懂她的意思。",
        "ex_py": "Wǒ yǒushí bú tài dǒng tā de yìsi.",
        "ex_vn": "Thỉnh thoảng tôi không hiểu lắm ý của cô ấy."
    },
    {
        "hanzi": "北京烤鸭",
        "pinyin": "Běijīng kǎoyā",
        "meaning": "vịt quay Bắc Kinh",
        "lesson": "1",
        "type": "Danh từ",
        "ex_cn": "她请我们吃了北京烤鸭。",
        "ex_py": "Tā qǐng wǒmen chī le Běijīng kǎoyā.",
        "ex_vn": "Cô ấy mời chúng tôi ăn vịt quay Bắc Kinh."
    }
]

# Load current HSK2 vocab
with open('hsk2_vocab_data.json', 'r', encoding='utf-8') as f:
    hsk2_data = json.load(f)

# Filter out old lesson 1, replace with new lesson 1
hsk2_data = [item for item in hsk2_data if str(item.get('lesson')) != '1']
hsk2_data = lesson1_vocab + hsk2_data

with open('hsk2_vocab_data.json', 'w', encoding='utf-8') as f:
    json.dump(hsk2_data, f, ensure_ascii=False, indent=2)

print("Updated hsk2_vocab_data.json for Lesson 1.")
