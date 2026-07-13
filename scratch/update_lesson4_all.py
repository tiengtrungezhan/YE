import json
import os

hsk1_path = 'hsk1_vocab_data.json'
with open(hsk1_path, 'r', encoding='utf-8') as f:
    hsk1_data = json.load(f)

# Define target vocabulary details for Lesson 4
lesson4_updates = {
    "有": {
        "hanzi": "有", "pinyin": "yǒu", "meaning": "có", "lesson": "4", "type": "Động từ",
        "ex_cn": "我有三个哥哥。", "ex_py": "Wǒ yǒu sān ge gēge.", "ex_vn": "Tôi có ba người anh trai."
    },
    "多少": {
        "hanzi": "多少", "pinyin": "duōshao", "meaning": "bao nhiêu", "lesson": "4", "type": "Đại từ",
        "ex_cn": "这件衣服多少钱？", "ex_py": "Zhè jiàn yīfu duōshao qián?", "ex_vn": "Chiếc áo này bao nhiêu tiền?"
    },
    "个": {
        "hanzi": "个", "pinyin": "gè", "meaning": "cái", "lesson": "4", "type": "Lượng từ",
        "ex_cn": "我们班有三十个学生。", "ex_py": "Wǒmen bān yǒu sānshí gè xuésheng.", "ex_vn": "Lớp chúng tôi có ba mươi học sinh."
    },
    "零": {
        "hanzi": "零", "pinyin": "líng", "meaning": "số không", "lesson": "4", "type": "Số từ",
        "ex_cn": "今天零度。", "ex_py": "Jīntiān líng dù.", "ex_vn": "Hôm nay không độ."
    },
    "一": {
        "hanzi": "一", "pinyin": "yī", "meaning": "số 1", "lesson": "4", "type": "Số từ",
        "ex_cn": "一、二、三。", "ex_py": "Yī, èr, sān.", "ex_vn": "Một, hai, ba."
    },
    "二": {
        "hanzi": "二", "pinyin": "èr", "meaning": "số 2", "lesson": "4", "type": "Số từ",
        "ex_cn": "一、二、三。", "ex_py": "Yī, èr, sān.", "ex_vn": "Một, hai, ba."
    },
    "三": {
        "hanzi": "三", "pinyin": "sān", "meaning": "ba", "lesson": "4", "type": "Số từ",
        "ex_cn": "一、二、三。", "ex_py": "Yī, èr, sān.", "ex_vn": "Một, hai, ba."
    },
    "四": {
        "hanzi": "四", "pinyin": "sì", "meaning": "bốn", "lesson": "4", "type": "Số từ",
        "ex_cn": "我们家有四口人。", "ex_py": "Wǒmen jiā yǒu sì kǒu rén.", "ex_vn": "Nhà chúng tôi có bốn người."
    },
    "五": {
        "hanzi": "五", "pinyin": "wǔ", "meaning": "năm", "lesson": "4", "type": "Số từ",
        "ex_cn": "他每天五点起床跑步。", "ex_py": "Tā měitiān wǔ diǎn qǐchuáng pǎobù.", "ex_vn": "Mỗi ngày anh ấy thức dậy lúc 5 giờ để chạy bộ."
    },
    "六": {
        "hanzi": "六", "pinyin": "liù", "meaning": "sáu", "lesson": "4", "type": "Số từ",
        "ex_cn": "他今年六岁了。", "ex_py": "Tā jīnnián liù suì le.", "ex_vn": "Năm nay nó sáu tuổi rồi."
    },
    "七": {
        "hanzi": "七", "pinyin": "qī", "meaning": "số 7", "lesson": "4", "type": "Số từ",
        "ex_cn": "他们家有七口人。", "ex_py": "Tāmen jiā yǒu qī kǒu rén.", "ex_vn": "Gia đình họ có bảy người."
    },
    "八": {
        "hanzi": "八", "pinyin": "bā", "meaning": "số 8", "lesson": "4", "type": "Số từ",
        "ex_cn": "他今年八岁，很聪明。", "ex_py": "Tā jīnnián bā suì, hěn cōngming.", "ex_vn": "Năm nay anh ấy tám tuổi, rất thông minh."
    },
    "九": {
        "hanzi": "九", "pinyin": "jiǔ", "meaning": "chín", "lesson": "4", "type": "Số từ",
        "ex_cn": "九月十号是教师节。", "ex_py": "Jiǔyuè shí hào shì Jiàoshījié.", "ex_vn": "Ngày 10 tháng 9 là ngày Nhà giáo."
    },
    "十": {
        "hanzi": "十", "pinyin": "shí", "meaning": "số 10", "lesson": "4", "type": "Số từ",
        "ex_cn": "弟弟今年十岁了。", "ex_py": "Dìdi jīnnián shí suì le.", "ex_vn": "Em trai năm nay mười tuổi rồi."
    },
    "两": {
        "hanzi": "两", "pinyin": "liǎng", "meaning": "hai (dùng trước lượng từ)", "lesson": "4", "type": "Số từ",
        "ex_cn": "我有两个哥哥。", "ex_py": "Wǒ yǒu liǎng gè gēge.", "ex_vn": "Tôi có hai người anh trai."
    },
    "口": {
        "hanzi": "口", "pinyin": "kǒu", "meaning": "người (lượng từ chỉ thành viên gia đình)", "lesson": "4", "type": "Lượng từ",
        "ex_cn": "你家有几口人？", "ex_py": "Nǐ jiā yǒu jǐ kǒu rén?", "ex_vn": "Nhà bạn có mấy người."
    },
    "呢": {
        "hanzi": "呢", "pinyin": "ne", "meaning": "được dùng ở cuối câu hỏi", "lesson": "4", "type": "Trợ từ",
        "ex_cn": "我很好，你呢？", "ex_py": "Wǒ hěn hǎo, nǐ ne?", "ex_vn": "Tôi rất khỏe, còn bạn?"
    },
    "没": {
        "hanzi": "没", "pinyin": "méi", "meaning": "không, chưa", "lesson": "4", "type": "Phó từ",
        "ex_cn": "我没有弟弟。", "ex_py": "Wǒ méiyǒu dìdi.", "ex_vn": "Tôi không có em trai."
    },
    "几": {
        "hanzi": "几", "pinyin": "jǐ", "meaning": "mấy, vài", "lesson": "4", "type": "Đại từ",
        "ex_cn": "你有几个孩子？", "ex_py": "Nǐ yǒu jǐ gè háizi?", "ex_vn": "Bạn có mấy đứa con?"
    },
    "爸爸": {
        "hanzi": "爸爸", "pinyin": "bàba", "meaning": "bố, cha", "lesson": "4", "type": "Danh từ",
        "ex_cn": "他是我爸爸。", "ex_py": "Tā shì wǒ bàba.", "ex_vn": "Anh ấy là bố tôi."
    },
    "妈妈": {
        "hanzi": "妈妈", "pinyin": "māma", "meaning": "mẹ, má", "lesson": "4", "type": "Danh từ",
        "ex_cn": "我妈妈是老师。", "ex_py": "Wǒ māma... wait -> Wǒ māma shì lǎoshī.",
        "ex_cn": "我妈妈是老师。", "ex_py": "Wǒ māma shì lǎoshī.", "ex_vn": "Mẹ tôi là giáo viên."
    },
    "弟弟": {
        "hanzi": "弟弟", "pinyin": "dìdi", "meaning": "em trai", "lesson": "4", "type": "Danh từ",
        "ex_cn": "他是我弟弟。", "ex_py": "Tā shì wǒ dìdi.", "ex_vn": "Cậu ấy là em trai tôi."
    },
    "哥哥": {
        "hanzi": "哥哥", "pinyin": "gēge", "meaning": "anh trai", "lesson": "4", "type": "Danh từ",
        "ex_cn": "Tā shì wǒ gēge.",
        "ex_cn": "他是我哥哥。", "ex_py": "Tā shì wǒ gēge.", "ex_vn": "Anh ấy là anh trai tôi."
    },
    "妹妹": {
        "hanzi": "妹妹", "pinyin": "mèimei", "meaning": "em gái", "lesson": "4", "type": "Danh từ",
        "ex_cn": "我有两个妹妹。", "ex_py": "Wǒ yǒu liǎng gè mèimei.", "ex_vn": "Tôi có hai người em gái."
    },
    "和": {
        "hanzi": "和", "pinyin": "hé", "meaning": "và, với", "lesson": "4", "type": "Liên từ",
        "ex_cn": "爸爸和妈妈都在家。", "ex_py": "Bàba hé māma dōu zài jiā.", "ex_vn": "Bố và mẹ đều ở nhà."
    },
    "儿子": {
        "hanzi": "儿子", "pinyin": "érzi", "meaning": "con trai", "lesson": "4", "type": "Danh từ",
        "ex_cn": "他是我儿子。", "ex_py": "Tā shì wǒ érzi.", "ex_vn": "Nó là con trai tôi."
    },
    "女儿": {
        "hanzi": "女儿", "pinyin": "nǚ'ér", "meaning": "con gái", "lesson": "4", "type": "Danh từ",
        "ex_cn": "她是我女儿。", "ex_py": "Tā shì wǒ nǚ'ér.", "ex_vn": "Con bé là con gái tôi."
    },
    "多大": {
        "hanzi": "多大", "pinyin": "duō dà", "meaning": "bao nhiêu tuổi", "lesson": "4", "type": "Cụm từ",
        "ex_cn": "你女儿今年多大？", "ex_py": "Nǐ nǚ'ér jīnnián duō dà?", "ex_vn": "Con gái bạn năm nay bao nhiêu tuổi?"
    },
    "岁": {
        "hanzi": "岁", "pinyin": "suì", "meaning": "tuổi", "lesson": "4", "type": "Lượng từ",
        "ex_cn": "女儿今年五岁了。", "ex_py": "Nǚ'ér jīnnián wǔ suì le.", "ex_vn": "Con gái năm nay năm tuổi rồi."
    },
    "这": {
        "hanzi": "这", "pinyin": "zhè", "meaning": "đây, này", "lesson": "4", "type": "Đại từ",
        "ex_cn": "这是 my 书 -> 这是我的书。",
        "ex_cn": "这是我的书。", "ex_py": "Zhè shì wǒ de shū.", "ex_vn": "Đây là cuốn sách của tôi."
    },
    "是的": {
        "hanzi": "是的", "pinyin": "shìde", "meaning": "vâng, phải, đúng vậy", "lesson": "4", "type": "Cụm từ",
        "ex_cn": "是的，他是我儿子。", "ex_py": "Shìde, tā shì wǒ érzi.", "ex_vn": "Vâng, nó là con trai tôi."
    },
    "他": {
        "hanzi": "他", "pinyin": "tā", "meaning": "anh ấy, cậu ấy", "lesson": "4", "type": "Đại từ",
        "ex_cn": "他是我的好 phượng -> 他是我的好朋友。",
        "ex_cn": "他是我的好朋友。", "ex_py": "Tā shì wǒ de hǎo péngyou.", "ex_vn": "Cậu ấy là bạn tốt của tôi."
    },
    "今天": {
        "hanzi": "今天", "pinyin": "jīntiān", "meaning": "hôm nay", "lesson": "4", "type": "Danh từ",
        "ex_cn": "今天星期二。", "ex_py": "Jīntiān Xīngqī'èr.", "ex_vn": "Hôm nay là thứ Ba."
    },
    "她": {
        "hanzi": "她", "pinyin": "tā", "meaning": "cô ấy, bà ấy", "lesson": "4", "type": "Đại từ",
        "ex_cn": "她是我的老师。", "ex_py": "Tā shì wǒ de lǎoshī.", "ex_vn": "Cô ấy là giáo viên của tôi."
    }
}

