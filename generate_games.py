import json
import os

# Build a global mapping of all vocab grouped by level and lesson
all_vocab = {}
for lvl in range(1, 7):
    json_file = f'hsk{lvl}_vocab_data.json'
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            all_vocab[lvl] = json.load(f)

def get_cumulative_chars(target_level, target_lesson):
    chars = set()
    for lvl in range(1, target_level + 1):
        if lvl in all_vocab:
            for item in all_vocab[lvl]:
                l_id = int(item['lesson'])
                if lvl < target_level or l_id <= target_lesson:
                    for char in item['hanzi']:
                        chars.add(char)
    return "".join(chars)

def generate_hsk_games(level):
    json_file = f'hsk{level}_vocab_data.json'
    if not os.path.exists(json_file):
        print(f"File {json_file} not found. Skipping HSK{level}.")
        return

    # Load Hanzi Details (Only for HSK 1)
    hanzi_details = {}
    if level == 1:
        details_file = 'hsk1_hanzi_details.json'
        if os.path.exists(details_file):
            with open(details_file, 'r', encoding='utf-8') as hf:
                hanzi_details = json.load(hf)

    # Load vocabulary data
    with open(json_file, 'r', encoding='utf-8') as f:
        vocab_data = json.load(f)

    # Group by lesson
    lessons = {}
    for item in vocab_data:
        l_id = int(item['lesson'])
        if l_id not in lessons:
            lessons[l_id] = []
        lessons[l_id].append(item)

    # HTML Templates
    FLIP_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lật Thẻ Thông Minh - HSK {level_label} Bài {lesson_id}</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        body {{ background: #f0f9ff; }}
        .game-header {{ text-align: center; margin-bottom: 2rem; position: relative; }}
        .mascot-container {{ 
            position: absolute; right: 0; top: -20px; width: 100px; 
            animation: bounce 2s infinite ease-in-out; 
        }}
        @keyframes bounce {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
        .mascot-bubble {{
            background: white; padding: 10px 15px; border-radius: 20px; box-shadow: var(--shadow);
            font-size: 0.85rem; position: absolute; right: 110px; top: 10px; width: 150px;
            color: var(--primary-dark); font-weight: 700; z-index: 10;
        }}
        .game-container {{ max-width: 1100px; margin: 0 auto; padding: 2rem; }}
        .single-card-container {{ display: flex; justify-content: center; align-items: center; margin-top: 2rem; position: relative; }}
        .flip-card {{ background-color: transparent; width: 100%; max-width: 500px; height: 500px; perspective: 1000px; cursor: pointer; }}
        .flip-card-inner {{ position: relative; width: 100%; height: 100%; text-align: center; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); transform-style: preserve-3d; }}
        .flip-card.flipped .flip-card-inner {{ transform: rotateY(180deg); }}
        .flip-card-front, .flip-card-back {{ 
            position: absolute; width: 100%; height: 100%; backface-visibility: hidden; 
            display: flex; flex-direction: column; border-radius: 30px; padding: 1.2rem; 
            border: 2px solid var(--primary-light); background: white;
            box-shadow: 0 10px 30px rgba(165, 207, 218, 0.2);
        }}
        .flip-card-front {{ justify-content: center; align-items: center; }}
        .flip-card-front .hanzi {{ font-family: "KaiTi", "楷体", "STKaiti", serif; font-size: 8rem; font-weight: 800; color: var(--primary-dark); transition: transform 0.3s; }}
        .flip-card:hover .hanzi {{ transform: scale(1.1); }}
        .flip-card-back {{ transform: rotateY(180deg); text-align: left; background: #fff; border-color: var(--primary-color); }}
        .flip-card.mastered .flip-card-front, .flip-card.mastered .flip-card-back {{ border-color: #ffd700; background: #fffdf0; }}
        .master-badge {{ position: absolute; top: 15px; right: 15px; font-size: 1.5rem; display: none; z-index: 5; }}
        .flip-card.mastered .master-badge {{ display: block; animation: pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); }}
        @keyframes pop {{ from {{ transform: scale(0); }} to {{ transform: scale(1); }} }}
        .back-header {{ width: 100%; display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid #eee; padding-bottom: 0.5rem; }}
        .back-hanzi {{ font-family: "KaiTi", "楷体", "STKaiti", serif; font-size: 3rem; font-weight: 800; color: var(--primary-dark); }}
        .back-pinyin {{ font-size: 1.8rem; color: #e67e22; font-weight: 700; }}
        .btn-speak {{ background: var(--primary-light); border: none; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; transition: 0.3s; }}
        .btn-speak:hover {{ background: var(--primary-color); transform: scale(1.1); }}
        .back-meaning {{ font-size: 1.6rem; font-weight: 700; color: #444; }}
        .back-example {{ font-size: 1.2rem; background: #f9f9f9; padding: 1rem; border-radius: 12px; margin-top: 1rem; line-height: 1.5; }}
        .back-example strong {{ font-size: 1.2rem; color: var(--primary-dark); }}
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
        <a href="game-hsk{level}.html" class="back-btn">← Quay lại</a>
        <header class="game-header">
            <h1 style="color: var(--primary-dark); font-size: 2.2rem;">Lật Thẻ Thông Minh</h1>
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

    MASTER_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trùm Từ Vựng - HSK {level_label} Bài {lesson_id}</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        body {{ background: #fdf2f8; }}
        .game-wrapper {{ max-width: 600px; margin: 0 auto; padding: 2rem; text-align: center; }}
        .quiz-card {{ background: var(--white); border-radius: 30px; padding: 3rem 2rem; box-shadow: var(--shadow); margin-top: 2rem; min-height: 450px; display: flex; flex-direction: column; justify-content: center; position: relative; }}
        .progress-container {{ width: 100%; height: 8px; background: #eee; border-radius: 4px; margin-bottom: 2rem; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: var(--primary-color); width: 0%; transition: width 0.3s; }}
        .question-text {{ font-size: 1.5rem; font-weight: 700; color: var(--text-color); margin-bottom: 1rem; }}
        .sub-text {{ font-size: 1.1rem; color: #666; margin-bottom: 2rem; line-height: 1.6; }}
        .options-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem; }}
        .option-btn {{ padding: 1.2rem; background: #f8fbfe; border: 2px solid #eef2f5; border-radius: 15px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: 0.2s; }}
        .option-btn:hover:not(:disabled) {{ border-color: var(--primary-color); background: #f0f7f9; }}
        .option-btn.correct {{ background: #d4edda !important; border-color: #28a745 !important; color: #155724 !important; }}
        .option-btn.wrong {{ background: #f8d7da !important; border-color: #dc3545 !important; color: #721c24 !important; }}
        .typing-input {{ width: 100%; padding: 1.2rem; border: 2px solid #ddd; border-radius: 15px; font-size: 1.4rem; text-align: center; margin-bottom: 1.5rem; transition: 0.3s; }}
        .typing-input:focus {{ border-color: var(--primary-color); outline: none; box-shadow: 0 0 10px rgba(255,107,107,0.1); }}
        .submit-btn {{ padding: 1.2rem; background: var(--primary-color); color: white; border: none; border-radius: 15px; font-weight: 700; font-size: 1.1rem; cursor: pointer; width: 100%; transition: 0.3s; }}
        .submit-btn:hover {{ background: var(--primary-dark); transform: translateY(-2px); }}
        .phrase-box {{ display: flex; flex-wrap: wrap; gap: 0.8rem; justify-content: center; margin: 1.5rem 0; min-height: 80px; padding: 1rem; border: 2px dashed #ffe4e6; border-radius: 20px; background: #fffafb; }}
        .phrase-item {{ padding: 0.8rem 1.2rem; background: white; border: 2px solid #ffccd5; border-radius: 12px; cursor: pointer; font-size: 1.2rem; font-weight: 600; color: #e91e63; transition: 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .phrase-item:hover {{ background: #fff0f3; transform: scale(1.05); }}
        .blank-text {{ font-size: 1.8rem; letter-spacing: 2px; color: var(--text-color); margin-bottom: 2rem; font-weight: bold; }}
        .blank-fill {{ color: var(--primary-color); border-bottom: 3px solid var(--primary-color); padding: 0 10px; min-width: 60px; display: inline-block; }}
        .result-screen {{ display: none; }}
        .score-circle {{ width: 150px; height: 150px; border-radius: 50%; border: 10px solid var(--primary-light); display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: 800; margin: 2rem auto; color: var(--primary-dark); }}
    </style>
</head>
<body>
    <a href="index.html" class="home-logo-btn">
        <img src="mascot.png" alt="Home">
    </a>
    <div class="page-container">
        <a href="game-hsk{level}.html" class="back-btn">← Quay lại</a>
        <div class="game-wrapper">
            <div id="game-ui">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
                    <div class="progress-container" style="margin-bottom: 0; flex: 1;"><div class="progress-fill" id="progress"></div></div>
                    <div id="progress-text" style="font-weight: bold; color: var(--primary-dark); font-size: 1.1rem; min-width: 50px; text-align: right;"></div>
                </div>
                <div class="quiz-card" id="quiz-card"></div>
            </div>
            <div id="result-ui" class="result-screen">
                <div class="quiz-card">
                    <h1 style="color: var(--primary-dark);">Kết Quả</h1>
                    <div class="score-circle" id="final-score">0%</div>
                    <p id="score-text"></p>
                    <button class="submit-btn" style="margin-top: 2rem;" onclick="location.reload()">Chơi Lại</button>
                    <a href="game-hsk{level}-l{lesson_id}-match.html" class="submit-btn" style="margin-top: 1rem; background: #e65100; text-decoration: none; display: block; line-height: 1.5; padding: 1rem 0; text-align: center;">Thử thách Ghép Đôi</a>
                </div>
            </div>
        </div>
    </div>
    <script>
        const vocabulary = {vocab_json};
        const allHanzi = {all_hanzi_json};
        let currentQuestion = 0, score = 0, questions = [], totalQuestions = 0;

        function initGame() {{ 
            totalQuestions = Math.min(20, vocabulary.length); 
            questions = generateQuestions(); 
            renderQuestion(); 
        }}

        function splitIntoPhrases(sentence, targetWord) {{
            // Improved splitting: use lesson vocabulary as anchors for "meaningful" chunks
            let cleanSentence = sentence.replace(/[，。？！、\s]/g, '');
            let lessonWords = allHanzi.sort((a, b) => b.length - a.length);
            
            let phrases = [];
            let remaining = cleanSentence;
            
            while (remaining.length > 0) {{
                let found = false;
                for (let word of lessonWords) {{
                    if (remaining.startsWith(word)) {{
                        phrases.push(word);
                        remaining = remaining.substring(word.length);
                        found = true;
                        break;
                    }}
                }}
                
                if (!found) {{
                    // If no lesson word matches, take 1-2 chars
                    let take = (remaining.length >= 2 && !lessonWords.some(w => remaining.substring(1).startsWith(w))) ? 2 : 1;
                    phrases.push(remaining.substring(0, take));
                    remaining = remaining.substring(take);
                }}
            }}
            
            return phrases;
        }}

        function generateQuestions() {{
            let qs = [], shuffled = [...vocabulary].sort(() => Math.random() - 0.5);
            for (let i = 0; i < totalQuestions; i++) {{
                const word = shuffled[i];
                let type;
                
                if ({level} === 3) {{
                    const types = [10, 11, 12];
                    type = types[Math.floor(Math.random() * types.length)];
                }} else {{
                    type = Math.floor(Math.random() * 4);
                }}

                let q = {{ type, word }};
                
                if (type <= 2) q.options = generateOptions(word, type);
                if (type === 10) {{
                    q.correctSentence = word.ex_cn.replace(/[，。？！、\s]/g, '');
                    q.phrases = splitIntoPhrases(word.ex_cn, word.hanzi).sort(() => Math.random() - 0.5);
                }}
                if (type === 12) {{
                    q.displaySentence = word.ex_cn.replace(word.hanzi, "______");
                    q.options = generateOptions(word, 0);
                }}
                
                qs.push(q);
            }}
            return qs;
        }}

        function generateOptions(correctWord, type) {{
            let options = [correctWord];
            while (options.length < 4 && vocabulary.length >= 4) {{
                const rand = vocabulary[Math.floor(Math.random() * vocabulary.length)];
                if (!options.includes(rand)) options.push(rand);
            }}
            return options.sort(() => Math.random() - 0.5);
        }}

        function renderQuestion() {{
            const q = questions[currentQuestion], card = document.getElementById('quiz-card'), progress = document.getElementById('progress');
            progress.style.width = (currentQuestion / totalQuestions) * 100 + '%';
            document.getElementById('progress-text').innerText = (currentQuestion + 1) + '/' + totalQuestions;
            
            let html = '';
            if (q.type === 0) {{
                html = `<div class="question-text">Nghe và chọn từ đúng:</div><button class="audio-btn" style="background: #fdf2f8; border: none; font-size: 3rem; cursor: pointer;" onclick="speak('${{q.word.hanzi}}')">🔊</button><div class="options-grid">${{q.options.map(opt => `<button class="option-btn" onclick="checkAnswer('${{opt.hanzi}}', '${{q.word.hanzi}}', this)">${{opt.hanzi}}</button>`).join('')}}</div>`;
                setTimeout(() => speak(q.word.hanzi), 500);
            }} else if (q.type === 1) {{
                html = `<div class="question-text">Từ "${{q.word.hanzi}}" có nghĩa là gì?</div><div class="options-grid">${{q.options.map(opt => `<button class="option-btn" onclick="checkAnswer('${{opt.meaning}}', '${{q.word.meaning}}', this)">${{opt.meaning}}</button>`).join('')}}</div>`;
            }} else if (q.type === 2) {{
                html = `<div class="question-text">Từ "${{q.word.hanzi}}" có phiên âm là gì?</div><div class="options-grid">${{q.options.map(opt => `<button class="option-btn" onclick="checkAnswer('${{opt.pinyin}}', '${{q.word.pinyin}}', this)">${{opt.pinyin}}</button>`).join('')}}</div>`;
            }} else if (q.type === 3) {{
                html = `<div class="question-text">"${{q.word.meaning}}" trong tiếng Trung là gì?</div><input type="text" class="typing-input" id="typing-ans" placeholder="Nhập Hán tự..."><button class="submit-btn" onclick="checkTyping('${{q.word.hanzi}}')">Kiểm tra</button>`;
            }} 
            // New Types for HSK3
            else if (q.type === 10) {{
                html = `<div class="question-text">Sắp xếp câu chính xác:</div><div id="drop-zone" class="phrase-box"></div><div style="text-align: right; margin-bottom: 1rem;"><button onclick="clearDropZone()" style="background: #ff8787; color: white; border: none; padding: 5px 12px; border-radius: 8px; font-size: 0.8rem; cursor: pointer;">Xóa tất cả</button></div><div id="drag-zone" class="phrase-box" style="border: none; background: transparent;">${{q.phrases.map(p => `<div class="phrase-item" onclick="movePhrase(this, '${{q.correctSentence}}')">${{p}}</div>`).join('')}}</div>`;
            }} else if (q.type === 11) {{
                html = `<div class="question-text">Dịch câu sau sang tiếng Trung:</div><div class="sub-text" style="font-size: 1.4rem; color: var(--primary-dark); display: flex; align-items: center; justify-content: center; gap: 0.8rem;">${{q.word.ex_vn}}<button onclick="speakVN(this.dataset.text)" data-text="${{q.word.ex_vn}}" style="background: none; border: 2px solid var(--primary-color); border-radius: 50%; width: 42px; height: 42px; font-size: 1.3rem; cursor: pointer; flex-shrink: 0; display: flex; align-items: center; justify-content: center; transition: 0.2s;" onmouseover="this.style.background='var(--primary-light)'" onmouseout="this.style.background='none'" title="Nghe câu tiếng Việt">🔊</button></div><input type="text" class="typing-input" id="typing-ans" placeholder="Nhập câu tiếng Trung..." data-answer="${{q.word.ex_cn}}"><button class="submit-btn" onclick="checkTyping('${{q.word.ex_cn.replace(/[，。？！\s]/g, '')}}', '${{q.word.ex_cn}}')">Gửi đáp án</button>`;
            }} else if (q.type === 12) {{
                html = `<div class="question-text">Điền từ vào ô trống:</div><div class="blank-text">${{q.displaySentence.replace("______", "<span class='blank-fill' id='blank-target'>?</span>")}}</div><div class="options-grid">${{q.options.map(opt => `<button class="option-btn" onclick="checkBlank('${{opt.hanzi}}', '${{q.word.hanzi}}', this)">${{opt.hanzi}}</button>`).join('')}}</div>`;
            }}

            card.innerHTML = html;
        }}

        function speak(t) {{ const m = new SpeechSynthesisUtterance(); m.text = t; m.lang = 'zh-CN'; window.speechSynthesis.cancel(); window.speechSynthesis.speak(m); }}
        function speakVN(t) {{ const m = new SpeechSynthesisUtterance(); m.text = t; m.lang = 'vi-VN'; window.speechSynthesis.cancel(); window.speechSynthesis.speak(m); }}
        
        function checkAnswer(s, c, b) {{
            const btns = document.querySelectorAll('.option-btn');
            btns.forEach(x => x.disabled = true);
            if (s === c) {{ b.classList.add('correct'); score++; }} 
            else {{ b.classList.add('wrong'); btns.forEach(x => {{ if(x.innerText === c) x.classList.add('correct'); }}); }}
            showNext();
        }}

        function checkBlank(s, c, b) {{
            const target = document.getElementById('blank-target');
            target.innerText = c;
            checkAnswer(s, c, b);
        }}

        function checkTyping(correct, fullSentence) {{
            const input = document.getElementById('typing-ans');
            const val = input.value.trim().replace(/[，。？！、\s]/g, '');
            const speakText = fullSentence || correct;
            if (val === correct) {{
                input.style.borderColor = "#28a745";
                input.style.background = "#d4edda";
                score++;
                // Auto-speak the correct Chinese answer
                setTimeout(() => speak(speakText), 300);
            }} else {{
                input.style.borderColor = "#dc3545";
                input.style.background = "#f8d7da";
                const err = document.createElement('div');
                err.style = "color: #dc3545; margin-top: 10px; font-weight: bold; display: flex; align-items: center; justify-content: center; gap: 0.6rem;";
                err.innerHTML = `Đáp án đúng: <span style="color: #155724; font-size: 1.3rem;">${{speakText}}</span><button onclick="speak('${{speakText}}')" style="background: #28a745; color: white; border: none; border-radius: 50%; width: 36px; height: 36px; font-size: 1.1rem; cursor: pointer;" title="Nghe đáp án tiếng Trung">🔊</button>`;
                input.parentNode.appendChild(err);
                // Auto-speak the correct Chinese answer after a short delay
                setTimeout(() => speak(speakText), 300);
            }}
            document.querySelector('.submit-btn').disabled = true;
            showNext();
        }}

        function movePhrase(el, correct) {{
            const dropZone = document.getElementById('drop-zone');
            const dragZone = document.getElementById('drag-zone');
            if (el.parentNode === dragZone) dropZone.appendChild(el);
            else dragZone.appendChild(el);

            const current = Array.from(dropZone.children).map(x => x.innerText).join('').replace(/\s/g, '');
            const cleanCorrect = correct.replace(/\s/g, '');

            if (dragZone.children.length === 0 && dropZone.children.length > 0) {{
                if (current === cleanCorrect) {{
                    dropZone.style.background = "#d4edda";
                    dropZone.style.borderColor = "#28a745";
                    score++;
                    showNext();
                }} else {{
                    dropZone.style.background = "#f8d7da";
                    dropZone.style.borderColor = "#dc3545";
                    const err = document.createElement('div');
                    err.style = "color: #dc3545; margin-top: 10px; font-weight: bold;";
                    err.innerHTML = `Chưa đúng rồi!<br><span style="color: #28a745">Đáp án: ${{correct}}</span>`;
                    document.getElementById('quiz-card').appendChild(err);
                    showNext();
                }}
            }}
        }}

        function clearDropZone() {{
            const dropZone = document.getElementById('drop-zone');
            const dragZone = document.getElementById('drag-zone');
            while (dropZone.firstChild) {{
                dragZone.appendChild(dropZone.firstChild);
            }}
            dropZone.style.background = "#fffafb";
            dropZone.style.borderColor = "#ffe4e6";
        }}

        function showNext() {{
            const btns = document.querySelectorAll('.phrase-item');
            btns.forEach(b => b.onclick = null);
            
            const nextBtn = document.createElement('button');
            nextBtn.className = "submit-btn";
            nextBtn.style = "margin-top: 1.5rem; background: #4dabf7;";
            nextBtn.innerText = "Tiếp theo ➔";
            nextBtn.onclick = () => {{
                currentQuestion++;
                if (currentQuestion < totalQuestions) renderQuestion();
                else showResults();
            }};
            document.getElementById('quiz-card').appendChild(nextBtn);
        }}

        function showResults() {{
            document.getElementById('game-ui').style.display = 'none';
            document.getElementById('result-ui').style.display = 'block';
            document.getElementById('final-score').innerText = Math.round((score/totalQuestions)*100)+'%';
            document.getElementById('score-text').innerText = `Bạn đã hoàn thành ${{score}}/${{totalQuestions}} câu hỏi.`;
        }}

        initGame();
    </script>
</body>
</html>"""

    MATCH_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Truy Tìm Cặp Đôi - HSK {level_label} Bài {lesson_id}</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        body {{ background: #fdf2f8; }}
        .game-container {{ max-width: 800px; margin: 0 auto; padding: 2rem; text-align: center; }}
        .memory-grid {{ 
            display: grid; 
            grid-template-columns: repeat(4, 1fr); 
            gap: 1rem; 
            margin-top: 2rem; 
        }}
        .memory-card {{
            aspect-ratio: 1/1;
            background-color: var(--white);
            cursor: pointer;
            position: relative;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
            font-weight: bold;
            box-shadow: var(--shadow);
            border: 2px solid var(--primary-light);
            transition: transform 0.2s, background-color 0.2s, opacity 0.6s, border-color 0.2s;
            font-size: 1.1rem;
            color: var(--text-color);
            text-align: center;
        }}
        .memory-card:hover:not(.matched):not(.selected) {{
            border-color: var(--primary-color);
            background-color: #f0f9ff;
            transform: translateY(-2px);
        }}
        .memory-card.hanzi {{
            font-size: 2rem;
            color: var(--primary-dark);
        }}
        .memory-card.selected {{
            background-color: var(--primary-light);
            border-color: var(--primary-color);
            transform: scale(1.05);
        }}
        .memory-card.matched {{
            visibility: hidden;
            opacity: 0;
            pointer-events: none;
        }}
        .stats {{
            margin-bottom: 1rem;
            font-size: 1.2rem;
            font-weight: bold;
            color: var(--primary-dark);
            display: flex;
            justify-content: space-around;
        }}
        .result-overlay {{
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255,255,255,0.9);
            z-index: 100;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        .result-content {{
            background: white;
            padding: 3rem;
            border-radius: 30px;
            box-shadow: var(--shadow);
            text-align: center;
        }}
        .btn-restart {{
            margin-top: 2rem;
            padding: 1rem 2rem;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: bold;
            cursor: pointer;
            font-size: 1.1rem;
        }}
        @media (max-width: 600px) {{
            .memory-grid {{ grid-template-columns: repeat(4, 1fr); gap: 0.5rem; }}
            .memory-card {{ font-size: 0.9rem; }}
            .memory-card.hanzi {{ font-size: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <a href="index.html" class="home-logo-btn">
        <img src="mascot.png" alt="Home">
    </a>
    <div class="page-container">
        <a href="game-hsk{level}.html" class="back-btn">← Quay lại</a>
        <div class="game-container">
            <h1 style="color: var(--primary-dark); margin-bottom: 1rem;">Truy Tìm Cặp Đôi: Bài {lesson_id}</h1>
            <div class="stats">
                <div>Lượt: <span id="moves">0</span></div>
                <div>Thời gian: <span id="timer">0</span>s</div>
                <div>Cặp: <span id="matches">0/8</span></div>
            </div>
            <div class="memory-grid" id="gameGrid"></div>
        </div>
    </div>

    <div id="resultOverlay" class="result-overlay">
        <div class="result-content" id="resultContent">
            <!-- Content will be injected by JS -->
        </div>
    </div>

    <script>
        const allVocabulary = {vocab_json};
        let remainingWords = [...allVocabulary];
        let currentRoundWords = [];
        let cardsData = [];
        let selectedCards = [];
        let matchedPairs = 0;
        let moves = 0;
        let canSelect = true;
        let timer = 0;
        let timerInterval = null;
        let gameStarted = false;

        function initGame(isNewGame = true) {{
            if (isNewGame) {{
                remainingWords = [...allVocabulary].sort(() => Math.random() - 0.5);
                moves = 0;
                timer = 0;
                gameStarted = false;
                clearInterval(timerInterval);
                document.getElementById('timer').innerText = '0';
                document.getElementById('moves').innerText = '0';
            }}

            const gameGrid = document.getElementById('gameGrid');
            gameGrid.innerHTML = '';
            cardsData = [];
            
            // Take up to 8 words for this round
            currentRoundWords = remainingWords.splice(0, 8);

            currentRoundWords.forEach((item, index) => {{
                cardsData.push({{ id: index, content: item.hanzi, type: 'hanzi' }});
                cardsData.push({{ id: index, content: item.meaning, type: 'meaning' }});
            }});

            cardsData.sort(() => Math.random() - 0.5);

            cardsData.forEach((data) => {{
                const card = document.createElement('div');
                card.className = `memory-card ${{data.type}}`;
                card.innerText = data.content;
                card.dataset.id = data.id;
                
                card.addEventListener('click', () => selectCard(card));
                gameGrid.appendChild(card);
            }});

            matchedPairs = 0;
            selectedCards = [];
            canSelect = true;
            updateStats();
        }}

        function startTimer() {{
            if (gameStarted) return;
            gameStarted = true;
            timerInterval = setInterval(() => {{
                timer++;
                document.getElementById('timer').innerText = timer;
            }}, 1000);
        }}

        function selectCard(card) {{
            if (!canSelect || card.classList.contains('selected') || card.classList.contains('matched')) return;

            startTimer();
            card.classList.add('selected');
            selectedCards.push(card);

            if (selectedCards.length === 2) {{
                moves++;
                checkMatch();
            }}
        }}

        function checkMatch() {{
            canSelect = false;
            const [card1, card2] = selectedCards;
            const isMatch = card1.dataset.id === card2.dataset.id;

            if (isMatch) {{
                setTimeout(() => {{
                    card1.classList.add('matched');
                    card2.classList.add('matched');
                    matchedPairs++;
                    updateStats();
                    selectedCards = [];
                    canSelect = true;
                    
                    if (matchedPairs === currentRoundWords.length) {{
                        if (remainingWords.length > 0) {{
                            showNextRoundPrompt();
                        }} else {{
                            clearInterval(timerInterval);
                            showFinalResult();
                        }}
                    }}
                }}, 400);
            }} else {{
                setTimeout(() => {{
                    card1.classList.remove('selected');
                    card2.classList.remove('selected');
                    selectedCards = [];
                    canSelect = true;
                }}, 600);
            }}
        }}

        function updateStats() {{
            document.getElementById('moves').innerText = moves;
            document.getElementById('matches').innerText = `${{matchedPairs}}/${{currentRoundWords.length}}`;
            document.getElementById('timer').innerText = timer;
        }}

        function showNextRoundPrompt() {{
            const content = document.getElementById('resultContent');
            content.innerHTML = `
                <h2 style="font-size: 2rem; color: var(--primary-dark); margin-bottom: 1rem;">Xong hiệp này!</h2>
                <p style="font-size: 1.1rem;">Còn ${{remainingWords.length}} từ vựng nữa.</p>
                <button class="btn-restart" onclick="nextRound()">Tiếp tục hiệp kế</button>
            `;
            document.getElementById('resultOverlay').style.display = 'flex';
        }}

        function showFinalResult() {{
            const content = document.getElementById('resultContent');
            content.innerHTML = `
                <h2 style="font-size: 2.5rem; color: var(--primary-dark); margin-bottom: 1rem;">Hoàn thành!</h2>
                <p style="font-size: 1.2rem;">Bạn đã học hết từ vựng của bài này.</p>
                <div style="margin: 1.5rem 0; font-weight: bold; font-size: 1.1rem;">
                    Tổng thời gian: ${{timer}} giây<br>
                    Tổng số lượt: ${{moves}}
                </div>
                <button class="btn-restart" onclick="resetGame()">Chơi Lại Từ Đầu</button>
            `;
            document.getElementById('resultOverlay').style.display = 'flex';
        }}

        function nextRound() {{
            document.getElementById('resultOverlay').style.display = 'none';
            initGame(false);
        }}

        function resetGame() {{
            document.getElementById('resultOverlay').style.display = 'none';
            initGame(true);
        }}

        initGame();
    </script>
</body>
</html>"""

    MEMORY_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Siêu Trí Nhớ - HSK {level_label} Bài {lesson_id}</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        body {{ background: #fdf2f8; }}
        .game-header {{ text-align: center; margin-bottom: 2rem; }}
        .memory-container {{ max-width: 900px; margin: 0 auto; padding: 2rem; background: white; border-radius: 30px; box-shadow: var(--shadow); }}
        .dialog-selector {{ display: flex; justify-content: center; gap: 1rem; margin-bottom: 2rem; }}
        .dialog-btn {{ padding: 0.5rem 1.5rem; border-radius: 10px; border: 2px solid var(--primary-light); background: white; cursor: pointer; font-weight: 700; transition: 0.3s; }}
        .dialog-btn.active {{ background: var(--primary-color); color: white; border-color: var(--primary-color); }}
        
        .audio-section-simple {{ text-align: center; margin-bottom: 2rem; padding: 2rem; background: #f0f9ff; border-radius: 20px; }}
        .btn-speaker {{ width: 100px; height: 100px; border-radius: 50%; border: none; background: var(--primary-color); color: white; font-size: 3rem; cursor: pointer; transition: 0.3s; box-shadow: 0 10px 25px rgba(165,207,218,0.5); display: flex; align-items: center; justify-content: center; margin: 0 auto; }}
        .btn-speaker:hover {{ transform: scale(1.1); background: var(--primary-dark); }}
        
        .practice-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem; }}
        .practice-box {{ display: flex; flex-direction: column; gap: 0.5rem; }}
        .practice-box label {{ font-weight: 800; color: var(--primary-dark); font-size: 0.9rem; }}
        .display-area, .input-area {{ width: 100%; min-height: 150px; padding: 1.5rem; border-radius: 20px; border: 2px solid #eee; font-size: 1.4rem; line-height: 1.6; font-family: "Noto Sans SC", sans-serif; }}
        .display-area {{ background: #f9f9f9; color: transparent; user-select: none; transition: 0.3s; }}
        .display-area.visible {{ color: #333; }}
        .input-area {{ background: white; resize: none; border-color: var(--primary-light); }}
        .input-area:focus {{ outline: none; border-color: var(--primary-color); box-shadow: 0 0 0 4px rgba(165,207,218,0.2); }}
        
        .controls {{ display: flex; justify-content: center; gap: 1.5rem; }}
        .btn-action {{ padding: 1rem 2rem; border-radius: 15px; border: none; font-weight: 800; cursor: pointer; transition: 0.3s; font-size: 1rem; }}
        .btn-hint {{ background: #e3f2fd; color: #1976d2; }}
        .btn-submit {{ background: var(--primary-color); color: white; }}
        .btn-action:hover {{ transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
        
        .result-section {{ margin-top: 3rem; padding-top: 2rem; border-top: 2px dashed #eee; display: none; }}
        .diff-text {{ font-size: 1.6rem; margin-bottom: 1rem; line-height: 2; }}
        .char-correct {{ color: #28a745; }}
        .char-wrong {{ color: #dc3545; text-decoration: underline; font-weight: 800; }}
        .correction-info {{ background: #fffdf0; padding: 1.5rem; border-radius: 20px; border: 1px solid #ffeeba; }}
        .correction-item {{ margin-bottom: 1rem; }}
        .correction-item:last-child {{ margin-bottom: 0; }}
        .correct-hanzi {{ font-size: 1.4rem; font-weight: 800; color: var(--primary-dark); }}
        .correct-pinyin {{ color: #e67e22; font-style: italic; }}
    </style>
</head>
<body>
    <a href="index.html" class="home-logo-btn">
        <img src="mascot.png" alt="Home">
    </a>
    <div class="page-container">
        <a href="game-hsk{level}.html" class="back-btn">← Quay lại</a>
        <header class="game-header">
            <h1 style="color: var(--primary-dark); font-size: 2.2rem;">Siêu Trí Nhớ 🧠</h1>
            <p>HSK {level_label} Bài {lesson_id}: Nghe và kể lại bài khóa</p>
        </header>

        <div class="memory-container">
            <div class="dialog-selector" id="dialogSelector"></div>

            <div class="audio-section-simple">
                <button class="btn-speaker" onclick="toggleAudio()" id="mainPlayBtn">🔊</button>
                <div id="dialogLoc" style="margin-top: 1rem; font-style: italic; color: #888; text-align: center;">Chủ đề: ...</div>
            </div>

            <div class="practice-grid">
                <div class="practice-box">
                    <label>ĐÁP ÁN (ẨN)</label>
                    <div id="displayArea" class="display-area"></div>
                </div>
                <div class="practice-box">
                    <label>BẠN GÕ VÀO ĐÂY</label>
                    <textarea id="inputArea" class="input-area" placeholder="Gõ chữ Hán bạn nghe được..."></textarea>
                </div>
            </div>

            <div class="controls">
                <button class="btn-action btn-hint" onclick="showHint()">Gợi ý một xíu 💡</button>
                <button class="btn-action btn-submit" onclick="submitAnswer()">Nộp bài ✅</button>
            </div>

            <div id="resultSection" class="result-section">
                <h2 style="margin-bottom: 1.5rem; color: var(--primary-dark);">Kết quả kiểm tra:</h2>
                <div id="diffOutput" class="diff-text"></div>
                <div class="correction-info" id="correctionInfo"></div>
                <button class="btn-action btn-submit" style="margin-top: 2rem; width: 100%;" onclick="location.reload()">Thử lại bài này</button>
            </div>
        </div>
    </div>

    <script>
        const dialogs = {dialog_json};
        let currentDialogIdx = 0;

        const displayArea = document.getElementById('displayArea');
        const inputArea = document.getElementById('inputArea');
        const diffOutput = document.getElementById('diffOutput');
        const correctionInfo = document.getElementById('correctionInfo');
        const resultSection = document.getElementById('resultSection');
        const dialogLoc = document.getElementById('dialogLoc');
        const dialogSelector = document.getElementById('dialogSelector');

        function initSelector() {{
            dialogSelector.innerHTML = '';
            dialogs.forEach((d, idx) => {{
                const btn = document.createElement('button');
                btn.className = 'dialog-btn' + (idx === 0 ? ' active' : '');
                btn.innerText = 'Bài khóa ' + (idx + 1);
                btn.onclick = () => loadDialog(idx);
                dialogSelector.appendChild(btn);
            }});
        }}

        function loadDialog(idx) {{
            window.speechSynthesis.cancel();
            document.getElementById('mainPlayBtn').innerHTML = '🔊';
            
            currentDialogIdx = idx;
            const d = dialogs[idx];
            displayArea.innerText = d.content;
            displayArea.classList.remove('visible');
            inputArea.value = '';
            resultSection.style.display = 'none';
            dialogLoc.innerText = "Chủ đề: " + d.location;
            
            document.querySelectorAll('.dialog-btn').forEach((btn, i) => {{
                btn.classList.toggle('active', i === idx);
            }});
        }}

        function toggleAudio() {{
            const btn = document.getElementById('mainPlayBtn');
            if (window.speechSynthesis.speaking) {{
                if (window.speechSynthesis.paused) {{
                    window.speechSynthesis.resume();
                    btn.innerHTML = '⏸';
                }} else {{
                    window.speechSynthesis.pause();
                    btn.innerHTML = '▶';
                }}
                return;
            }}
            playAudio();
        }}

        function playAudio() {{
            window.speechSynthesis.cancel();
            const text = dialogs[currentDialogIdx].content;
            const utterance = new SpeechSynthesisUtterance(text);
            const btn = document.getElementById('mainPlayBtn');
            
            const voices = window.speechSynthesis.getVoices();
            const preferredVoice = voices.find(v => v.name === 'Tingting') || 
                                   voices.find(v => v.name.includes('Meijia')) ||
                                   voices.find(v => v.name.includes('Google') && v.lang.includes('zh')) ||
                                   voices.find(v => v.lang.includes('zh'));
            
            if (preferredVoice) utterance.voice = preferredVoice;
            utterance.lang = 'zh-CN';
            utterance.rate = 0.8; 

            utterance.onstart = () => {{
                btn.innerHTML = '⏸';
            }};
            utterance.onend = () => {{
                btn.innerHTML = '🔊';
            }};
            utterance.onerror = () => {{
                btn.innerHTML = '🔊';
            }};
            window.speechSynthesis.speak(utterance);
        }}

        function showHint() {{
            displayArea.classList.add('visible');
        }}

        function submitAnswer() {{
            const correct = dialogs[currentDialogIdx].content.replace(/[，。？！、\s]/g, '');
            const input = inputArea.value.replace(/[，。？！、\s]/g, '');
            
            let html = '';
            let fullCorrectText = dialogs[currentDialogIdx].content;
            let j = 0;
            
            for (let i = 0; i < fullCorrectText.length; i++) {{
                const char = fullCorrectText[i];
                if (/[，。？！、\s]/.test(char)) {{
                    html += char;
                    continue;
                }}
                
                if (j < input.length) {{
                    if (input[j] === char) {{
                        html += `<span class="char-correct">${{char}}</span>`;
                    }} else {{
                        html += `<span class="char-wrong">${{char}}</span>`;
                    }}
                    j++;
                }} else {{
                    html += `<span class="char-wrong" style="opacity: 0.5;">${{char}}</span>`;
                }}
            }}

            diffOutput.innerHTML = html;
            
            let correctHtml = '<h3>Xem lại chi tiết:</h3>';
            dialogs[currentDialogIdx].lines.forEach(line => {{
                correctHtml += `
                    <div class="correction-item">
                        <div class="correct-hanzi">${{line.hanzi}}</div>
                        <div class="correct-pinyin">${{line.pinyin}}</div>
                    </div>
                `;
            }});
            correctionInfo.innerHTML = correctHtml;
            
            resultSection.style.display = 'block';
            resultSection.scrollIntoView({{ behavior: 'smooth' }});
        }}

        window.addEventListener('pagehide', () => {{
            window.speechSynthesis.cancel();
        }});

        initSelector();
        loadDialog(0);
    </script>
</body>
</html>"""

    HANZI_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luyện Chữ Hán - HSK {level_label} Bài {lesson_id}</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3.5/dist/hanzi-writer.min.js"></script>
    <style>
        body {{ background: #f0f7f9; }}
        .game-wrapper {{
            display: flex;
            gap: 2rem;
            max-width: 1000px;
            margin: 2rem auto;
            align-items: flex-start;
        }}
        .char-sidebar {{
            flex: 0 0 180px;
            background: var(--white);
            border-radius: 25px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            max-height: 550px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 0.8rem;
        }}
        .sidebar-title {{
            font-size: 0.9rem;
            font-weight: bold;
            color: var(--primary-dark);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
            text-align: center;
            border-bottom: 2px solid var(--primary-light);
            padding-bottom: 0.5rem;
        }}
        .char-btn {{
            padding: 0.8rem;
            background: #f8fbfe;
            border: 2px solid #eef2f5;
            border-radius: 15px;
            font-size: 1.6rem;
            font-family: "KaiTi", "楷体", "STKaiti", serif;
            font-weight: bold;
            color: var(--text-color);
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.8rem;
        }}
        .char-btn span {{
            font-size: 0.9rem;
            font-family: Arial, sans-serif;
            font-weight: normal;
            color: #666;
        }}
        .char-btn:hover {{
            border-color: var(--primary-color);
            background: #f0f7f9;
            transform: translateY(-2px);
        }}
        .char-btn.active {{
            background: var(--primary-color);
            border-color: var(--primary-color);
            color: white;
        }}
        .char-btn.active span {{
            color: #fff;
        }}
        
        .char-panel {{
            flex: 1;
            background: var(--white);
            border-radius: 30px;
            padding: 3rem;
            box-shadow: var(--shadow);
            display: flex;
            gap: 3rem;
            min-height: 550px;
        }}
        .writer-section {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1.5rem;
            flex: 0 0 250px;
        }}
        .hanzi-writer-container {{
            width: 250px;
            height: 250px;
            background: #fff;
            border: 3px solid var(--primary-light);
            border-radius: 20px;
            position: relative;
            box-shadow: 0 10px 25px rgba(165,207,218,0.15);
            background-image: 
                linear-gradient(to right, #f5f5f5 1px, transparent 1px),
                linear-gradient(to bottom, #f5f5f5 1px, transparent 1px),
                linear-gradient(to right, transparent 50%, #ffe3e3 1px, transparent 50%),
                linear-gradient(to bottom, transparent 50%, #ffe3e3 1px, transparent 50%);
            background-size: 25px 25px, 25px 25px, 100% 100%, 100% 100%;
        }}
        
        .control-buttons {{
            display: flex;
            flex-direction: column;
            gap: 0.8rem;
            width: 100%;
        }}
        .btn-control {{
            padding: 0.8rem 1.5rem;
            border-radius: 12px;
            border: 2px solid var(--primary-color);
            background: white;
            color: var(--primary-dark);
            font-weight: bold;
            font-size: 0.95rem;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }}
        .btn-control:hover {{
            background: var(--primary-color);
            color: white;
            transform: translateY(-2px);
        }}
        .btn-speak-big {{
            background: #f0f7f9;
            border-color: var(--primary-color);
        }}
        
        .details-section {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}
        
        .char-header {{
            border-bottom: 2px dashed var(--primary-light);
            padding-bottom: 1rem;
        }}
        .char-pinyin-display {{
            font-size: 2rem;
            font-weight: bold;
            color: #e67e22;
        }}
        .char-meaning-display {{
            font-size: 1.3rem;
            font-weight: bold;
            color: var(--text-color);
            margin-top: 0.3rem;
        }}
        
        .pills-container {{
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        .info-pill {{
            background: #f0f9ff;
            color: var(--text-color);
            padding: 0.6rem 1.2rem;
            border-radius: 100px;
            font-size: 0.95rem;
            border: 1px solid var(--primary-light);
            display: flex;
            gap: 0.5rem;
        }}
        .info-pill strong {{
            color: var(--primary-dark);
        }}
        
        .mnemonic-box {{
            background: #fffdf0;
            border: 1px solid #ffeeba;
            border-radius: 20px;
            padding: 1.5rem;
            margin-top: auto;
            position: relative;
        }}
        .mnemonic-title {{
            font-weight: bold;
            color: #d48806;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .mnemonic-content {{
            font-size: 1.05rem;
            line-height: 1.6;
            color: #555;
        }}
        
        .evolution-step-card {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 90px;
        }}
        .evolution-step-card img {{
            width: 100%;
            height: 75px;
            object-fit: contain;
        }}
        .evolution-arrow {{
            font-size: 1.5rem;
            color: var(--primary-dark);
            font-weight: bold;
            user-select: none;
        }}
        
        /* Toast notification */
        .toast {{
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: #28a745;
            color: white;
            padding: 1rem 2rem;
            border-radius: 50px;
            font-weight: bold;
            box-shadow: 0 10px 25px rgba(40,167,69,0.3);
            z-index: 1000;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s;
            opacity: 0;
            pointer-events: none;
        }}
        .toast.show {{
            transform: translateX(-50%) translateY(0);
            opacity: 1;
        }}

        @media (max-width: 768px) {{
            .game-wrapper {{
                flex-direction: column;
                padding: 1rem;
            }}
            .char-sidebar {{
                flex: 1;
                width: 100%;
                max-height: 120px;
                flex-direction: row;
                overflow-x: auto;
                padding: 1rem;
            }}
            .sidebar-title {{
                display: none;
            }}
            .char-btn {{
                flex-shrink: 0;
                min-width: 80px;
            }}
            .char-panel {{
                flex-direction: column;
                padding: 2rem;
                width: 100%;
                gap: 2rem;
            }}
            .writer-section {{
                width: 100%;
                flex: none;
            }}
        }}
    </style>
</head>
<body>
    <a href="index.html" class="home-logo-btn">
        <img src="mascot.png" alt="Home">
    </a>
    <div class="page-container">
        <a href="game-hsk1.html" class="back-btn">← Quay lại</a>
        <h1 style="text-align: center; color: var(--primary-dark); font-size: 2.2rem; margin-bottom: 1rem;">Luyện Chữ Hán HSK {level_label} ✍️</h1>
        <p style="text-align: center; margin-bottom: 2rem; opacity: 0.8;">Học cách viết, số nét, bộ thủ và mẹo nhớ từng chữ Hán trong bài.</p>
        
        <div class="game-wrapper">
            <div class="char-sidebar" id="charSidebar">
                <div class="sidebar-title">Chữ Hán</div>
                <!-- Buttons will be injected here -->
            </div>
            
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
                        <span class="char-pinyin-display" id="char-pinyin">nǐ</span>
                        <div class="char-meaning-display" id="char-meaning">bạn, anh, chị</div>
                    </div>
                    
                    <div class="pills-container">
                        <div class="info-pill"><strong>Bộ thủ:</strong> <span id="char-radical">丨</span></div>
                        <div class="info-pill"><strong>Số nét:</strong> <span id="char-strokes">7</span></div>
                    </div>
                    
                    <div class="mnemonic-box">
                        <div class="mnemonic-title">💡 Mẹo Nhớ Chữ Hán</div>
                        <div class="mnemonic-content" id="char-mnemonic"></div>
                    </div>
                    
                    <div class="illustration-box" id="char-illustration-container" style="display: none; margin-top: 1.5rem; text-align: center; width: 100%;">
                        <div style="font-weight: bold; color: var(--primary-dark); margin-bottom: 0.8rem; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 1px; display: flex; align-items: center; gap: 0.5rem; justify-content: center;">🎨 Quá trình hình thành chữ Hán</div>
                        <div id="char-illustration-single-box" style="display: none;">
                            <img id="char-illustration" src="" style="max-width: 100%; max-height: 180px; border-radius: 15px; border: 1px solid var(--primary-light); box-shadow: 0 4px 10px rgba(0,0,0,0.05);" alt="Infographic">
                        </div>
                        <div id="char-illustration-steps-box" style="display: none; justify-content: center; align-items: center; gap: 0.4rem; flex-wrap: wrap; width: 100%;">
                            <!-- Steps will be injected here -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="toast" id="toast">Tuyệt vời! Bạn viết rất đẹp! 🎉</div>

    <script>
        const hanziData = {hanzi_json};
        const RADICAL_DICT = {{
            "丨": "Cổn (sổ thẳng)",
            "丿": "Phiệt (nét phẩy)",
            "人": "Nhân (người)",
            "亻": "Nhân (người)",
            "口": "Khẩu (miệng)",
            "宀": "Miên (mái nhà)",
            "日": "Nhật (mặt trời/ngày)",
            "木": "Mộc (cây)",
            "水": "Thủy (nước)",
            "氵": "Thủy (nước)",
            "言": "Ngôn (nói/lời nói)",
            "讠": "Ngôn (nói/lời nói)",
            "门": "Môn (cửa)",
            "心": "Tâm (tim/lòng)",
            "忄": "Tâm (tim/lòng)",
            "禾": "Hòa (lúa)",
            "女": "Nữ (con gái/phụ nữ)",
            "贝": "Bối (tiền vỏ sò/bảo bối)",
            "囗": "Vi (bao quanh/bờ cõi)",
            "八": "Bát (số tám)",
            "走": "Tẩu (đi/chạy)",
            "戈": "Qua (cây thương/vũ khí)",
            "羊": "Dương (con cừu)",
            "大": "Đại (to lớn)",
            "彳": "Xích (bước chân trái)",
            "乙": "Ất (vị trí thứ hai)",
            "韦": "Vi (da thú)",
            "耳": "Nhĩ (tai)",
            "目": "Mục (mắt)",
            "王": "Vương (vua/ngọc)",
            "力": "Lực (sức mạnh)",
            "月": "Nguyệt (mặt trăng/tháng)",
            "火": "Hỏa (lửa)",
            "灬": "Hỏa (lửa)",
            "土": "Thổ (đất)",
            "寸": "Thốn (tấc/chiều dài)",
            "食": "Thực (ăn/thức ăn)",
            "饣": "Thực (ăn/thức ăn)",
            "犬": "Khuyển (con chó)",
            "犭": "Khuyển (con chó)",
            "父": "Phụ (cha)",
            "手": "Thủ (tay)",
            "扌": "Thủ (tay)",
            "糸": "Mịch (tơ lụa)",
            "纟": "Mịch (tơ lụa)",
            "辵": "Sước (chợt đi chợt dừng)",
            "辶": "Sước (chợt đi chợt dừng)",
            "艸": "Thảo (cỏ)",
            "艹": "Thảo (cỏ)",
            "竹": "Trúc (tre trúc)",
            "⺮": "Trúc (tre trúc)",
            "雨": "Vũ (mưa)",
            "自": "Tự (bản thân/mũi)",
            "足": "Túc (chân)",
            "车": "Xa (xe)",
            "衣": "Y (áo/trang phục)",
            "衤": "Y (áo/trang phục)",
            "广": "Quảng (nhà rộng/mái che)",
            "疒": "Nạch (bệnh tật)",
            "皿": "Mãnh (bát đĩa/đồ đựng)",
            "石": "Thạch (đá)",
            "示": "Thị (mách bảo/thần đất)",
            "礻": "Thị (mách bảo/thần đất)",
            "穴": "Huyệt (hang động)",
            "立": "Lập (đứng thẳng)",
            "皮": "Bì (da)",
            "矢": "Thỉ (mũi tên)",
            "耒": "Lỗi (cái cày)",
            "聿": "Duật (bút viết)",
            "肉": "Nhục (thịt)",
            "臣": "Thần (bầy tôi)",
            "至": "Chí (đến)",
            "臼": "Cối (cái cối giã)",
            "舌": "Thiệt (cái lưỡi)",
            "舛": "Suyễn (sai lệch)",
            "舟": "Chu (chiếc thuyền)",
            "艮": "Cấn (bướng bỉnh/dừng lại)",
            "色": "Sắc (màu sắc)",
            "虍": "Hô (vằn hổ)",
            "虫": "Trùng (sâu bọ)",
            "血": "Huyết (máu)",
            "行": "Hành (đi/hàng lối)",
            "西": "Tây (phía tây)",
            "见": "Kiến (nhìn thấy)",
            "角": "Giác (sừng/góc)",
            "谷": "Cốc (khe núi)",
            "豆": "Đậu (hạt đậu/cái đậu)",
            "豕": "Thỉ (con heo)",
            "豸": "Trĩ (loài sâu không chân)",
            "赤": "Xích (màu đỏ)",
            "身": "Thân (thân thể)",
            "辛": "Tân (cay/vất vả)",
            "辰": "Thần (sao Thần/giờ Thần)",
            "邑": "Ấp (vùng đất/thành trì)",
            "酉": "Dậu (rượu/giờ Dậu)",
            "釆": "Biện (phân biệt)",
            "里": "Lý (dặm/làng)",
            "长": "Trường (dài/trưởng)",
            "青": "Thanh (màu xanh)",
            "非": "Phi (không phải/sai)",
            "面": "Diện (mặt/bề mặt)",
            "革": "Cách (da thuộc/thay đổi)",
            "韭": "Cửu (rau hẹ)",
            "音": "Âm (âm thanh)",
            "页": "Hiệt (trang giấy/đầu)",
            "风": "Phong (gió)",
            "飞": "Phi (bay)",
            "首": "Thủ (đầu/đứng đầu)",
            "香": "Hương (mùi thơm)",
            "马": "Mã (con ngựa)",
            "骨": "Cốt (xương)",
            "高": "Cao (cao)",
            "髟": "Tiêu (tóc dài)",
            "鬥": "Đấu (chiến đấu)",
            "鬯": "Sướng (rượu nghệ)",
            "鬲": "Cách (cái đỉnh/nồi đất)",
            "鬼": "Quỷ (ma quỷ)",
            "鱼": "Ngư (con cá)",
            "鸟": "Điểu (con chim)",
            "卤": "Lỗ (đất mặn)",
            "鹿": "Lộc (con hươu)",
            "麦": "Mạch (lúa mì)",
            "麻": "Ma (cây gai)",
            "黄": "Hoàng (màu vàng)",
            "黍": "Thử (lúa nếp)",
            "黑": "Hắc (màu đen)",
            "黹": "Chỉ (may vá/thêu thùa)",
            "黾": "Mãnh (con ếch/con rùa)",
            "鼎": "Đỉnh (cái đỉnh đồng)",
            "鼓": "Cổ (cái trống)",
            "鼠": "Thử (con chuột)",
            "鼻": "Tị (mũi)",
            "齐": "Tề (ngay ngắn/bằng nhau)",
            "齿": "Sỉ (răng)",
            "龙": "Long (con rồng)",
            "龟": "Qui (con rùa)",
            "龠": "Dược (sáo trúc)",
            "一": "Nhất (số một)",
            "丶": "Chủ (chấm)",
            "亅": "Quyết (nét móc)",
            "二": "Nhị (số hai)",
            "亠": "Đầu (nắp, mái che)",
            "儿": "Nhân (chân người)",
            "入": "Nhập (vào)",
            "冂": "Quynh (vùng biên giới)",
            "冖": "Mịch (trùm khăn lên)",
            "冫": "Băng (nước đá)",
            "几": "Kỷ (cái bàn nhỏ)",
            "凵": "Khảm (há miệng/hố sâu)",
            "刀": "Đao (con dao)",
            "刂": "Đao (con dao)",
            "勹": "Bao (bao bọc)",
            "匕": "Chủy (cái thìa)",
            "匚": "Phương (tủ đựng đồ)",
            "匸": "Hệ (che đậy)",
            "十": "Thập (số mười)",
            "卜": "Bốc (xem bói)",
            "卩": "Tiết (quỳ gối/đốt tre)",
            "厂": "Hán (sườn núi)",
            "厶": "Tư (riêng tư)",
            "又": "Hựu (lại/bàn tay)",
            "士": "Sĩ (kẻ sĩ)",
            "夂": "Truy (đi chậm)",
            "夊": "Tuy (đi chậm)",
            "夕": "Tịch (buổi tối)",
            "子": "Tử (con/đứa trẻ)",
            "寸": "Thốn (tấc)",
            "小": "Tiểu (nhỏ bé)",
            "尢": "Uông (yếu đuối)",
            "尸": "Thi (xác chết)",
            "屮": "Triệt (mầm non mới mọc)",
            "山": "Sơn (núi)",
            "巛": "Xuyên (sông ngòi)",
            "川": "Xuyên (sông ngòi)",
            "工": "Công (thợ/công việc)",
            "己": "Kỷ (bản thân)",
            "巾": "Cân (khăn)",
            "干": "Can (lá chắn/thiên can)",
            "幺": "Yêu (nhỏ nhắn)",
            "廴": "Dẫn (đi dài)",
            "廾": "Củng (chắp tay)",
            "弋": "Dực (bắn cung)",
            "弓": "Cung (cái cung)",
            "彐": "Kệ (đầu con heo)",
            "彡": "Sâm (lông dài)",
            "支": "Chi (cành cây)",
            "攴": "Phộc (đánh khẽ)",
            "攵": "Phộc (đánh khẽ)",
            "文": "Văn (chữ viết/văn chương)",
            "斗": "Đấu (cái đấu đong gạo)",
            "斤": "Cân (cái rìu)",
            "方": "Phương (hướng/hình vuông)",
            "无": "Vô (không có)",
            "曰": "Viết (nói rằng)",
            "欠": "Khiếm (thiếu thốn)",
            "止": "Chỉ (dừng lại)",
            "歹": "Đãi (xấu xa)",
            "殳": "Thù (binh khí dài)",
            "毋": "Vô (chớ/không)",
            "比": "Tỉ (so sánh)",
            "毛": "Mao (lông)",
            "氏": "Thị (họ)",
            "气": "Khí (hơi nước/khí)",
            "爪": "Trảo (móng vuốt)",
            "爻": "Hào (hào âm dương)",
            "爿": "Tường (mảnh gỗ)",
            "片": "Phiến (mảnh tấm)",
            "牙": "Nha (răng)",
            "牛": "Ngưu (con bò)",
            "牜": "Ngưu (con bò)",
            "玄": "Huyền (màu đen)",
            "玉": "Ngọc (viên ngọc)",
            "瓜": "Qua (quả dưa)",
            "瓦": "Ngõa (ngói nung)",
            "甘": "Cam (ngọt)",
            "生": "Sinh (sinh ra/sống)",
            "用": "Dụng (sử dụng)",
            "田": "Điền (ruộng)",
            "疋": "Sơ (cuộn vải)",
            "癶": "Bát (bước đi)",
            "白": "Bạch (màu trắng)",
            "匚": "Phương (tủ đựng đồ)"
        }};
        const characters = Object.keys(hanziData);
        let selectedChar = characters[0];
        let writer = null;
        
        function initSidebar() {{
            const sidebar = document.getElementById('charSidebar');
            characters.forEach((char, idx) => {{
                const btn = document.createElement('button');
                btn.className = 'char-btn' + (char === selectedChar ? ' active' : '');
                btn.innerHTML = char + " <span>(" + hanziData[char].pinyin + ")</span>";
                btn.onclick = () => selectCharacter(char, btn);
                sidebar.appendChild(btn);
            }});
        }}
        
        function selectCharacter(char, btnElement) {{
            selectedChar = char;
            document.querySelectorAll('.char-btn').forEach(btn => btn.classList.remove('active'));
            if (btnElement) {{
                btnElement.classList.add('active');
            }}
            loadCharacter(char);
        }}
        
        function loadCharacter(char) {{
            document.getElementById('character-target-div').innerHTML = '';
            
            const detail = hanziData[char];
            document.getElementById('char-pinyin').innerText = detail.pinyin;
            document.getElementById('char-meaning').innerText = detail.meaning;
            const rawRadical = detail.radical;
            const radicalTranslation = RADICAL_DICT[rawRadical] || "";
            document.getElementById('char-radical').innerText = radicalTranslation ? rawRadical + " - " + radicalTranslation : rawRadical;
            document.getElementById('char-strokes').innerText = detail.strokes;
            document.getElementById('char-mnemonic').innerText = detail.mnemonic;
            
            const illustrationContainer = document.getElementById('char-illustration-container');
            const singleBox = document.getElementById('char-illustration-single-box');
            const stepsBox = document.getElementById('char-illustration-steps-box');
            const timestamp = new Date().getTime();
            
            if (detail.illustration_steps && detail.illustration_steps.length > 0) {{
                singleBox.style.display = 'none';
                stepsBox.style.display = 'flex';
                stepsBox.innerHTML = '';
                
                const labels = ["Hình vẽ", "Giáp cốt", "Tiểu triện", "Chữ Lệ", "Khải (Hiện đại)"];
                
                detail.illustration_steps.forEach((src, idx) => {{
                    const card = document.createElement('div');
                    card.className = 'evolution-step-card';
                    card.innerHTML = '<img src="' + src + '?t=' + timestamp + '" alt="Step ' + (idx+1) + '">';
                    stepsBox.appendChild(card);
                    
                    if (idx < detail.illustration_steps.length - 1) {{
                        const arrow = document.createElement('div');
                        arrow.className = 'evolution-arrow';
                        arrow.innerText = '→';
                        stepsBox.appendChild(arrow);
                    }}
                }});
                illustrationContainer.style.display = 'block';
            }} else if (detail.illustration) {{
                stepsBox.style.display = 'none';
                singleBox.style.display = 'block';
                document.getElementById('char-illustration').src = detail.illustration + "?t=" + timestamp;
                illustrationContainer.style.display = 'block';
            }} else {{
                illustrationContainer.style.display = 'none';
            }}
            
            writer = HanziWriter.create('character-target-div', char, {{
                width: 250,
                height: 250,
                padding: 15,
                showOutline: true,
                strokeColor: '#8AB8C5',
                outlineColor: '#f3f3f3',
                drawingColor: '#e65100',
                drawingWidth: 6,
                strokeAnimationSpeed: 1,
                delayBetweenStrokes: 300
            }});
            
            // Auto play animation
            setTimeout(() => {{
                writer.animateCharacter();
            }}, 300);
        }}
        
        function animateChar() {{
            if (writer) {{
                writer.animateCharacter();
            }}
        }}
        
        function startPractice() {{
            if (writer) {{
                writer.quiz({{
                    onComplete: function(summaryData) {{
                        showToast("Tuyệt vời! Bạn viết rất chính xác chữ " + selectedChar + "! 🎉");
                    }}
                }});
            }}
        }}
        
        function speakChar() {{
            const utterance = new SpeechSynthesisUtterance(selectedChar);
            utterance.lang = 'zh-CN';
            utterance.rate = 0.8;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
        }}
        
        function showToast(msg) {{
            const toast = document.getElementById('toast');
            toast.innerText = msg;
            toast.classList.add('show');
            setTimeout(() => {{
                toast.classList.remove('show');
            }}, 3000);
        }}
        
        window.addEventListener('pagehide', () => {{
            window.speechSynthesis.cancel();
        }});
        
        if (characters.length > 0) {{
            initSidebar();
            loadCharacter(selectedChar);
        }}
    </script>
</body>
</html>"""

    # Load Dialogues if level-specific JSON exists
    dialog_data = []
    dialog_file = f'hsk{level}_dialogs.json'
    if os.path.exists(dialog_file):
        with open(dialog_file, 'r', encoding='utf-8') as df:
            dialog_data = json.load(df)

    # Load all hanzi for anchor splitting
    try:
        with open('all_hanzi.json', 'r', encoding='utf-8') as f:
            all_hanzi_json = f.read()
    except:
        all_hanzi_json = "[]"

    # Generate files
    for lesson_id, vocab_list in lessons.items():
        vocab_json = json.dumps(vocab_list, ensure_ascii=False)
        
        level_label = f"{level} 3.0" if level in [1, 2] else str(level)
        
        # Flip Page
        with open(f'game-hsk{level}-l{lesson_id}-flip.html', 'w', encoding='utf-8') as f:
            f.write(FLIP_TEMPLATE.format(level=level, level_label=level_label, lesson_id=lesson_id, vocab_json=vocab_json))
        
        # Master Page
        cumulative_chars = get_cumulative_chars(level, int(lesson_id))
        with open(f'game-hsk{level}-l{lesson_id}-master.html', 'w', encoding='utf-8') as f:
            f.write(MASTER_TEMPLATE.format(level=level, level_label=level_label, lesson_id=lesson_id, vocab_json=vocab_json, cumulative_chars=cumulative_chars, all_hanzi_json=all_hanzi_json))

        # Match Page (HSK 1, 2, and 3)
        if level <= 3:
            with open(f'game-hsk{level}-l{lesson_id}-match.html', 'w', encoding='utf-8') as f:
                f.write(MATCH_TEMPLATE.format(level=level, level_label=level_label, lesson_id=lesson_id, vocab_json=vocab_json))

        # Memory Page
        if dialog_data:
            lesson_dialogs = next((item['dialogs'] for item in dialog_data if str(item['lesson']) == str(lesson_id)), [])
            if lesson_dialogs:
                dialog_json = json.dumps(lesson_dialogs, ensure_ascii=False)
                with open(f'game-hsk{level}-l{lesson_id}-memory.html', 'w', encoding='utf-8') as f:
                    f.write(MEMORY_TEMPLATE.format(level=level, level_label=level_label, lesson_id=lesson_id, dialog_json=dialog_json))

        # Hanzi Page (Only for HSK 1)
        if level == 1:
            lesson_chars = []
            seen_chars = set()
            for item in vocab_list:
                for char in item['hanzi']:
                    if '\u4e00' <= char <= '\u9fff' and char not in seen_chars:
                        seen_chars.add(char)
                        lesson_chars.append(char)
            
            # Look up details
            lesson_hanzi_details = {}
            for c in lesson_chars:
                lesson_hanzi_details[c] = hanzi_details.get(c, {
                    "strokes": "N/A",
                    "radical": "Đang cập nhật",
                    "pinyin": "",
                    "meaning": "Đang cập nhật",
                    "mnemonic": "Chưa có mẹo nhớ cho chữ này."
                })
            
            hanzi_json = json.dumps(lesson_hanzi_details, ensure_ascii=False)
            with open(f'game-hsk{level}-l{lesson_id}-hanzi.html', 'w', encoding='utf-8') as f:
                f.write(HANZI_TEMPLATE.format(level=level, level_label=level_label, lesson_id=lesson_id, hanzi_json=hanzi_json))

    print(f"Successfully generated HSK{level} game pages for {len(lessons)} lessons.")

if __name__ == "__main__":
    generate_hsk_games(1)
    generate_hsk_games(2)
    generate_hsk_games(3)
