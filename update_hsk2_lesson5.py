import json
import os

# Lesson 5 vocabulary list (17 words matched with user's 17 sentences)
lesson5_vocab = [
    {
        "hanzi": "快",
        "pinyin": "kuài",
        "meaning": "nhanh, mau",
        "lesson": "5",
        "type": "Tính từ / Phó từ",
        "ex_cn": "你快来看，这个电影很有意思。",
        "ex_py": "Nǐ kuài lái kàn, zhè ge diànyǐng hěn yǒu yìsi.",
        "ex_vn": "Bạn mau đến xem này, bộ phim này rất hay."
    },
    {
        "hanzi": "下来",
        "pinyin": "xiàlái",
        "meaning": "đi xuống, xuống đây",
        "lesson": "5",
        "type": "Động từ",
        "ex_cn": "你快下来，我们在下面等你。",
        "ex_py": "Nǐ kuài xiàlái, wǒmen zài xiàmiàn děng nǐ.",
        "ex_vn": "Bạn mau xuống đây đi, chúng tôi ở dưới chờ bạn."
    },
    {
        "hanzi": "上来",
        "pinyin": "shànglái",
        "meaning": "đi lên, lên đây",
        "lesson": "5",
        "type": "Động từ",
        "ex_cn": "老师在上面，你快上来吧。",
        "ex_py": "Lǎoshī zài shàngmiàn, nǐ kuài shànglái ba.",
        "ex_vn": "Thầy giáo ở bên trên, bạn mau lên đây đi."
    },
    {
        "hanzi": "上去",
        "pinyin": "shàngqù",
        "meaning": "đi lên, lên trên",
        "lesson": "5",
        "type": "Động từ",
        "ex_cn": "我不上去了，在教室门口等你。",
        "ex_py": "Wǒ bú shàngqù le, zài jiàoshì ménkǒu děng nǐ.",
        "ex_vn": "Tôi không đi lên nữa, ở cổng phòng học chờ bạn."
    },
    {
        "hanzi": "下面",
        "pinyin": "xiàmiàn",
        "meaning": "bên dưới, dưới",
        "lesson": "5",
        "type": "Danh từ",
        "ex_cn": "桌子下面有一个黑色的书包。",
        "ex_py": "Zhuōzi xiàmiàn yǒu yí gè hēisè de shūbāo.",
        "ex_vn": "Dưới cái bàn có một chiếc cặp sách màu đen."
    },
    {
        "hanzi": "等",
        "pinyin": "děng",
        "meaning": "đợi, chờ",
        "lesson": "5",
        "type": "Động từ",
        "ex_cn": "请等一下，我去买两杯水。",
        "ex_py": "Qǐng děng yíxià, wǒ qù mǎi liǎng bēi shuǐ.",
        "ex_vn": "Xin đợi một chút, tôi đi mua hai ly nước."
    },
    {
        "hanzi": "一会儿",
        "pinyin": "yíhuìr",
        "meaning": "một lúc, một lát",
        "lesson": "5",
        "type": "Danh từ / Phó từ",
        "ex_cn": "工作太累了，你休息一会儿吧。",
        "ex_py": "Gōngzuò tài lèi le, nǐ xiūxi yíhuìr ba.",
        "ex_vn": "Công việc mệt quá rồi, bạn nghỉ ngơi một lúc đi."
    },
    {
        "hanzi": "下去",
        "pinyin": "xiàqù",
        "meaning": "đi xuống",
        "lesson": "5",
        "type": "Động từ",
        "ex_cn": "我一会儿就下去找你。",
        "ex_py": "Wǒ yíhuìr jiù xiàqù zhǎo nǐ.",
        "ex_vn": "Một lát nữa tôi sẽ đi xuống tìm bạn."
    },
    {
        "hanzi": "进来",
        "pinyin": "jìnlái",
        "meaning": "đi vào, vào đây",
        "lesson": "5",
        "type": "Động từ",
        "ex_cn": "外面很冷，快进来喝杯热茶吧。",
        "ex_py": "Wàimiàn hěn lěng, kuài jìnlái hē bēi rè chá ba.",
        "ex_vn": "Bên ngoài rất lạnh, mau vào đây uống ly trà nóng đi."
    },
    {
        "hanzi": "爷爷",
        "pinyin": "yéye",
        "meaning": "ông nội",
        "lesson": "5",
        "type": "Danh từ",
        "ex_cn": "我爷爷今年七十岁了。",
        "ex_py": "Wǒ yéye jīnián qīshí suì le.",
        "ex_vn": "Ông nội tôi năm nay 70 tuổi rồi."
    },
    {
        "hanzi": "奶奶",
        "pinyin": "nǎinai",
        "meaning": "bà nội",
        "lesson": "5",
        "type": "Danh từ",
        "ex_cn": "我奶奶喜欢喝中国茶。",
        "ex_py": "Wǒ nǎinai xǐhuan hē Zhōngguó chá.",
        "ex_vn": "Bà nội tôi thích uống trà Trung Quốc."
    },
    {
        "hanzi": "礼物",
        "pinyin": "lǐwù",
        "meaning": "món quà, quà",
        "lesson": "5",
        "type": "Danh từ",
        "ex_cn": "这个书包是我送你的生日礼物。",
        "ex_py": "Zhè ge shūbāo shì wǒ sòng nǐ de shēngrì lǐwù.",
        "ex_vn": "Chiếc cặp sách này là món quà sinh nhật tôi tặng bạn."
    },
    {
        "hanzi": "准备",
        "pinyin": "zhǔnbèi",
        "meaning": "chuẩn bị",
        "lesson": "5",
        "type": "Động từ",
        "ex_cn": "这是给孩子们准备的礼物。",
        "ex_py": "Zhè shì gěi háizimen zhǔnbèi de lǐwù.",
        "ex_vn": "Đây là món quà chuẩn bị cho bọn trẻ."
    },
    {
        "hanzi": "奶茶",
        "pinyin": "nǎichá",
        "meaning": "trà sữa",
        "lesson": "5",
        "type": "Danh từ",
        "ex_cn": "我想去买一杯奶茶。",
        "ex_py": "Wǒ xiǎng qù mǎi yì bēi nǎichá.",
        "ex_vn": "Tôi muốn đi mua một ly trà sữa."
    },
    {
        "hanzi": "跟",
        "pinyin": "gēn",
        "meaning": "cùng, với, theo",
        "lesson": "5",
        "type": "Giới từ / Động từ",
        "ex_cn": "我想跟你一起去北京旅游。",
        "ex_py": "Wǒ xiǎng gēn nǐ yìqǐ qù Běijīng lǚyóu.",
        "ex_vn": "Tôi muốn cùng bạn đi Bắc Kinh du lịch."
    },
    {
        "hanzi": "走",
        "pinyin": "zǒu",
        "meaning": "đi, đi bộ",
        "lesson": "5",
        "type": "Động từ",
        "ex_cn": "我们吃完饭是走回酒店的。",
        "ex_py": "Wǒmen chī wán fàn shì zǒu huí jiǔdiàn de.",
        "ex_vn": "Chúng tôi ăn cơm xong là đi bộ về khách sạn."
    },
    {
        "hanzi": "酒店",
        "pinyin": "jiǔdiàn",
        "meaning": "khách sạn",
        "lesson": "5",
        "type": "Danh từ",
        "ex_cn": "这家酒店离车站很近。",
        "ex_py": "Zhè jiā jiǔdiàn lí chēzhàn hěn jìn.",
        "ex_vn": "Khách sạn này cách bến xe rất gần."
    }
]

# Update hsk2_vocab_data.json
hsk2_path = 'hsk2_vocab_data.json'
with open(hsk2_path, 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

# Filter out old lesson 5 items
vocab_data = [item for item in vocab_data if str(item.get('lesson')) != '5']

# Find insertion index (after lesson 4 items)
insert_idx = 0
for idx, item in enumerate(vocab_data):
    if str(item.get('lesson')) == '4':
        insert_idx = idx + 1

# Insert new lesson 5 items
vocab_data[insert_idx:insert_idx] = lesson5_vocab

with open(hsk2_path, 'w', encoding='utf-8') as f:
    json.dump(vocab_data, f, ensure_ascii=False, indent=2)

print(f"Updated {hsk2_path} with {len(lesson5_vocab)} words for Lesson 5.")