# 1. Update/Add words in hsk1_vocab_data.json
updated_count = 0
added_count = 0

# Check words already in hsk1
for word_hanzi, word_data in lesson4_updates.items():
    found = False
    for item in hsk1_data:
        if item['hanzi'] == word_hanzi:
            print(f"Updating existing word in HSK1: {word_hanzi} (Lesson {item.get('lesson')} -> 4)")
            item.update(word_data)
            found = True
            updated_count += 1
            break
    if not found:
        print(f"Adding new word to HSK1 Lesson 4: {word_hanzi}")
        hsk1_data.append(word_data)
        added_count += 1

# Save back to file
with open(hsk1_path, 'w', encoding='utf-8') as f:
    json.dump(hsk1_data, f, ensure_ascii=False, indent=2)

print(f"\nCompleted updating hsk1_vocab_data.json. Updated: {updated_count}, Added: {added_count}.")

# Verify all target words are indeed in Lesson 4
lesson4_words = [item for item in hsk1_data if item.get('lesson') == '4']
print(f"\nVerification: Lesson 4 now has {len(lesson4_words)} words:")
for item in sorted(lesson4_words, key=lambda x: x['hanzi']):
    print(f"  - {item['hanzi']} ({item['pinyin']}): {item['meaning']} [Lesson: {item['lesson']}]")
