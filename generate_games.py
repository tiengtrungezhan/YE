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
    <title>Lật Thẻ Thông Minh - HSK {level} Bài {lesson_id}</title>
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
        .card-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 2rem; margin-top: 2rem; }}
        .flip-card {{ background-color: transparent; width: 100%; height: 320px; perspective: 1000px; cursor: pointer; }}
        .flip-card-inner {{ position: relative; width: 100%; height: 100%; text-align: center; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); transform-style: preserve-3d; }}
        .flip-card.flipped .flip-card-inner {{ transform: rotateY(180deg); }}
        .flip-card-front, .flip-card-back {{ 
            position: absolute; width: 100%; height: 100%; backface-visibility: hidden; 
            display: flex; flex-direction: column; border-radius: 30px; padding: 1.2rem; 
            border: 2px solid var(--primary-light); background: white;
            box-shadow: 0 10px 30px rgba(165, 207, 218, 0.2);
        }}
        .flip-card-front {{ justify-content: center; align-items: center; }}
        .flip-card-front .hanzi {{ font-size: 4.5rem; font-weight: 800; color: var(--primary-dark); transition: transform 0.3s; }}
        .flip-card:hover .hanzi {{ transform: scale(1.1); }}
        .flip-card-back {{ transform: rotateY(180deg); text-align: left; background: #fff; border-color: var(--primary-color); }}
        .flip-card.mastered .flip-card-front, .flip-card.mastered .flip-card-back {{ border-color: #ffd700; background: #fffdf0; }}
        .master-badge {{ position: absolute; top: 15px; right: 15px; font-size: 1.5rem; display: none; z-index: 5; }}
        .flip-card.mastered .master-badge {{ display: block; animation: pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); }}
        @keyframes pop {{ from {{ transform: scale(0); }} to {{ transform: scale(1); }} }}
        .back-header {{ width: 100%; display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; border-bottom: 1px solid #eee; padding-bottom: 0.5rem; }}
        .back-hanzi {{ font-size: 1.8rem; font-weight: 800; color: var(--primary-dark); }}
        .back-pinyin {{ font-size: 1.1rem; color: #e67e22; font-weight: 700; }}
        .btn-speak {{ background: var(--primary-light); border: none; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.3s; }}
        .btn-speak:hover {{ background: var(--primary-color); transform: scale(1.1); }}
        .back-meaning {{ font-size: 1.2rem; font-weight: 700; color: #444; }}
        .back-example {{ font-size: 0.8rem; background: #f9f9f9; padding: 0.6rem; border-radius: 12px; margin-top: 0.5rem; line-height: 1.3; }}
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
    <div class="page-container">
        <header class="game-header">
            <a href="game-hsk{level}.html" class="back-btn" style="position: absolute; left: 0; top: 0;">← Quay lại</a>
            <h1 style="color: var(--primary-dark); font-size: 2.2rem;">Lật Thẻ Thông Minh</h1>
            <p>Bài {lesson_id} - Khám phá từ vựng</p>
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
        <div class="card-grid" id="cardGrid"></div>
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
        totalCountEl.innerText = vocabData.length;

        function renderCards() {{
            grid.innerHTML = '';
            vocabData.forEach((word, index) => {{
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
                                <span class="back-hanzi" style="font-size:1.4rem">${{word.hanzi}}</span>
                                <span class="back-pinyin">${{word.pinyin}}</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.5rem;">
                                <button class="btn-speak" onclick="event.stopPropagation(); speak('${{word.hanzi}}')">🔊</button>
                                <div class="back-meaning">${{word.meaning}}</div>
                            </div>
                            <div class="back-example">
                                <strong style="font-size: 0.75rem; color: var(--primary-dark);">Ví dụ:</strong>
                                <div style="margin-top:2px">${{word.ex_cn || word.hanzi}}</div>
                                <div style="color: #e67e22; font-style: italic; font-size: 0.7rem;">${{word.ex_py || word.pinyin}}</div>
                                <div style="color: #666; font-size: 0.7rem; border-top: 1px dashed #eee; margin-top:2px;">${{word.ex_vn || word.meaning}}</div>
                            </div>
                            <button class="master-btn ${{masteredSet.has(index) ? 'active' : ''}}" onclick="event.stopPropagation(); toggleMaster(${{index}}, this)">
                                ${{masteredSet.has(index) ? 'Bỏ thuộc' : 'Đã thuộc'}}
                            </button>
                        </div>
                    </div>`;
                card.addEventListener('click', () => card.classList.toggle('flipped'));
                grid.appendChild(card);
            }});
        }}

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
            renderCards();
            updateProgress();
        }};

        window.resetProgress = function() {{
            masteredSet.clear();
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
    <title>Trùm Từ Vựng - HSK {level} Bài {lesson_id}</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        body {{ background: #fdf2f8; }}
        .game-wrapper {{ max-width: 600px; margin: 0 auto; padding: 2rem; text-align: center; }}
        .quiz-card {{ background: var(--white); border-radius: 30px; padding: 3rem 2rem; box-shadow: var(--shadow); margin-top: 2rem; min-height: 400px; display: flex; flex-direction: column; justify-content: center; position: relative; }}
        .progress-container {{ width: 100%; height: 8px; background: #eee; border-radius: 4px; margin-bottom: 2rem; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: var(--primary-color); width: 0%; transition: width 0.3s; }}
        .question-text {{ font-size: 1.5rem; font-weight: 700; color: var(--text-color); margin-bottom: 2rem; }}
        .options-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem; }}
        .option-btn {{ padding: 1.2rem; background: #f8fbfe; border: 2px solid #eef2f5; border-radius: 15px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: 0.2s; }}
        .option-btn:hover {{ border-color: var(--primary-color); background: #f0f7f9; }}
        .option-btn.correct {{ background: #d4edda; border-color: #28a745; color: #155724; }}
        .option-btn.wrong {{ background: #f8d7da; border-color: #dc3545; color: #721c24; }}
        .audio-btn {{ background: var(--primary-light); width: 80px; height: 80px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 2rem; cursor: pointer; margin-bottom: 2rem; border: none; }}
        .typing-input {{ width: 100%; padding: 1.2rem; border: 2px solid #ddd; border-radius: 15px; font-size: 1.5rem; text-align: center; margin-bottom: 1.5rem; }}
        .submit-btn {{ padding: 1rem 2rem; background: var(--primary-color); color: white; border: none; border-radius: 12px; font-weight: 700; cursor: pointer; width: 100%; }}
        .result-screen {{ display: none; }}
        .score-circle {{ width: 150px; height: 150px; border-radius: 50%; border: 10px solid var(--primary-light); display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: 800; margin: 2rem auto; color: var(--primary-dark); }}
    </style>
</head>
<body>
    <div class="page-container">
        <a href="game-hsk{level}.html" class="back-btn">← Quay lại</a>
        <div class="game-wrapper">
            <div id="game-ui">
                <div class="progress-container"><div class="progress-fill" id="progress"></div></div>
                <div class="quiz-card" id="quiz-card"></div>
            </div>
            <div id="result-ui" class="result-screen">
                <div class="quiz-card">
                    <h1 style="color: var(--primary-dark);">Kết Quả</h1>
                    <div class="score-circle" id="final-score">0%</div>
                    <p id="score-text"></p>
                    <button class="submit-btn" style="margin-top: 2rem;" onclick="location.reload()">Chơi Lại</button>
                    <a href="game-hsk{level}-l{lesson_id}-match.html" class="submit-btn" style="margin-top: 1rem; background: #e65100; text-decoration: none; display: block; line-height: 1.5; padding: 1rem 0;">Thử thách Ghép Đôi</a>
                </div>
            </div>
        </div>
    </div>
    <script>
        const vocabulary = {vocab_json};
        let currentQuestion = 0, score = 0, questions = [], totalQuestions = 0;
        function initGame() {{ 
            totalQuestions = Math.min(60, Math.max(20, vocabulary.length * 2));
            questions = generateQuestions(); 
            renderQuestion(); 
        }}
        function generateQuestions() {{
            let qs = [], shuffled = [...vocabulary].sort(() => Math.random() - 0.5);
            for (let i = 0; i < totalQuestions; i++) {{
                const word = shuffled[i % shuffled.length];
                let availableTypes = [0, 1, 2, 3];
                
                if (word.ex_cn && word.ex_cn.length > 2) {{
                    let isAllowed = true;
                    if ({level} === 1 && parseInt('{lesson_id}') < 4) isAllowed = false;
                    
                    if (isAllowed) {{
                        let cleanSentence = word.ex_cn.replace(/[，。？！、\s]/g, '');
                        const cumulativeChars = "{cumulative_chars}";
                        for (let c of cleanSentence) {{
                            if (!cumulativeChars.includes(c)) {{
                                isAllowed = false;
                                break;
                            }}
                        }}
                    }}
                    
                    if (isAllowed) availableTypes.push(5);
                }}
                
                const type = availableTypes[Math.floor(Math.random() * availableTypes.length)];
                let q = {{ type, word }};
                
                if (type === 0 || type === 1 || type === 2) q.options = generateOptions(word, type);
                if (type === 5) {{
                    let cleanSentence = word.ex_cn.replace(/[，。？！、\s]/g, '');
                    q.chars = cleanSentence.split('').sort(() => Math.random() - 0.5);
                    q.correctSentence = cleanSentence;
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
            let html = '';
            if (q.type === 0) {{
                html = `<div class="question-text">Nghe và chọn từ đúng:</div><button class="audio-btn" onclick="speak('${{q.word.hanzi}}')">🔊</button><div class="options-grid">${{q.options.map(opt => `<button class="option-btn" onclick="checkAnswer('${{opt.hanzi}}', '${{q.word.hanzi}}', this)">${{opt.hanzi}}</button>`).join('')}}</div>`;
                setTimeout(() => speak(q.word.hanzi), 500);
            }} else if (q.type === 1) {{
                html = `<div class="question-text">Từ "${{q.word.hanzi}}" có nghĩa là gì?</div><div class="options-grid">${{q.options.map(opt => `<button class="option-btn" onclick="checkAnswer('${{opt.meaning}}', '${{q.word.meaning}}', this)">${{opt.meaning}}</button>`).join('')}}</div>`;
            }} else if (q.type === 2) {{
                html = `<div class="question-text">Từ "${{q.word.hanzi}}" có phiên âm là gì?</div><div class="options-grid">${{q.options.map(opt => `<button class="option-btn" onclick="checkAnswer('${{opt.pinyin}}', '${{q.word.pinyin}}', this)">${{opt.pinyin}}</button>`).join('')}}</div>`;
            }} else if (q.type === 3) {{
                html = `<div class="question-text">"${{q.word.meaning}}" trong tiếng Trung viết là gì?</div><div class="input-area"><input type="text" class="typing-input" id="typing-ans" placeholder="Nhập chữ Hán..."><button class="submit-btn" onclick="checkTyping('${{q.word.hanzi}}')">Gửi</button></div>`;
            }} else if (q.type === 5) {{
                html = `<div class="question-text">Sắp xếp thành câu đúng:</div><div style="color: #666; margin-bottom: 1.5rem; font-size: 1.1rem;">Nghĩa: ${{q.word.ex_vn || q.word.meaning}}</div><div id="drop-zone" style="min-height: 70px; padding: 1rem; border: 2px dashed #ccc; border-radius: 15px; margin-bottom: 1.5rem; display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; align-items: center;"></div><div id="drag-zone" style="display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center;">${{q.chars.map((char, i) => `<button class="option-btn" style="padding: 0.8rem 1.2rem; font-size: 1.5rem;" onclick="moveChar(this, '${{q.correctSentence}}')">${{char}}</button>`).join('')}}</div>`;
            }}
            card.innerHTML = html;
        }}
        function speak(t) {{ const m = new SpeechSynthesisUtterance(); m.text = t; m.lang = 'zh-CN'; window.speechSynthesis.speak(m); }}
        function checkAnswer(s, c, b) {{
            document.querySelectorAll('.option-btn').forEach(x => x.disabled = true);
            if (s === c) {{ b.classList.add('correct'); score++; }} else {{ b.classList.add('wrong'); document.querySelectorAll('.option-btn').forEach(x => {{ if(x.innerText===c) x.classList.add('correct'); }}); }}
            showNextButton();
        }}
        function checkTyping(c) {{
            const i = document.getElementById('typing-ans'), v = i.value.trim();
            if (v === c) {{ i.style.borderColor = "#28a745"; score++; }} else {{ i.style.borderColor = "#dc3545"; alert('Đáp án đúng: ' + c); }}
            showNextButton();
        }}
        function moveChar(btn, correctSentence) {{
            const dropZone = document.getElementById('drop-zone');
            if (btn.parentElement.id === 'drag-zone') {{
                dropZone.appendChild(btn);
            }} else {{
                document.getElementById('drag-zone').appendChild(btn);
            }}
            
            let currentStr = Array.from(dropZone.children).map(c => c.innerText).join('');
            if (document.getElementById('drag-zone').children.length === 0) {{
                if (currentStr === correctSentence) {{
                    dropZone.style.borderColor = '#28a745';
                    dropZone.style.backgroundColor = '#d4edda';
                    score++;
                }} else {{
                    dropZone.style.borderColor = '#dc3545';
                    dropZone.style.backgroundColor = '#f8d7da';
                    let alertDiv = document.createElement('div');
                    alertDiv.style = "color: #dc3545; font-weight: bold; margin-top: 1rem;";
                    alertDiv.innerText = "Sai rồi! Câu đúng là: " + correctSentence;
                    document.getElementById('quiz-card').appendChild(alertDiv);
                }}
                showNextButton();
            }}
        }}
        function showNextButton() {{
            if (!document.getElementById('next-btn')) {{
                document.getElementById('quiz-card').insertAdjacentHTML('beforeend', '<button id="next-btn" class="submit-btn" style="margin-top: 1.5rem; background: #17a2b8;" onclick="next()">Tiếp Tục ➡</button>');
            }}
        }}
        function next() {{ currentQuestion++; if (currentQuestion < totalQuestions) renderQuestion(); else showResults(); }}
        function showResults() {{ document.getElementById('game-ui').style.display = 'none'; document.getElementById('result-ui').style.display = 'block'; document.getElementById('final-score').innerText = Math.round((score/totalQuestions)*100)+'%'; document.getElementById('score-text').innerText = `Bạn đúng ${{score}}/${{totalQuestions}} câu.`; }}
        initGame();
    </script>
</body>
</html>"""

    MATCH_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Truy Tìm Cặp Đôi - HSK {level} Bài {lesson_id}</title>
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
    <title>Siêu Trí Nhớ - HSK {level} Bài {lesson_id}</title>
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
    <div class="page-container">
        <header class="game-header">
            <a href="game-hsk{level}.html" class="back-btn" style="position: absolute; left: 0; top: 0;">← Quay lại</a>
            <h1 style="color: var(--primary-dark); font-size: 2.2rem;">Siêu Trí Nhớ 🧠</h1>
            <p>HSK {level} Bài {lesson_id}: Nghe và kể lại bài khóa</p>
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

        initSelector();
        loadDialog(0);
    </script>
</body>
</html>"""

    # Load Dialogues if HSK2
    dialog_data = []
    if level == 2 and os.path.exists('hsk2_dialogs.json'):
        with open('hsk2_dialogs.json', 'r', encoding='utf-8') as df:
            dialog_data = json.load(df)

    # Generate files
    for lesson_id, vocab_list in lessons.items():
        vocab_json = json.dumps(vocab_list, ensure_ascii=False)
        
        # Flip Page
        with open(f'game-hsk{level}-l{lesson_id}-flip.html', 'w', encoding='utf-8') as f:
            f.write(FLIP_TEMPLATE.format(level=level, lesson_id=lesson_id, vocab_json=vocab_json))
        
        # Master Page
        cumulative_chars = get_cumulative_chars(level, int(lesson_id))
        with open(f'game-hsk{level}-l{lesson_id}-master.html', 'w', encoding='utf-8') as f:
            f.write(MASTER_TEMPLATE.format(level=level, lesson_id=lesson_id, vocab_json=vocab_json, cumulative_chars=cumulative_chars))

        # Match Page (HSK 1 and HSK 2 only)
        if level <= 2:
            with open(f'game-hsk{level}-l{lesson_id}-match.html', 'w', encoding='utf-8') as f:
                f.write(MATCH_TEMPLATE.format(level=level, lesson_id=lesson_id, vocab_json=vocab_json))

        # Memory Page (HSK 2 only for now)
        if level == 2:
            lesson_dialogs = next((item['dialogs'] for item in dialog_data if item['lesson'] == lesson_id), [])
            if lesson_dialogs:
                dialog_json = json.dumps(lesson_dialogs, ensure_ascii=False)
                with open(f'game-hsk{level}-l{lesson_id}-memory.html', 'w', encoding='utf-8') as f:
                    f.write(MEMORY_TEMPLATE.format(level=level, lesson_id=lesson_id, dialog_json=dialog_json))

    print(f"Successfully generated HSK{level} game pages for {len(lessons)} lessons.")

if __name__ == "__main__":
    generate_hsk_games(1)
    generate_hsk_games(2)
