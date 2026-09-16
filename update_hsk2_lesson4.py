import json
import os

# Lesson 4 vocabulary list (16 words)
lesson4_vocab = [
    {
        "hanzi": "过",
        "pinyin": "guò",
        "meaning": "qua, từng",
        "lesson": "4",
        "type": "Động từ / Trợ từ",
        "ex_cn": "我们来过这家商场吗？",
        "ex_py": "Wǒmen lái guò zhè jiā shāngchǎng ma?",
        "ex_vn": "Chúng ta từng đến trung tâm thương mại này chưa?"
    },
    {
        "hanzi": "商场",
        "pinyin": "shāngchǎng",
        "meaning": "trung tâm thương mại",
        "lesson": "4",
        "type": "Danh từ",
        "ex_cn": "我和朋友一起去商场买衣服。",
        "ex_py": "Wǒ hé péngyou yìqǐ qù shāngchǎng mǎi yīfu.",
        "ex_vn": "Tôi cùng bạn đi trung tâm thương mại mua quần áo."
    },
    {
        "hanzi": "进去",
        "pinyin": "jìnqù",
        "meaning": "đi vào",
        "lesson": "4",
        "type": "Động từ",
        "ex_cn": "老师在教室里，我们进去吧。",
        "ex_py": "Lǎoshī zài jiàoshì lǐ, wǒmen jìnqù ba.",
        "ex_vn": "Thầy giáo đang ở trong phòng học, chúng ta đi vào đi."
    },
    {
        "hanzi": "条",
        "pinyin": "tiáo",
        "meaning": "chiếc, cái (lượng từ chỉ quần, sông...)",
        "lesson": "4",
        "type": "Lượng từ",
        "ex_cn": "我想买条裤子。",
        "ex_py": "Wǒ xiǎng mǎi tiáo kùzi.",
        "ex_vn": "Tôi muốn mua một chiếc quần."
    },
    {
        "hanzi": "裤子",
        "pinyin": "kùzi",
        "meaning": "quần",
        "lesson": "4",
        "type": "Danh từ",
        "ex_cn": "这条黑色的裤子很漂亮。",
        "ex_py": "Zhè tiáo hēisè de kùzi hěn piàoliang.",
        "ex_vn": "Chiếc quần màu đen này rất đẹp."
    },
    {
        "hanzi": "白色",
        "pinyin": "báisè",
        "meaning": "màu trắng",
        "lesson": "4",
        "type": "Danh từ",
        "ex_cn": "我喜欢白色的衣服。",
        "ex_py": "Wǒ xǐhuan báisè de yīfu.",
        "ex_vn": "Tôi thích quần áo màu trắng."
    },
    {
        "hanzi": "因为",
        "pinyin": "yīnwèi",
        "meaning": "bởi vì",
        "lesson": "4",
        "type": "Liên từ",
        "ex_cn": "因为今天太累了，所以我想早点儿回家。",
        "ex_py": "Yīnwèi jīntiān tài lèi le, suǒyǐ wǒ xiǎng zǎodiǎnr huí jiā.",
        "ex_vn": "Bởi vì hôm nay quá mệt, cho nên tôi muốn về nhà sớm một chút."
    },
    {
        "hanzi": "试",
        "pinyin": "shì",
        "meaning": "thử",
        "lesson": "4",
        "type": "Động từ",
        "ex_cn": "你试试那条红色的吧。",
        "ex_py": "Nǐ shìshi nà tiáo hóngsè de ba.",
        "ex_vn": "Bạn thử chiếc màu đỏ kia đi."
    },
    {
        "hanzi": "红色",
        "pinyin": "hóngsè",
        "meaning": "màu đỏ",
        "lesson": "4",
        "type": "Danh từ",
        "ex_cn": "桌子上有两个红色的苹果。",
        "ex_py": "Zhuōzi shang yǒu liǎng gè hóngsè de píngguǒ.",
        "ex_vn": "Trên bàn có hai quả táo màu đỏ."
    },
    {
        "hanzi": "所以",
        "pinyin": "suǒyǐ",
        "meaning": "cho nên",
        "lesson": "4",
        "type": "Liên từ",
        "ex_cn": "因为今天太冷了，所以我们打车去吧。",
        "ex_py": "Yīnwèi jīntiān tài lěng le, suǒyǐ wǒmen dǎchē qù ba.",
        "ex_vn": "Bởi vì hôm nay quá lạnh, cho nên chúng mình đi taxi đi."
    },
    {
        "hanzi": "书包",
        "pinyin": "shūbāo",
        "meaning": "cặp sách, ba lô",
        "lesson": "4",
        "type": "Danh từ",
        "ex_cn": "我想买个新书包。",
        "ex_py": "Wǒ xiǎng mǎi gè xīn shūbāo.",
        "ex_vn": "Tôi muốn mua một chiếc cặp sách mới."
    },
    {
        "hanzi": "过去",
        "pinyin": "guòqù",
        "meaning": "đi qua",
        "lesson": "4",
        "type": "Động từ",
        "ex_cn": "朋友在那边，我们过去吧。",
        "ex_py": "Péngyou zài nàbiān, wǒmen guòqù ba.",
        "ex_vn": "Bạn bè ở đằng kia, chúng ta qua đó đi."
    },
    {
        "hanzi": "绿色",
        "pinyin": "lǜsè",
        "meaning": "màu xanh lá",
        "lesson": "4",
        "type": "Danh từ",
        "ex_cn": "我喜欢绿色的书包。",
        "ex_py": "Wǒ xǐhuan lǜsè de shūbāo.",
        "ex_vn": "Tôi thích chiếc cặp sách màu xanh lá."
    },
    {
        "hanzi": "黑色",
        "pinyin": "hēisè",
        "meaning": "màu đen",
        "lesson": "4",
        "type": "Danh từ",
        "ex_cn": "红色的、绿色的、黑色的，你想买哪个？",
        "ex_py": "Hóngsè de, lǜsè de, hēisè de, nǐ xiǎng mǎi nǎ gè?",
        "ex_vn": "Màu đỏ, màu xanh lá, màu đen, bạn muốn mua cái nào?"
    },
    {
        "hanzi": "更",
        "pinyin": "gèng",
        "meaning": "càng, hơn",
        "lesson": "4",
        "type": "Phó từ",
        "ex_cn": "我也觉得绿色的更好看。",
        "ex_py": "Wǒ yě juéde lǜsè de gèng hǎokàn.",
        "ex_vn": "Tôi cũng cảm thấy màu xanh lá đẹp hơn."
    },
    {
        "hanzi": "颜色",
        "pinyin": "yánsè",
        "meaning": "màu sắc",
        "lesson": "4",
        "type": "Danh từ",
        "ex_cn": "你喜欢什么颜色的衣服？",
        "ex_py": "Nǐ xǐhuan shénme yánsè de yīfu?",
        "ex_vn": "Bạn thích quần áo màu gì?"
    }
]

# Update hsk2_vocab_data.json
hsk2_path = 'hsk2_vocab_data.json'
with open(hsk2_path, 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

# Filter out old lesson 4 items
vocab_data = [item for item in vocab_data if str(item.get('lesson')) != '4']

# Find insertion index (after lesson 3 items)
insert_idx = 0
for idx, item in enumerate(vocab_data):
    if str(item.get('lesson')) == '3':
        insert_idx = idx + 1

# Insert new lesson 4 items
vocab_data[insert_idx:insert_idx] = lesson4_vocab

with open(hsk2_path, 'w', encoding='utf-8') as f:
    json.dump(vocab_data, f, ensure_ascii=False, indent=2)

print(f"Updated {hsk2_path} with {len(lesson4_vocab)} words for Lesson 4.")
