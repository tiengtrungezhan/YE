import json
import os
import sys

# Add the Hello directory to path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load vocab
with open('hsk5_vocab_data.json', 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

# Group by lesson
lessons = {}
for item in vocab_data:
    l_id = int(item['lesson'])
    if l_id not in lessons:
        lessons[l_id] = []
    lessons[l_id].append(item)

# Load all_hanzi
try:
    with open('all_hanzi.json', 'r', encoding='utf-8') as f:
        all_hanzi_json = f.read()
        all_hanzi_list = json.load(open('all_hanzi.json', 'r', encoding='utf-8'))
except:
    all_hanzi_json = "[]"
    all_hanzi_list = []

# Build cumulative hanzi from HSK1-4 + current lesson
def get_all_known_hanzi(lesson_vocab):
    chars = set()
    for item in lesson_vocab:
        for ch in item['hanzi']:
            chars.add(ch)
    # Also pull from lower HSK levels
    for lvl in range(1, 5):
        jf = f'hsk{lvl}_vocab_data.json'
        if os.path.exists(jf):
            with open(jf, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for item in data:
                for ch in item['hanzi']:
                    chars.add(ch)
    return "".join(chars)

# ============ TEMPLATES ============

FLIP_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lật Thẻ Thông Minh - HSK 5 Bài {lesson_id}</title>
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
        <a href="game-hsk5.html" class="back-btn">← Quay lại</a>
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
            <span id="cardCounter" style="font-size: 1.2rem; font-weight: bold; color: var(--text-color);">1 / {total}</span>
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
                            <strong>Từ loại:</strong> ${{word.type || 'Đang cập nhật'}}
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
            if(currentCardIndex > 0) {{ currentCardIndex--; renderCards(); }}
        }};

        window.nextCard = function() {{
            if(currentCardIndex < vocabData.length - 1) {{ currentCardIndex++; renderCards(); }}
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
            if (percent === 100) {{ mascotSpeech.innerText = "Tuyệt vời! Bạn đã thuộc hết rồi! 🏆"; celebration.style.display = 'flex'; }}
            else if (percent >= 50) mascotSpeech.innerText = "Sắp xong rồi, bạn học nhanh quá! 🚀";
            else if (percent > 0) mascotSpeech.innerText = "Giỏi lắm! Cố gắng lên nhé! 💪";
        }}

        window.toggleMaster = function(index, btn) {{
            if (masteredSet.has(index)) {{ masteredSet.delete(index); }} else {{ masteredSet.add(index); }}
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
    <title>Trùm Từ Vựng - HSK 5 Bài {lesson_id}</title>
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
        .typing-input:focus {{ border-color: var(--primary-color); outline: none; }}
        .submit-btn {{ padding: 1.2rem; background: var(--primary-color); color: white; border: none; border-radius: 15px; font-weight: 700; font-size: 1.1rem; cursor: pointer; width: 100%; transition: 0.3s; }}
        .submit-btn:hover {{ background: var(--primary-dark); transform: translateY(-2px); }}
        .result-screen {{ display: none; }}
        .score-circle {{ width: 150px; height: 150px; border-radius: 50%; border: 10px solid var(--primary-light); display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: 800; margin: 2rem auto; color: var(--primary-dark); }}
        .blank-text {{ font-size: 1.8rem; letter-spacing: 2px; color: var(--text-color); margin-bottom: 2rem; font-weight: bold; }}
        .blank-fill {{ color: var(--primary-color); border-bottom: 3px solid var(--primary-color); padding: 0 10px; min-width: 60px; display: inline-block; }}
    </style>
</head>
<body>
    <a href="index.html" class="home-logo-btn">
        <img src="mascot.png" alt="Home">
    </a>
    <div class="page-container">
        <a href="game-hsk5.html" class="back-btn">← Quay lại</a>
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
                </div>
            </div>
        </div>
    </div>
    <script>
        const vocabulary = {vocab_json};
        let currentQuestion = 0, score = 0, questions = [], totalQuestions = 0;

        function initGame() {{
            totalQuestions = Math.min(20, vocabulary.length);
            questions = generateQuestions();
            renderQuestion();
        }}

        function generateOptions(correctWord) {{
            let options = [correctWord];
            while (options.length < 4 && vocabulary.length >= 4) {{
                const rand = vocabulary[Math.floor(Math.random() * vocabulary.length)];
                if (!options.includes(rand)) options.push(rand);
            }}
            return options.sort(() => Math.random() - 0.5);
        }}

        function generateQuestions() {{
            let qs = [], shuffled = [...vocabulary].sort(() => Math.random() - 0.5);
            for (let i = 0; i < totalQuestions; i++) {{
                const word = shuffled[i % shuffled.length];
                const type = Math.floor(Math.random() * 3);
                let q = {{ type, word }};
                q.options = generateOptions(word);
                qs.push(q);
            }}
            return qs;
        }}

        function renderQuestion() {{
            const q = questions[currentQuestion];
            const card = document.getElementById('quiz-card');
            const progress = document.getElementById('progress');
            progress.style.width = (currentQuestion / totalQuestions) * 100 + '%';
            document.getElementById('progress-text').innerText = (currentQuestion + 1) + '/' + totalQuestions;

            let html = '';
            if (q.type === 0) {{
                html = `<div class="question-text">Nghe và chọn từ đúng:</div><button style="background:#fdf2f8;border:none;font-size:3rem;cursor:pointer;margin-bottom:1rem;" onclick="speak('${{q.word.hanzi}}')">🔊</button><div class="options-grid">${{q.options.map(opt => `<button class="option-btn" onclick="checkAnswer('${{opt.hanzi}}','${{q.word.hanzi}}',this)">${{opt.hanzi}}</button>`).join('')}}</div>`;
                setTimeout(() => speak(q.word.hanzi), 500);
            }} else if (q.type === 1) {{
                html = `<div class="question-text">Từ "${{q.word.hanzi}}" có nghĩa là gì?</div><div class="options-grid">${{q.options.map(opt => `<button class="option-btn" onclick="checkAnswer('${{opt.meaning}}','${{q.word.meaning}}',this)">${{opt.meaning}}</button>`).join('')}}</div>`;
            }} else {{
                html = `<div class="question-text">Từ "${{q.word.hanzi}}" có phiên âm là gì?</div><div class="options-grid">${{q.options.map(opt => `<button class="option-btn" onclick="checkAnswer('${{opt.pinyin}}','${{q.word.pinyin}}',this)">${{opt.pinyin}}</button>`).join('')}}</div>`;
            }}
            card.innerHTML = html;
        }}

        function speak(t) {{ const m = new SpeechSynthesisUtterance(); m.text = t; m.lang = 'zh-CN'; window.speechSynthesis.speak(m); }}

        function checkAnswer(s, c, b) {{
            const btns = document.querySelectorAll('.option-btn');
            btns.forEach(x => x.disabled = true);
            if (s === c) {{ b.classList.add('correct'); score++; }}
            else {{ b.classList.add('wrong'); btns.forEach(x => {{ if(x.innerText === c || x.innerText.trim() === c) x.classList.add('correct'); }}); }}
            showNext();
        }}

        function showNext() {{
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

# Generate files for each lesson
for lesson_id, vocab_list in lessons.items():
    vocab_json = json.dumps(vocab_list, ensure_ascii=False)
    total = len(vocab_list)

    # Flip Page
    with open(f'game-hsk5-l{lesson_id}-flip.html', 'w', encoding='utf-8') as f:
        f.write(FLIP_TEMPLATE.format(lesson_id=lesson_id, vocab_json=vocab_json, total=total))
    print(f"  ✓ game-hsk5-l{lesson_id}-flip.html")

    # Master Page
    with open(f'game-hsk5-l{lesson_id}-master.html', 'w', encoding='utf-8') as f:
        f.write(MASTER_TEMPLATE.format(lesson_id=lesson_id, vocab_json=vocab_json))
    print(f"  ✓ game-hsk5-l{lesson_id}-master.html")

print(f"\n✅ Done! Generated games for {len(lessons)} lesson(s): {sorted(lessons.keys())}")
