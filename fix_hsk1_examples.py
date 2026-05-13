import json

with open('hsk1_vocab_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def fix(hanzi, lesson, ex_cn, ex_py, ex_vn):
    for item in data:
        if item['hanzi'] == hanzi and str(item['lesson']) == str(lesson):
            item['ex_cn'] = ex_cn
            item['ex_py'] = ex_py
            item['ex_vn'] = ex_vn
            print(f"  ✓ L{lesson} {hanzi}: {ex_cn}")
            return True
    print(f"  ✗ NOT FOUND: L{lesson} {hanzi}")
    return False

print("=== Sửa nốt các ví dụ còn ngắn ===")

fix("我", "1",
    "我是越南留学生，在中国学习汉语。",
    "Wǒ shì Yuènán liúxuéshēng, zài Zhōngguó xuéxí Hànyǔ.",
    "Tôi là lưu học sinh Việt Nam, đang học tiếng Trung ở Trung Quốc.")

fix("是", "3",
    "他是我们班的学生，很努力。",
    "Tā shì wǒmen bān de xuésheng, hěn nǔlì.",
    "Anh ấy là học sinh lớp chúng tôi, rất chăm chỉ.")

fix("医生", "3",
    "他是医生，每天在医院工作。",
    "Tā shì yīshēng, měitiān zài yīyuàn gōngzuò.",
    "Anh ấy là bác sĩ, mỗi ngày làm việc ở bệnh viện.")

fix("职员", "3",
    "他是公司职员，每天坐地铁上班。",
    "Tā shì gōngsī zhíyuán, měitiān zuò dìtiě shàngbān.",
    "Anh ấy là nhân viên công ty, mỗi ngày đi tàu điện ngầm đi làm.")

fix("米饭", "8",
    "我每天中午都吃米饭，不吃面包。",
    "Wǒ měitiān zhōngwǔ dōu chī mǐfàn, bù chī miànbāo.",
    "Mỗi buổi trưa tôi đều ăn cơm, không ăn bánh mì.")

fix("冷", "12",
    "今天天气很冷，我穿了厚厚的外套。",
    "Jīntiān tiānqì hěn lěng, wǒ chuān le hòu hòu de wàitào.",
    "Hôm nay trời rất lạnh, tôi mặc áo khoác dày.")

fix("热", "12",
    "今天天气很热，我们去游泳吧。",
    "Jīntiān tiānqì hěn rè, wǒmen qù yóuyǒng ba.",
    "Hôm nay trời rất nóng, chúng ta đi bơi đi.")

fix("水", "12",
    "他运动以后喝了很多水。",
    "Tā yùndòng yǐhòu hē le hěn duō shuǐ.",
    "Sau khi tập thể dục, anh ấy uống rất nhiều nước.")

fix("下雨", "12",
    "今天下雨了，我没有带伞，全身都湿了。",
    "Jīntiān xià yǔ le, wǒ méiyǒu dài sǎn, quánshēn dōu shī le.",
    "Hôm nay trời mưa, tôi không mang ô nên ướt hết cả người.")

fix("小姐", "12",
    "那位小姐是我们学校的老师。",
    "Nà wèi xiǎojiě shì wǒmen xuéxiào de lǎoshī.",
    "Cô gái đó là giáo viên trường chúng tôi.")

fix("桌子", "12",
    "这张桌子是新买的，很漂亮。",
    "Zhè zhāng zhuōzi shì xīn mǎi de, hěn piàoliang.",
    "Chiếc bàn này mới mua, rất đẹp.")

print("\n=== Lưu file ===")
with open('hsk1_vocab_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"✅ Saved! Total words: {len(data)}")
