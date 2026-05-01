import json
import re
import glob

def guess_pos(meaning, hanzi):
    m = meaning.lower()
    if hanzi in ['我', '你', '他', '她', '它', '我们', '你们', '他们', '她们', '大家', '自己', '这', '那', '哪', '谁', '什么', '哪儿', '这儿', '那儿', '怎么', '怎么样']: return 'Đại từ'
    if hanzi in ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '零', '两', '些']: return 'Số từ'
    if hanzi in ['个', '本', '杯', '块', '件', '次', '公斤', '度']: return 'Lượng từ'
    if hanzi in ['很', '太', '真', '最', '非常', '更', '都', '也', '还', '就', '才', '已经', '经常', '一直', '正在', '不', '没', '别']: return 'Phó từ'
    if hanzi in ['和', '跟', '因为', '所以', '虽然', '但是']: return 'Liên từ'
    if hanzi in ['在', '从', '到', '比', '离', '向', '往']: return 'Giới từ'
    if hanzi in ['的', '了', '吗', '呢', '吧', '啊', '得', '着', '过']: return 'Trợ từ'
    if hanzi in ['大', '小', '多', '少', '好', '坏', '冷', '热', '新', '旧', '高', '低', '远', '近', '长', '短', '贵', '便宜', '漂亮', '快', '慢', '白', '黑', '红', '晴', '阴', '错', '对']: return 'Tính từ'
    if hanzi in ['是', '有', '在', '吃', '喝', '去', '来', '买', '卖', '看', '听', '说', '读', '写', '做', '坐', '住', '学习', '工作', '睡觉', '打', '想', '要', '能', '会', '可以', '知道', '认识', '觉得', '希望', '准备', '开始', '帮助', '介绍', '跳舞', '唱歌', '运动', '旅游', '休息', '生病', '出院', '起床', '跑步', '洗', '穿', '进', '笑', '找', '等', '告诉', '让', '走', '问', '回答', '接', '送', '玩儿', '懂', '完']: return 'Động từ'
    
    if re.search(r'\b(tôi|bạn|anh|chị|nó|hắn|chúng|ai|gì|đâu)\b', m): return 'Đại từ'
    if re.search(r'\b(rất|quá|cũng|đều|đã|đang|sẽ|không|đừng|luôn|cực kỳ|hơi)\b', m): return 'Phó từ'
    if re.search(r'\b(và|nhưng|bởi vì|cho nên|hoặc|tuy)\b', m): return 'Liên từ'
    if re.search(r'\b(ở|tại|từ|đến|cho|đối với)\b', m): return 'Giới từ'
    if re.search(r'\b(tốt|xấu|to|nhỏ|nhiều|ít|đẹp|cao|thấp|mới|cũ|xa|gần|đắt|rẻ|nhanh|chậm|trắng|đen|đỏ)\b', m): return 'Tính từ'
    if re.search(r'\b(làm|ăn|uống|đi|chạy|nhảy|nhìn|thấy|nghe|nói|nghĩ|muốn|cần|biết|hiểu|học|mua|bán)\b', m): return 'Động từ'
    
    return 'Danh từ'

with open("generate_games.py", "r", encoding="utf-8") as f:
    gen_content = f.read()
match = re.search(r'FLIP_TEMPLATE\s*=\s*"""(.*?)"""', gen_content, re.DOTALL)
flip_template = match.group(1)

for filename in glob.glob("game-hsk*-flip.html"):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    match2 = re.search(r"let vocabData = (\[.*?\]);", content, re.DOTALL)
    if match2:
        vocab_json_str = match2.group(1)
        vocab_data = json.loads(vocab_json_str)
        
        # update POS
        for item in vocab_data:
            if 'type' not in item or not item['type']:
                item['type'] = guess_pos(item['meaning'], item['hanzi'])
                
        new_vocab_json_str = json.dumps(vocab_data, ensure_ascii=False)
        
        m_filename = re.match(r"game-hsk(\d+)-l(\d+)-flip\.html", filename)
        if m_filename:
            level = int(m_filename.group(1))
            lesson_id = int(m_filename.group(2))
            new_content = flip_template.format(level=level, lesson_id=lesson_id, vocab_json=new_vocab_json_str)
            with open(filename, "w", encoding="utf-8") as f2:
                f2.write(new_content)

print("Updated HTML files.")
