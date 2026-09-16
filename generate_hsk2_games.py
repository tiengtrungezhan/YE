import json
import os
import re

# Load vocabulary
with open('hsk2_vocab_data.json', 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

# Group by lesson
lessons = {}
for item in vocab_data:
    l_id = int(item['lesson'])
    if l_id not in lessons:
        lessons[l_id] = []
    lessons[l_id].append(item)

# Radical dictionary
RADICAL_DICT = {
    "丨": "Cổn (sổ thẳng)", "丿": "Phiệt (nét phẩy)", "人": "Nhân (người)", "亻": "Nhân (người)",
    "口": "Khẩu (miệng)", "宀": "Miên (mái nhà)", "日": "Nhật (mặt trời/ngày)", "木": "Mộc (cây)",
    "水": "Thủy (nước)", "氵": "Thủy (nước)", "言": "Ngôn (nói/lời nói)", "讠": "Ngôn (nói/lời nói)",
    "门": "Môn (cửa)", "心": "Tâm (tim/lòng)", "忄": "Tâm (tim/lòng)", "禾": "Hòa (lúa)",
    "女": "Nữ (con gái/phụ nữ)", "贝": "Bối (tiền vỏ sò/bảo bối)", "囗": "Vi (bao quanh)",
    "八": "Bát (số tám)", "走": "Tẩu (đi/chạy)", "戈": "Qua (vũ khí)", "羊": "Dương (con cừu)",
    "大": "Đại (to lớn)", "彳": "Xích (bước chân trái)", "乙": "Ất", "耳": "Nhĩ (tai)",
    "目": "Mục (mắt)", "王": "Vương (vua)", "力": "Lực (sức mạnh)", "月": "Nguyệt (mặt trăng/tháng)",
    "火": "Hỏa (lửa)", "灬": "Hỏa (lửa)", "土": "Thổ (đất)", "寸": "Thốn (tấc)",
    "食": "Thực (ăn)", "饣": "Thực (ăn)", "犬": "Khuyển (con chó)", "犭": "Khuyển (con chó)",
    "父": "Phụ (cha)", "手": "Thủ (tay)", "扌": "Thủ (tay)", "糸": "Mịch (tơ lụa)",
    "纟": "Mịch (tơ lụa)", "辵": "Sước (đi)", "辶": "Sước (đi)", "艸": "Thảo (cỏ)",
    "艹": "Thảo (cỏ)", "竹": "Trúc (tre)", "⺮": "Trúc (tre)", "雨": "Vũ (mưa)",
    "自": "Tự (bản thân)", "足": "Túc (chân)", "车": "Xa (xe)", "衣": "Y (áo)",
    "衤": "Y (áo)", "广": "Quảng (mái che)", "疒": "Nạch (bệnh)", "皿": "Mãnh (đồ đựng)",
    "石": "Thạch (đá)", "示": "Thị (mách bảo)", "礻": "Thị (mách bảo)", "穴": "Huyệt (hang)",
    "立": "Lập (đứng)", "皮": "Bì (da)", "矢": "Thỉ (mũi tên)", "肉": "Nhục (thịt)",
    "舌": "Thiệt (lưỡi)", "舟": "Chu (thuyền)", "虫": "Trùng (sâu bọ)", "血": "Huyết (máu)",
    "行": "Hành (đi)", "见": "Kiến (nhìn)", "角": "Giác (sừng)", "身": "Thân (thân thể)",
    "辛": "Tân (cay)", "酉": "Dậu (rượu)", "里": "Lý (dặm)", "长": "Trường (dài)",
    "风": "Phong (gió)", "飞": "Phi (bay)", "首": "Thủ (đầu)", "香": "Hương (thơm)",
    "马": "Mã (ngựa)", "高": "Cao (cao)", "鱼": "Ngư (cá)", "鸟": "Điểu (chim)",
    "黄": "Hoàng (vàng)", "黑": "Hắc (đen)", "鼻": "Tị (mũi)", "一": "Nhất (một)",
    "丶": "Chủ (chấm)", "二": "Nhị (hai)", "亠": "Đầu (nắp)", "儿": "Nhân (chân)",
    "几": "Kỷ (bàn nhỏ)", "刀": "Đao (dao)", "刂": "Đao (dao)", "十": "Thập (mười)",
    "又": "Hựu (lại)", "子": "Tử (con)", "小": "Tiểu (nhỏ)", "工": "Công (thợ)",
    "巾": "Cân (khăn)", "干": "Can", "弓": "Cung (cung)", "方": "Phương (hướng)",
    "白": "Bạch (trắng)"
}

def get_hanzi_details_dict(vocab_list):
    seen_chars = set()
    details = {}
    
    hsk1_details = {}
    if os.path.exists('hsk1_hanzi_details.json'):
        with open('hsk1_hanzi_details.json', 'r', encoding='utf-8') as f:
            hsk1_details = json.load(f)
            
    for item in vocab_list:
        for char in item['hanzi']:
            if '\u4e00' <= char <= '\u9fff' and char not in seen_chars:
                seen_chars.add(char)
                if char in hsk1_details:
                    details[char] = hsk1_details[char]
                else:
                    strokes = 6
                    radical = "一"
                    if char in "你好他她们您": radical = "亻"; strokes = 7 if char == "你" else (6 if char in "她好" else 5)
                    elif char in "就": radical = "亠"; strokes = 12
                    elif char in "给": radical = "纟"; strokes = 9
                    elif char in "让": radical = "讠"; strokes = 5
                    elif char in "接": radical = "扌"; strokes = 11
                    elif char in "次": radical = "欠"; strokes = 6
                    elif char in "旅": radical = "方"; strokes = 10
                    elif char in "游": radical = "氵"; strokes = 12
                    elif char in "帮": radical = "巾"; strokes = 9
                    elif char in "忙": radical = "忄"; strokes = 6
                    elif char in "意": radical = "心"; strokes = 13
                    elif char in "思": radical = "心"; strokes = 9
                    elif char in "已": radical = "己"; strokes = 3
                    elif char in "经": radical = "纟"; strokes = 8
                    elif char in "那": radical = "阝"; strokes = 6
                    elif char in "介": radical = "人"; strokes = 4
                    elif char in "绍": radical = "纟"; strokes = 8
                    elif char in "有": radical = "月"; strokes = 6
                    elif char in "时": radical = "日"; strokes = 7
                    elif char in "懂": radical = "忄"; strokes = 15
                    elif char in "北": radical = "匕"; strokes = 5
                    elif char in "京": radical = "亠"; strokes = 8
                    elif char in "烤": radical = "火"; strokes = 10
                    elif char in "鸭": radical = "鸟"; strokes = 10
                    elif char in "病": radical = "疒"; strokes = 10
                    elif char in "跑": radical = "足"; strokes = 12
                    elif char in "步": radical = "止"; strokes = 7
                    elif char in "唱": radical = "口"; strokes = 11
                    elif char in "歌": radical = "欠"; strokes = 14
                    elif char in "舞": radical = "夕"; strokes = 14
                    elif char in "房": radical = "户"; strokes = 8
                    elif char in "间": radical = "门"; strokes = 7
                    elif char in "公": radical = "八"; strokes = 4
                    elif char in "交": radical = "亠"; strokes = 6
                    elif char in "车": radical = "车"; strokes = 4
                    elif char in "但": radical = "亻"; strokes = 7
                    elif char in "站": radical = "立"; strokes = 10
                    elif char in "远": radical = "辶"; strokes = 7
                    elif char in "打": radical = "扌"; strokes = 5
                    elif char in "还": radical = "辶"; strokes = 7
                    elif char in "啊": radical = "口"; strokes = 10
                    elif char in "万": radical = "一"; strokes = 3
                    elif char in "名": radical = "口"; strokes = 6
                    elif char in "网": radical = "冂"; strokes = 6
                    elif char in "国": radical = "囗"; strokes = 8
                    elif char in "教": radical = "攵"; strokes = 11
                    elif char in "室": radical = "宀"; strokes = 9
                    elif char in "票": radical = "示"; strokes = 11
                    elif char in "别": radical = "刂"; strokes = 7
                    elif char in "过": radical = "辶"; strokes = 6

                    details[char] = {
                        "strokes": strokes,
                        "radical": radical,
                        "pinyin": "",
                        "meaning": f"Chữ Hán: {char}",
                        "mnemonic": f"Quan sát thứ tự nét và kết cấu của chữ {char} để ghi nhớ lâu hơn."
                    }
    return details

def get_lesson_sentences(lesson_id, vocab_list):
    if lesson_id == 1:
        return [
            {
                "cn": "她让我来接你们。",
                "vn": "Cô ấy bảo tôi đến đón các bạn.",
                "phrases": ["她", "让", "我", "来接", "你们。"]
            },
            {
                "cn": "你们是第一次来北京吗？",
                "vn": "Các bạn là lần đầu tiên đến Bắc Kinh à?",
                "phrases": ["你们", "是", "第一次", "来北京", "吗？"]
            },
            {
                "cn": "我们是来旅游的。",
                "vn": "Chúng tôi đến để đi du lịch.",
                "phrases": ["我们", "是", "来", "旅游的。"]
            },
            {
                "cn": "我想请你帮个忙。",
                "vn": "Tôi muốn nhờ bạn giúp một việc.",
                "phrases": ["我", "想请你", "帮个忙。"]
            },
            {
                "cn": "不好意思，我接个电话。",
                "vn": "Ngại quá, tôi nghe một cuộc điện thoại.",
                "phrases": ["不好意思，", "我", "接个", "电话。"]
            },
            {
                "cn": "我已经到北京了。",
                "vn": "Tôi đã đến Bắc Kinh rồi.",
                "phrases": ["我", "已经", "到", "北京了。"]
            },
            {
                "cn": "好的，那我给你打电话。",
                "vn": "Được, vậy tôi sẽ gọi điện cho bạn.",
                "phrases": ["好的，", "那", "我给你", "打电话。"]
            },
            {
                "cn": "她还给我们介绍了很多东西。",
                "vn": "Cô ấy còn giới thiệu cho chúng tôi rất nhiều thứ.",
                "phrases": ["她还", "给我们", "介绍了", "很多东西。"]
            },
            {
                "cn": "我有时不太懂她的意思。",
                "vn": "Thỉnh thoảng tôi không hiểu lắm ý của cô ấy.",
                "phrases": ["我", "有时", "不太懂", "她的意思。"]
            },
            {
                "cn": "她请我们吃了北京烤鸭。",
                "vn": "Cô ấy mời chúng tôi ăn vịt quay Bắc Kinh.",
                "phrases": ["她请", "我们", "吃了", "北京烤鸭。"]
            }
        ]
    if lesson_id == 2:
        return [
            {
                "cn": "我坐公交车去学校。",
                "vn": "Tôi đi xe buýt đến trường.",
                "phrases": ["我", "坐公交车", "去", "学校。"]
            },
            {
                "cn": "这个苹果很好吃，但太贵了。",
                "vn": "Quả táo này rất ngon, nhưng đắt quá.",
                "phrases": ["这个苹果", "很好吃，", "但", "太贵了。"]
            },
            {
                "cn": "我在车站等你。",
                "vn": "Tôi ở trạm xe đợi bạn.",
                "phrases": ["我", "在车站", "等你。"]
            },
            {
                "cn": "我家离学校不远。",
                "vn": "Nhà tôi cách trường không xa.",
                "phrases": ["我家", "离学校", "不远。"]
            },
            {
                "cn": "今天太冷了，我们打车去饭店吧。",
                "vn": "Hôm nay lạnh quá, chúng mình đi taxi đến nhà hàng nhé.",
                "phrases": ["今天太冷了，", "我们", "打车去", "饭店吧。"]
            },
            {
                "cn": "你想喝茶还是喝水？",
                "vn": "Bạn muốn uống trà hay uống nước?",
                "phrases": ["你想", "喝茶", "还是", "喝水？"]
            },
            {
                "cn": "今天天气真好啊！",
                "vn": "Thời tiết hôm nay thật là tốt!",
                "phrases": ["今天天气", "真好啊！"]
            },
            {
                "cn": "那个学校有一万名学生。",
                "vn": "Trường học đó có một vạn (10.000) học sinh.",
                "phrases": ["那个学校", "有", "一万名", "学生。"]
            },
            {
                "cn": "我们学校有三十名老师。",
                "vn": "Trường chúng tôi có ba mươi giáo viên.",
                "phrases": ["我们学校", "有", "三十名", "老师。"]
            },
            {
                "cn": "我在网上买了一本书。",
                "vn": "Tôi đã mua một cuốn sách trên mạng.",
                "phrases": ["我", "在网上", "买了一本书。"]
            },
            {
                "cn": "他有很多外国朋友。",
                "vn": "Anh ấy có rất nhiều bạn nước ngoài.",
                "phrases": ["他", "有很多", "外国朋友。"]
            },
            {
                "cn": "这个学校有二十间教室。",
                "vn": "Trường học này có hai mươi phòng học.",
                "phrases": ["这个学校", "有", "二十间", "教室。"]
            },
            {
                "cn": "老师和学生都在教室里。",
                "vn": "Thầy giáo và học sinh đều ở trong phòng học.",
                "phrases": ["老师和学生", "都在", "教室里。"]
            },
            {
                "cn": "请问，去北京的火车票多少钱？",
                "vn": "Xin hỏi, vé tàu hỏa đi Bắc Kinh bao nhiêu tiền?",
                "phrases": ["请问，", "去北京的", "火车票", "多少钱？"]
            },
            {
                "cn": "太晚了，你别看电视了。",
                "vn": "Muộn quá rồi, bạn đừng xem tivi nữa.",
                "phrases": ["太晚了，", "你", "别看电视了。"]
            },
            {
                "cn": "你过来，我有话对你说。",
                "vn": "Bạn qua đây, tôi có lời muốn nói với bạn.",
                "phrases": ["你过来，", "我有话", "对你说。"]
            }
        ]
    
    s_list = []
    for item in vocab_list:
        cn = item.get('ex_cn', '')
        vn = item.get('ex_vn', '')
        if cn and vn:
            clean_cn = cn.replace(' ', '')
            length = len(clean_cn)
            if length <= 6:
                phrases = [clean_cn[:2], clean_cn[2:]]
            elif length <= 10:
                phrases = [clean_cn[:3], clean_cn[3:6], clean_cn[6:]]
            else:
                phrases = [clean_cn[:3], clean_cn[3:7], clean_cn[7:11], clean_cn[11:]]
            phrases = [p for p in phrases if p]
            s_list.append({
                "cn": clean_cn,
                "vn": vn,
                "phrases": phrases
            })
    
    idx = 0
    while len(s_list) < 10:
        base = s_list[idx % len(s_list)] if s_list else {"cn": "我喜欢学习汉语。", "vn": "Tôi thích học tiếng Trung.", "phrases": ["我", "喜欢", "学习", "汉语。"]}
        s_list.append(base)
        idx += 1
        
    return s_list[:10]

FLIP_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lật Thẻ Thông Minh - HSK 2 3.0 Bài {lesson_id}</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        body {{ background: #f0f9ff; }}
        .game-header {{ text-align: center; margin-bottom: 2rem; position: relative; }}
        .mascot-container {{ position: absolute; right: 0; top: -20px; width: 100px; animation: bounce 2s infinite ease-in-out; }}
        @keyframes bounce {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
        .mascot-bubble {{ background: white; padding: 10px 15px; border-radius: 20px; box-shadow: var(--shadow); font-size: 0.85rem; position: absolute; right: 110px; top: 10px; width: 150px; color: var(--primary-dark); font-weight: 700; z-index: 10; }}
        .game-container {{ max-width: 1100px; margin: 0 auto; padding: 2rem; }}
        .single-card-container {{ display: flex; justify-content: center; align-items: center; margin-top: 2rem; position: relative; }}
        .flip-card {{ background-color: transparent; width: 100%; max-width: 500px; height: 500px; perspective: 1000px; cursor: pointer; }}
        .flip-card-inner {{ position: relative; width: 100%; height: 100%; text-align: center; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); transform-style: preserve-3d; }}
        .flip-card.flipped .flip-card-inner {{ transform: rotateY(180deg); }}
        .flip-card-front, .flip-card-back {{ position: absolute; width: 100%; height: 100%; backface-visibility: hidden; display: flex; flex-direction: column; border-radius: 30px; padding: 1.2rem; border: 2px solid var(--primary-light); background: white; box-shadow: 0 10px 30px rgba(165, 207, 218, 0.2); }}
        .flip-card-front {{ justify-content: center; align-items: center; }}
        .flip-card-front .hanzi {{ font-family: "KaiTi", "楷体", "STKaiti", serif; font-size: 6.5rem; font-weight: 800; color: var(--primary-dark); transition: transform 0.3s; word-break: break-all; text-align: center; }}
        .flip-card:hover .hanzi {{ transform: scale(1.05); }}
        .flip-card-back {{ transform: rotateY(180deg); text-align: left; background: #fff; border-color: var(--primary-color); }}
        .flip-card.mastered .flip-card-front, .flip-card.mastered .flip-card-back {{ border-color: #ffd700; background: #fffdf0; }}
        .master-badge {{ position: absolute; top: 15px; right: 15px; font-size: 1.5rem; display: none; z-index: 5; }}
        .flip-card.mastered .master-badge {{ display: block; animation: pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); }}
        @keyframes pop {{ from {{ transform: scale(0); }} to {{ transform: scale(1); }} }}
        .back-header {{ width: 100%; display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid #eee; padding-bottom: 0.5rem; }}
        .back-hanzi {{ font-family: "KaiTi", "楷体", "STKaiti", serif; font-size: 2.5rem; font-weight: 800; color: var(--primary-dark); }}
        .back-pinyin {{ font-size: 1.6rem; color: #e67e22; font-weight: 700; }}
        .btn-speak {{ background: var(--primary-light); border: none; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; transition: 0.3s; }}
        .btn-speak:hover {{ background: var(--primary-color); transform: scale(1.1); }}
        .back-meaning {{ font-size: 1.5rem; font-weight: 700; color: #444; }}
        .back-example {{ font-size: 1.1rem; background: #f9f9f9; padding: 1rem; border-radius: 12px; margin-top: 1rem; line-height: 1.5; }}
        .back-example strong {{ font-size: 1.1rem; color: var(--primary-dark); }}
        .master-btn {{ margin-top: auto; width: 100%; padding: 0.6rem; border-radius: 12px; border: 2px solid var(--primary-color); background: white; color: var(--primary-dark); font-weight: 800; cursor: pointer; transition: 0.3s; font-size: 0.85rem; }}
        .master-btn.active {{ background: var(--primary-color); color: white; }}
        .progress-container {{ background: white; padding: 1.5rem; border-radius: 20px; box-shadow: var(--shadow); margin: 2rem 0; }}
        .progress-text {{ display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-weight: 700; color: #555; }}
        .progress-bar {{ width: 100%; height: 12px; background: #eee; border-radius: 10px; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, var(--primary-color), var(--primary-dark)); width: 0%; transition: width 0.5s ease-out; }}
        .controls {{ display: flex; justify-content: center; gap: 1rem; margin-top: 1rem; }}
        .btn-control {{ padding: 0.5rem 1rem; border-radius: 10px; border: 1px solid var(--primary-color); background: white; color: var(--primary-dark); font-weight: 700; cursor: pointer; transition: 0.3s; font-size: 0.9rem; }}
        .celebration-overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255,255,255,0.95); z-index: 2000; display: none; flex-direction: column; align-items: center; justify-content: center; animation: fadeIn 0.5s; }}
        .trophy {{ font-size: 5rem; animation: trophyPop 1s infinite alternate; }}
        @keyframes trophyPop {{ from {{ transform: scale(1); }} to {{ transform: scale(1.2) rotate(5deg); }} }}
    </style>
</head>
<body>
    <a href="index.html" class="home-logo-btn">
        <img src="mascot.png" alt="Home">
    </a>
    <div class="page-container">
        <a href="game-hsk2.html" class="back-btn">← Quay lại danh sách bài</a>
        <header class="game-header">
            <h1 style="color: var(--primary-dark); font-size: 2.2rem;">Lật Thẻ Thông Minh - HSK 2 3.0 Bài {lesson_id}</h1>
            <div class="mascot-container">
                <div class="mascot-bubble" id="mascotSpeech">Cùng mình bắt đầu học nhé! 🐼</div>
                <img src="mascot-guide.png" style="width: 100%; mix-blend-mode: multiply;" alt="Mascot">
            </div>
        </header>

        <div class="progress-container">
            <div class="progress-text"><span>Tiến độ học tập</span><span id="progressPercent">0%</span></div>
            <div class="progress-bar"><div class="progress-fill" id="progress"></div></div>
            <div class="stats-info" style="margin-top:0.5rem">Bạn đã thuộc <span id="masteredCount">0</span> / <span id="totalCount">0</span> từ</div>
            <div class="controls">
                <button class="btn-control" onclick="shuffleCards()">🔀 Trộn thẻ</button>
                <button class="btn-control" onclick="resetProgress()">🔄 Học lại</button>
            </div>
        </div>
        <div class="single-card-container" id="cardGrid"></div>
        <div class="card-navigation" style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem; align-items: center;">
            <button class="btn-control" onclick="prevCard()" style="font-size: 1.2rem; padding: 0.8rem 1.5rem;">⬅ Trước</button>
            <span id="cardCounter" style="font-size: 1.2rem; font-weight: bold; color: var(--text-color);">1 / 10</span>
            <button class="btn-control" onclick="nextCard()" style="font-size: 1.2rem; padding: 0.8rem 1.5rem;">Sau ➡</button>
        </div>
    </div>

    <div class="celebration-overlay" id="celebration">
        <div class="trophy">🏆</div>
        <h2 style="font-size: 2rem; color: var(--primary-dark); margin: 1rem 0;">TUYỆT VỜI!</h2>
        <p>Bạn đã làm chủ hoàn toàn bài học này!</p>
        <button class="btn-control" style="margin-top: 2rem; padding: 1rem 2rem; background: var(--primary-color); color: white;" onclick="document.getElementById('celebration').style.display='none'">Tiếp tục luyện tập</button>
    </div>

    <script>
        let vocabData = {vocab_json};
        const grid = document.getElementById('cardGrid');
        const progressFill = document.getElementById('progress');
        const progressPercent = document.getElementById('progressPercent');
        const masteredCountEl = document.getElementById('masteredCount');
        const totalCountEl = document.getElementById('totalCount');
        const mascotSpeech = document.getElementById('mascotSpeech');
        const celebration = document.getElementById('celebration');

        let masteredSet = new Set();
        let currentCardIndex = 0;
        const cardCounterEl = document.getElementById('cardCounter');
        totalCountEl.innerText = vocabData.length;

        function renderCards() {{
            grid.innerHTML = '';
            if(vocabData.length === 0) return;
            const index = currentCardIndex;
            const word = vocabData[index];
            const card = document.createElement('div');
            card.className = 'flip-card' + (masteredSet.has(index) ? ' mastered' : '');
            card.innerHTML = `
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <div class="master-badge">⭐</div>
                        <div class="hanzi">${{word.hanzi}}</div>
                    </div>
                    <div class="flip-card-back">
                        <div class="back-header">
                            <span class="back-hanzi">${{word.hanzi}}</span>
                            <span class="back-pinyin">${{word.pinyin}}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 0.5rem;">
                            <button class="btn-speak" onclick="event.stopPropagation(); speak('${{word.hanzi}}')">🔊</button>
                            <div class="back-meaning">${{word.meaning}}</div>
                        </div>
                        <div style="font-size: 1.1rem; color: #555; margin-bottom: 1rem; padding-left: 5px;">
                            <strong>Từ loại:</strong> ${{word.type || word.pos || 'Đang cập nhật'}}
                        </div>
                        <div class="back-example">
                            <strong>Ví dụ:</strong>
                            <div style="font-family: 'KaiTi', '楷体', 'STKaiti', serif; margin-top:5px; font-size: 1.5rem;">${{word.ex_cn || word.hanzi}}</div>
                            <div style="color: #e67e22; font-style: italic; font-size: 1.2rem;">${{word.ex_py || word.pinyin}}</div>
                            <div style="color: #666; font-size: 1.1rem; border-top: 1px dashed #ccc; margin-top:5px; padding-top:5px;">${{word.ex_vn || word.meaning}}</div>
                        </div>
                        <button class="master-btn ${{masteredSet.has(index) ? 'active' : ''}}" onclick="event.stopPropagation(); toggleMaster(${{index}}, this)">
                            ${{masteredSet.has(index) ? 'Bỏ thuộc' : 'Đã thuộc'}}
                        </button>
                    </div>
                </div>`;
            card.addEventListener('click', () => card.classList.toggle('flipped'));
            grid.appendChild(card);
            cardCounterEl.innerText = (currentCardIndex + 1) + " / " + vocabData.length;
        }}

        window.prevCard = function() {{
            if(currentCardIndex > 0) {{
                currentCardIndex--;
                renderCards();
            }}
        }};

        window.nextCard = function() {{
            if(currentCardIndex < vocabData.length - 1) {{
                currentCardIndex++;
                renderCards();
            }}
        }};

        function speak(text) {{
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'zh-CN';
            utterance.rate = 0.8;
            window.speechSynthesis.speak(utterance);
        }}

        function updateProgress() {{
            const count = masteredSet.size;
            const percent = Math.round((count / vocabData.length) * 100);
            progressFill.style.width = percent + '%';
            progressPercent.innerText = percent + '%';
            masteredCountEl.innerText = count;

            if (percent === 100) {{
                mascotSpeech.innerText = "Tuyệt vời! Bạn đã thuộc hết rồi! 🏆";
                celebration.style.display = 'flex';
            }} else if (percent >= 50) mascotSpeech.innerText = "Sắp xong rồi, bạn học nhanh quá! 🚀";
            else if (percent > 0) mascotSpeech.innerText = "Giỏi lắm! Cố gắng lên nhé! 💪";
        }}

        window.toggleMaster = function(index, btn) {{
            if (masteredSet.has(index)) {{
                masteredSet.delete(index);
            }} else {{
                masteredSet.add(index);
            }}
            renderCards();
            updateProgress();
        }};

        window.shuffleCards = function() {{
            vocabData.sort(() => Math.random() - 0.5);
            masteredSet.clear();
            currentCardIndex = 0;
            renderCards();
            updateProgress();
        }};

        window.resetProgress = function() {{
            masteredSet.clear();
            currentCardIndex = 0;
            renderCards();
            updateProgress();
        }};

        renderCards();
    </script>
</body>
</html>"""

HANZI_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luyện Chữ Hán - HSK 2 3.0 Bài {lesson_id}</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3.5/dist/hanzi-writer.min.js"></script>
    <style>
        body {{ background: #f0f7f9; }}
        .game-wrapper {{ display: flex; gap: 2rem; max-width: 1000px; margin: 2rem auto; align-items: flex-start; }}
        .char-sidebar {{ flex: 0 0 180px; background: var(--white); border-radius: 25px; padding: 1.5rem; box-shadow: var(--shadow); max-height: 550px; overflow-y: auto; display: flex; flex-direction: column; gap: 0.8rem; }}
        .sidebar-title {{ font-size: 0.9rem; font-weight: bold; color: var(--primary-dark); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; text-align: center; border-bottom: 2px solid var(--primary-light); padding-bottom: 0.5rem; }}
        .char-btn {{ padding: 0.8rem; background: #f8fbfe; border: 2px solid #eef2f5; border-radius: 15px; font-size: 1.6rem; font-family: "KaiTi", "楷体", "STKaiti", serif; font-weight: bold; color: var(--text-color); cursor: pointer; transition: var(--transition); display: flex; align-items: center; justify-content: center; gap: 0.8rem; }}
        .char-btn span {{ font-size: 0.9rem; font-family: Arial, sans-serif; font-weight: normal; color: #666; }}
        .char-btn:hover {{ border-color: var(--primary-color); background: #f0f7f9; transform: translateY(-2px); }}
        .char-btn.active {{ background: var(--primary-color); border-color: var(--primary-color); color: white; }}
        .char-btn.active span {{ color: #fff; }}
        .char-panel {{ flex: 1; background: var(--white); border-radius: 30px; padding: 3rem; box-shadow: var(--shadow); display: flex; gap: 3rem; min-height: 550px; }}
        .writer-section {{ display: flex; flex-direction: column; align-items: center; gap: 1.5rem; flex: 0 0 250px; }}
        .hanzi-writer-container {{ width: 250px; height: 250px; background: #fff; border: 3px solid var(--primary-light); border-radius: 20px; position: relative; box-shadow: 0 10px 25px rgba(165,207,218,0.15); background-image: linear-gradient(to right, #f5f5f5 1px, transparent 1px), linear-gradient(to bottom, #f5f5f5 1px, transparent 1px), linear-gradient(to right, transparent 50%, #ffe3e3 1px, transparent 50%), linear-gradient(to bottom, transparent 50%, #ffe3e3 1px, transparent 50%); background-size: 25px 25px, 25px 25px, 100% 100%, 100% 100%; }}
        .control-buttons {{ display: flex; flex-direction: column; gap: 0.8rem; width: 100%; }}
        .btn-control {{ padding: 0.8rem 1.5rem; border-radius: 12px; border: 2px solid var(--primary-color); background: white; color: var(--primary-dark); font-weight: bold; font-size: 0.95rem; cursor: pointer; transition: var(--transition); display: flex; align-items: center; justify-content: center; gap: 0.5rem; }}
        .btn-control:hover {{ background: var(--primary-color); color: white; transform: translateY(-2px); }}
        .btn-speak-big {{ background: #f0f7f9; border-color: var(--primary-color); }}
        .details-section {{ flex: 1; display: flex; flex-direction: column; gap: 1.5rem; }}
        .char-header {{ border-bottom: 2px dashed var(--primary-light); padding-bottom: 1rem; }}
        .char-pinyin-display {{ font-size: 2rem; font-weight: bold; color: #e67e22; }}
        .char-meaning-display {{ font-size: 1.3rem; font-weight: bold; color: var(--text-color); margin-top: 0.3rem; }}
        .pills-container {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
        .info-pill {{ background: #f0f9ff; color: var(--text-color); padding: 0.6rem 1.2rem; border-radius: 100px; font-size: 0.95rem; border: 1px solid var(--primary-light); display: flex; gap: 0.5rem; }}
        .info-pill strong {{ color: var(--primary-dark); }}
        .mnemonic-box {{ background: #fffdf0; border: 1px solid #ffeeba; border-radius: 20px; padding: 1.5rem; margin-top: auto; position: relative; }}
        .mnemonic-title {{ font-weight: bold; color: #d48806; margin-bottom: 0.5rem; font-size: 1.1rem; display: flex; align-items: center; gap: 0.5rem; }}
        .mnemonic-content {{ font-size: 1.05rem; line-height: 1.6; color: #555; }}
        .toast {{ position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(100px); background: #28a745; color: white; padding: 1rem 2rem; border-radius: 50px; font-weight: bold; box-shadow: 0 10px 25px rgba(40,167,69,0.3); z-index: 1000; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s; opacity: 0; pointer-events: none; }}
        .toast.show {{ transform: translateX(-50%) translateY(0); opacity: 1; }}
        @media (max-width: 768px) {{ .game-wrapper {{ flex-direction: column; padding: 1rem; }} .char-sidebar {{ flex: 1; width: 100%; max-height: 120px; flex-direction: row; overflow-x: auto; padding: 1rem; }} .sidebar-title {{ display: none; }} .char-btn {{ flex-shrink: 0; min-width: 80px; }} .char-panel {{ flex-direction: column; padding: 2rem; width: 100%; gap: 2rem; }} .writer-section {{ width: 100%; flex: none; }} }}
    </style>
</head>
<body>
    <a href="index.html" class="home-logo-btn"><img src="mascot.png" alt="Home"></a>
    <div class="page-container">
        <a href="game-hsk2.html" class="back-btn">← Quay lại danh sách bài</a>
        <h1 style="text-align: center; color: var(--primary-dark); font-size: 2.2rem; margin-bottom: 1rem;">Luyện Chữ Hán HSK 2 3.0 Bài {lesson_id} ✍️</h1>
        <p style="text-align: center; margin-bottom: 2rem; opacity: 0.8;">Học cách viết, số nét, bộ thủ và mẹo nhớ từng chữ Hán trong bài.</p>
        <div class="game-wrapper">
            <div class="char-sidebar" id="charSidebar"><div class="sidebar-title">Chữ Hán</div></div>
            <div class="char-panel">
                <div class="writer-section">
                    <div id="character-target-div" class="hanzi-writer-container"></div>
                    <div class="control-buttons">
                        <button class="btn-control" onclick="animateChar()">▶ Xem viết</button>
                        <button class="btn-control" onclick="startPractice()">✏ Viết thử</button>
                        <button class="btn-control btn-speak-big" onclick="speakChar()">🔊 Phát âm</button>
                    </div>
                </div>
                <div class="details-section">
                    <div class="char-header">
                        <span class="char-pinyin-display" id="char-pinyin"></span>
                        <div class="char-meaning-display" id="char-meaning"></div>
                    </div>
                    <div class="pills-container">
                        <div class="info-pill"><strong>Bộ thủ:</strong> <span id="char-radical">丨</span></div>
                        <div class="info-pill"><strong>Số nét:</strong> <span id="char-strokes">6</span></div>
                    </div>
                    <div class="mnemonic-box">
                        <div class="mnemonic-title">💡 Mẹo Nhớ Chữ Hán</div>
                        <div class="mnemonic-content" id="char-mnemonic"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="toast" id="toast">Tuyệt vời! Bạn viết rất đẹp! 🎉</div>
    <script>
        const hanziData = {hanzi_json};
        const RADICAL_DICT = {radical_dict_json};
        const characters = Object.keys(hanziData);
        let selectedChar = characters[0];
        let writer = null;
        function initSidebar() {{
            const sidebar = document.getElementById('charSidebar');
            characters.forEach((char) => {{
                const btn = document.createElement('button');
                btn.className = 'char-btn' + (char === selectedChar ? ' active' : '');
                btn.innerHTML = char + " <span>(" + (hanziData[char].pinyin || '') + ")</span>";
                btn.onclick = () => selectCharacter(char, btn);
                sidebar.appendChild(btn);
            }});
        }}
        function selectCharacter(char, btnElement) {{
            selectedChar = char;
            document.querySelectorAll('.char-btn').forEach(btn => btn.classList.remove('active'));
            if (btnElement) btnElement.classList.add('active');
            loadCharacter(char);
        }}
        function loadCharacter(char) {{
            document.getElementById('character-target-div').innerHTML = '';
            const detail = hanziData[char];
            document.getElementById('char-pinyin').innerText = detail.pinyin || '';
            document.getElementById('char-meaning').innerText = detail.meaning || `Chữ Hán: ${{char}}`;
            const rawRadical = detail.radical || '一';
            const radicalTranslation = RADICAL_DICT[rawRadical] || "";
            document.getElementById('char-radical').innerText = radicalTranslation ? rawRadical + " - " + radicalTranslation : rawRadical;
            document.getElementById('char-strokes').innerText = detail.strokes || 6;
            document.getElementById('char-mnemonic').innerText = detail.mnemonic || "Luyện viết theo đúng thứ tự các nét.";
            writer = HanziWriter.create('character-target-div', char, {{
                width: 250, height: 250, padding: 15, showOutline: true,
                strokeColor: '#00796b', outlineColor: '#f3f3f3', drawingColor: '#e65100',
                drawingWidth: 6, strokeAnimationSpeed: 1, delayBetweenStrokes: 300
            }});
            setTimeout(() => {{ writer.animateCharacter(); }}, 300);
        }}
        function animateChar() {{ if (writer) writer.animateCharacter(); }}
        function startPractice() {{ if (writer) writer.quiz({{ onComplete: function() {{ showToast("Tuyệt vời! Bạn viết rất chính xác chữ " + selectedChar + "! 🎉"); }} }}); }}
        function speakChar() {{
            const utterance = new SpeechSynthesisUtterance(selectedChar);
            utterance.lang = 'zh-CN'; utterance.rate = 0.8;
            window.speechSynthesis.cancel(); window.speechSynthesis.speak(utterance);
        }}
        function showToast(msg) {{
            const toast = document.getElementById('toast'); toast.innerText = msg; toast.classList.add('show');
            setTimeout(() => {{ toast.classList.remove('show'); }}, 3000);
        }}
        if (characters.length > 0) {{ initSidebar(); loadCharacter(selectedChar); }}
    </script>
</body>
</html>"""

ARRANGE_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>10 Câu Sắp Xếp - HSK 2 3.0 Bài {lesson_id}</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        body {{ background: #fdf2f8; }}
        .game-wrapper {{ max-width: 700px; margin: 0 auto; padding: 2rem; text-align: center; }}
        .quiz-card {{ background: var(--white); border-radius: 30px; padding: 2.5rem 2rem; box-shadow: var(--shadow); margin-top: 1.5rem; min-height: 420px; display: flex; flex-direction: column; justify-content: center; position: relative; }}
        .progress-container {{ width: 100%; height: 10px; background: #eee; border-radius: 5px; margin-bottom: 1.5rem; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: #00796b; width: 0%; transition: width 0.3s; }}
        .question-title {{ font-size: 1.5rem; font-weight: 800; color: var(--primary-dark); margin-bottom: 0.5rem; }}
        .question-sub {{ font-size: 1.1rem; color: #666; margin-bottom: 1.5rem; }}
        .phrase-box {{ display: flex; flex-wrap: wrap; gap: 0.8rem; justify-content: center; margin: 1.5rem 0; min-height: 80px; padding: 1.2rem; border: 2px dashed #b2dfdb; border-radius: 20px; background: #e0f2f1; transition: 0.3s; }}
        .phrase-item {{ padding: 0.8rem 1.2rem; background: white; border: 2px solid #00796b; border-radius: 14px; cursor: pointer; font-size: 1.3rem; font-weight: 700; color: #004d40; transition: 0.2s; box-shadow: 0 3px 8px rgba(0,0,0,0.06); font-family: "KaiTi", "楷体", "STKaiti", serif; }}
        .phrase-item:hover {{ background: #b2dfdb; transform: scale(1.05); }}
        .submit-btn {{ padding: 1.2rem; background: #00796b; color: white; border: none; border-radius: 15px; font-weight: 700; font-size: 1.1rem; cursor: pointer; width: 100%; transition: 0.3s; margin-top: 1rem; }}
        .submit-btn:hover {{ background: #004d40; transform: translateY(-2px); }}
        .audio-btn-big {{ background: #e0f2f1; border: 2px solid #00796b; border-radius: 50%; width: 50px; height: 50px; font-size: 1.5rem; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; margin-left: 10px; transition: 0.2s; }}
        .audio-btn-big:hover {{ background: #b2dfdb; transform: scale(1.1); }}
        .result-screen {{ display: none; }}
        .score-circle {{ width: 140px; height: 140px; border-radius: 50%; border: 8px solid #00796b; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; font-weight: 800; margin: 1.5rem auto; color: #004d40; }}
    </style>
</head>
<body>
    <a href="index.html" class="home-logo-btn"><img src="mascot.png" alt="Home"></a>
    <div class="page-container">
        <a href="game-hsk2.html" class="back-btn">← Quay lại danh sách bài</a>
        <div class="game-wrapper">
            <div id="game-ui">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                    <div class="progress-container" style="margin-bottom: 0; flex: 1;"><div class="progress-fill" id="progress"></div></div>
                    <div id="progress-text" style="font-weight: bold; color: var(--primary-dark); font-size: 1.1rem; min-width: 50px; text-align: right;">1/10</div>
                </div>
                <div class="quiz-card" id="quiz-card"></div>
            </div>
            <div id="result-ui" class="result-screen">
                <div class="quiz-card">
                    <h1 style="color: var(--primary-dark);">KẾT QUẢ SẮP XẾP CÂU</h1>
                    <div class="score-circle" id="final-score">0%</div>
                    <p id="score-text" style="font-size: 1.2rem; color: #555;"></p>
                    <button class="submit-btn" onclick="location.reload()">Luyện Tập Lại</button>
                    <a href="game-hsk2-l{lesson_id}-translate.html" class="submit-btn" style="background: #e65100; text-decoration: none; display: block; text-align: center; margin-top: 1rem; line-height: 1.2;">Thử sức Dịch Việt Trung ➔</a>
                </div>
            </div>
        </div>
    </div>
    <script>
        const sentences = {sentences_json};
        let currentIndex = 0;
        let score = 0;
        function renderQuestion() {{
            const item = sentences[currentIndex];
            const card = document.getElementById('quiz-card');
            document.getElementById('progress').style.width = ((currentIndex + 1) / sentences.length * 100) + '%';
            document.getElementById('progress-text').innerText = (currentIndex + 1) + '/' + sentences.length;
            let shuffled = [...item.phrases].sort(() => Math.random() - 0.5);
            card.innerHTML = `
                <div class="question-title">Câu ${{currentIndex + 1}}: Sắp xếp câu hoàn chỉnh</div>
                <div id="drop-zone" class="phrase-box"></div>
                <div style="text-align: right; margin-bottom: 0.5rem;">
                    <button onclick="clearDropZone()" style="background: #ff8787; color: white; border: none; padding: 6px 14px; border-radius: 10px; font-size: 0.85rem; cursor: pointer; font-weight: bold;">Xóa tất cả</button>
                </div>
                <div id="drag-zone" class="phrase-box" style="border: none; background: transparent;">
                    ${{shuffled.map(p => `<div class="phrase-item" onclick="movePhrase(this, '${{item.cn}}')">${{p}}</div>`).join('')}}
                </div>
                <div id="feedback-zone" style="margin-top: 1rem;"></div>
            `;
        }}
        function movePhrase(el, correctStr) {{
            const dropZone = document.getElementById('drop-zone');
            const dragZone = document.getElementById('drag-zone');
            if (el.parentNode === dragZone) dropZone.appendChild(el);
            else dragZone.appendChild(el);
            const currentStr = Array.from(dropZone.children).map(x => x.innerText).join('').replace(/[，。？！\s]/g, '');
            const cleanCorrect = correctStr.replace(/[，。？！\s]/g, '');
            if (dragZone.children.length === 0 && dropZone.children.length > 0) {{
                const feedback = document.getElementById('feedback-zone');
                if (currentStr === cleanCorrect) {{
                    dropZone.style.background = "#d4edda"; dropZone.style.borderColor = "#28a745"; score++;
                    feedback.innerHTML = `<div style="color: #28a745; font-weight: bold; font-size: 1.3rem; margin-bottom: 1rem;">Correct! Bạn ghép rất chuẩn! 🎉 <button class="audio-btn-big" onclick="speak('${{correctStr}}')">🔊</button></div>`;
                    speak(correctStr); showNextBtn();
                }} else {{
                    dropZone.style.background = "#f8d7da"; dropZone.style.borderColor = "#dc3545";
                    feedback.innerHTML = `<div style="color: #dc3545; font-weight: bold; font-size: 1.1rem; margin-bottom: 1rem;">Chưa đúng rồi!<br><span style="color: #155724; font-size: 1.3rem;">Đáp án đúng: ${{correctStr}}</span> <button class="audio-btn-big" onclick="speak('${{correctStr}}')">🔊</button></div>`;
                    speak(correctStr); showNextBtn();
                }}
            }}
        }}
        function clearDropZone() {{
            const dropZone = document.getElementById('drop-zone');
            const dragZone = document.getElementById('drag-zone');
            while (dropZone.firstChild) dragZone.appendChild(dropZone.firstChild);
            dropZone.style.background = "#e0f2f1"; dropZone.style.borderColor = "#b2dfdb";
        }}
        function showNextBtn() {{
            const dragItems = document.querySelectorAll('.phrase-item');
            dragItems.forEach(b => b.onclick = null);
            const btn = document.createElement('button');
            btn.className = "submit-btn";
            btn.innerText = currentIndex < sentences.length - 1 ? "Câu tiếp theo ➔" : "Xem kết quả 🏆";
            btn.onclick = () => {{ currentIndex++; if (currentIndex < sentences.length) renderQuestion(); else showResults(); }};
            document.getElementById('quiz-card').appendChild(btn);
        }}
        function speak(text) {{
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'zh-CN'; utterance.rate = 0.8;
            window.speechSynthesis.cancel(); window.speechSynthesis.speak(utterance);
        }}
        function showResults() {{
            document.getElementById('game-ui').style.display = 'none';
            document.getElementById('result-ui').style.display = 'block';
            const pct = Math.round((score / sentences.length) * 100);
            document.getElementById('final-score').innerText = pct + '%';
            document.getElementById('score-text').innerText = `Bạn đã hoàn thành chính xác ${{score}} / ${{sentences.length}} câu sắp xếp.`;
        }}
        renderQuestion();
    </script>
</body>
</html>"""

TRANSLATE_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>10 Câu Dịch Việt Trung - HSK 2 3.0 Bài {lesson_id}</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        body {{ background: #fdf2f8; }}
        .game-wrapper {{ max-width: 700px; margin: 0 auto; padding: 2rem; text-align: center; }}
        .quiz-card {{ background: var(--white); border-radius: 30px; padding: 2.5rem 2rem; box-shadow: var(--shadow); margin-top: 1.5rem; min-height: 420px; display: flex; flex-direction: column; justify-content: center; position: relative; }}
        .progress-container {{ width: 100%; height: 10px; background: #eee; border-radius: 5px; margin-bottom: 1.5rem; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: #e65100; width: 0%; transition: width 0.3s; }}
        .vn-prompt {{ font-size: 1.5rem; font-weight: 800; color: #d84315; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: center; gap: 0.8rem; background: #fff3e0; padding: 1.2rem; border-radius: 20px; border: 1px solid #ffe0b2; }}
        .audio-btn {{ background: white; border: 2px solid #e65100; border-radius: 50%; width: 45px; height: 45px; font-size: 1.3rem; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; transition: 0.2s; }}
        .audio-btn:hover {{ background: #ffe0b2; transform: scale(1.1); }}
        .typing-input {{ width: 100%; padding: 1.2rem; border: 2px solid #ddd; border-radius: 15px; font-size: 1.5rem; text-align: center; margin-bottom: 1.5rem; transition: 0.3s; font-family: "KaiTi", "楷体", "STKaiti", serif; }}
        .typing-input:focus {{ border-color: #e65100; outline: none; box-shadow: 0 0 10px rgba(230,81,0,0.2); }}
        .submit-btn {{ padding: 1.2rem; background: #e65100; color: white; border: none; border-radius: 15px; font-weight: 700; font-size: 1.1rem; cursor: pointer; width: 100%; transition: 0.3s; margin-top: 0.5rem; }}
        .submit-btn:hover {{ background: #bf360c; transform: translateY(-2px); }}
        .result-screen {{ display: none; }}
        .score-circle {{ width: 140px; height: 140px; border-radius: 50%; border: 8px solid #e65100; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; font-weight: 800; margin: 1.5rem auto; color: #bf360c; }}
    </style>
</head>
<body>
    <a href="index.html" class="home-logo-btn"><img src="mascot.png" alt="Home"></a>
    <div class="page-container">
        <a href="game-hsk2.html" class="back-btn">← Quay lại danh sách bài</a>
        <div class="game-wrapper">
            <div id="game-ui">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                    <div class="progress-container" style="margin-bottom: 0; flex: 1;"><div class="progress-fill" id="progress"></div></div>
                    <div id="progress-text" style="font-weight: bold; color: #e65100; font-size: 1.1rem; min-width: 50px; text-align: right;">1/10</div>
                </div>
                <div class="quiz-card" id="quiz-card"></div>
            </div>
            <div id="result-ui" class="result-screen">
                <div class="quiz-card">
                    <h1 style="color: #bf360c;">KẾT QUẢ DỊCH VIỆT TRUNG</h1>
                    <div class="score-circle" id="final-score">0%</div>
                    <p id="score-text" style="font-size: 1.2rem; color: #555;"></p>
                    <button class="submit-btn" onclick="location.reload()">Dịch Lại</button>
                    <a href="game-hsk2.html" class="submit-btn" style="background: #00796b; text-decoration: none; display: block; text-align: center; margin-top: 1rem; line-height: 1.2;">Quay lại danh sách bài học</a>
                </div>
            </div>
        </div>
    </div>
    <script>
        const sentences = {sentences_json};
        let currentIndex = 0;
        let score = 0;
        function renderQuestion() {{
            const item = sentences[currentIndex];
            const card = document.getElementById('quiz-card');
            document.getElementById('progress').style.width = ((currentIndex + 1) / sentences.length * 100) + '%';
            document.getElementById('progress-text').innerText = (currentIndex + 1) + '/' + sentences.length;
            card.innerHTML = `
                <div style="font-size: 1.2rem; font-weight: 700; color: #e65100; margin-bottom: 1rem;">Câu ${{currentIndex + 1}}: Dịch câu tiếng Việt sang tiếng Trung</div>
                <div class="vn-prompt">
                    <span>${{item.vn}}</span>
                    <button class="audio-btn" onclick="speakVN('${{item.vn}}')" title="Nghe tiếng Việt">🔊</button>
                </div>
                <input type="text" class="typing-input" id="answer-input" placeholder="Nhập câu tiếng Trung..." autocomplete="off">
                <button class="submit-btn" id="submit-btn" onclick="checkTranslation('${{item.cn}}')">Gửi Đáp Án</button>
                <div id="feedback-zone" style="margin-top: 1rem;"></div>
            `;
            document.getElementById('answer-input').focus();
            document.getElementById('answer-input').addEventListener('keypress', function(e) {{ if (e.key === 'Enter') checkTranslation(item.cn); }});
        }}
        function checkTranslation(correctCN) {{
            const input = document.getElementById('answer-input');
            const val = input.value.trim().replace(/[，。？！\s]/g, '');
            const cleanCorrect = correctCN.replace(/[，。？！\s]/g, '');
            const feedback = document.getElementById('feedback-zone');
            const submitBtn = document.getElementById('submit-btn');
            if (!val) return;
            submitBtn.disabled = true; input.disabled = true;
            if (val === cleanCorrect) {{
                score++; input.style.borderColor = "#28a745"; input.style.background = "#d4edda";
                feedback.innerHTML = `<div style="color: #28a745; font-weight: bold; font-size: 1.3rem;">Correct! Bạn dịch rất chính xác! 🎉 <button class="audio-btn" style="display:inline-flex; width:36px; height:36px; font-size:1rem; margin-left:5px;" onclick="speakZH('${{correctCN}}')">🔊</button></div>`;
                speakZH(correctCN);
            }} else {{
                input.style.borderColor = "#dc3545"; input.style.background = "#f8d7da";
                feedback.innerHTML = `<div style="color: #dc3545; font-weight: bold; font-size: 1.1rem;">Chưa đúng rồi!<br><span style="color: #155724; font-size: 1.4rem;">Đáp án đúng: ${{correctCN}}</span> <button class="audio-btn" style="display:inline-flex; width:36px; height:36px; font-size:1rem; margin-left:5px;" onclick="speakZH('${{correctCN}}')">🔊</button></div>`;
                speakZH(correctCN);
            }}
            const nextBtn = document.createElement('button');
            nextBtn.className = "submit-btn"; nextBtn.style.background = "#4dabf7"; nextBtn.style.marginTop = "1rem";
            nextBtn.innerText = currentIndex < sentences.length - 1 ? "Câu tiếp theo ➔" : "Xem kết quả 🏆";
            nextBtn.onclick = () => {{ currentIndex++; if (currentIndex < sentences.length) renderQuestion(); else showResults(); }};
            document.getElementById('quiz-card').appendChild(nextBtn);
        }}
        function speakZH(text) {{
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'zh-CN'; utterance.rate = 0.8;
            window.speechSynthesis.cancel(); window.speechSynthesis.speak(utterance);
        }}
        function speakVN(text) {{
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'vi-VN'; utterance.rate = 0.9;
            window.speechSynthesis.cancel(); window.speechSynthesis.speak(utterance);
        }}
        function showResults() {{
            document.getElementById('game-ui').style.display = 'none';
            document.getElementById('result-ui').style.display = 'block';
            const pct = Math.round((score / sentences.length) * 100);
            document.getElementById('final-score').innerText = pct + '%';
            document.getElementById('score-text').innerText = `Bạn đã hoàn thành chính xác ${{score}} / ${{sentences.length}} câu dịch Việt Trung.`;
        }}
        renderQuestion();
    </script>
</body>
</html>"""

# Generate pages for all 15 lessons
for lesson_id in range(1, 16):
    vocab_list = lessons.get(lesson_id, [])
    vocab_json = json.dumps(vocab_list, ensure_ascii=False)
    
    # 1. Flip page
    flip_filename = f'game-hsk2-l{lesson_id}-flip.html'
    with open(flip_filename, 'w', encoding='utf-8') as f:
        f.write(FLIP_TEMPLATE.format(lesson_id=lesson_id, vocab_json=vocab_json))
        
    # 2. Hanzi page
    hanzi_details_dict = get_hanzi_details_dict(vocab_list)
    hanzi_json = json.dumps(hanzi_details_dict, ensure_ascii=False)
    radical_dict_json = json.dumps(RADICAL_DICT, ensure_ascii=False)
    hanzi_filename = f'game-hsk2-l{lesson_id}-hanzi.html'
    with open(hanzi_filename, 'w', encoding='utf-8') as f:
        f.write(HANZI_TEMPLATE.format(lesson_id=lesson_id, hanzi_json=hanzi_json, radical_dict_json=radical_dict_json))
        
    # 3. Arrange page
    sentences = get_lesson_sentences(lesson_id, vocab_list)
    sentences_json = json.dumps(sentences, ensure_ascii=False)
    arrange_filename = f'game-hsk2-l{lesson_id}-arrange.html'
    with open(arrange_filename, 'w', encoding='utf-8') as f:
        f.write(ARRANGE_TEMPLATE.format(lesson_id=lesson_id, sentences_json=sentences_json))
        
    # 4. Translate page
    translate_filename = f'game-hsk2-l{lesson_id}-translate.html'
    with open(translate_filename, 'w', encoding='utf-8') as f:
        f.write(TRANSLATE_TEMPLATE.format(lesson_id=lesson_id, sentences_json=sentences_json))

print("Successfully generated all 60 game files for HSK2 (Lessons 1-15 x 4 modes)!")
