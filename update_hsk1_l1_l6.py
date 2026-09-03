import urllib.request
import urllib.parse
import csv
import io
import json
import re

SHEET_ID = '1aDXa1SZXrdOI69dx6eKgJu-ItPwWY26nZrdUD3ZeQGI'

DEFAULT_TYPES = {
    '谢谢': 'Động từ',
    '不客气': 'Cụm từ',
    '再见': 'Cụm từ',
    '请问': 'Cụm từ',
    '是不是': 'Cụm từ',
    '对不起': 'Cụm từ',
    '没关系': 'Cụm từ',
    '没事': 'Cụm từ',
    '喂': 'Thán từ',
    '没有': 'Động từ',
    '多少': 'Đại từ',
    '几': 'Đại từ',
    '一些': 'Lượng từ',
    '里': 'Danh từ'
}

def parse_example(ex_str):
    ex_str = ex_str.strip()
    if not ex_str:
        return '', '', ''

    # Handle special case: '谢谢你 - 不客气。xièxie nǐ - bú kèqi. (Cảm ơn bạn - Không có gì)'
    if ' - ' in ex_str and '(' in ex_str and ')' in ex_str:
        m_spec = re.match(r'^(.*?)\s*[\(（](.*?)[\)）]$', ex_str)
        if m_spec:
            cn_py_part, vn_part = m_spec.groups()
            m_cn_py = re.search(r'([a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ\s\!\?\,\.\:\;\’\'-]+)$', cn_py_part, re.IGNORECASE)
            if m_cn_py:
                py = m_cn_py.group(1).strip()
                cn = cn_py_part[:m_cn_py.start()].strip()
                return cn, py, vn_part.strip()

    # Case A: Hanzi (Pinyin) - Meaning  OR  Hanzi (Pinyin) (Meaning)
    mA = re.match(r'^([\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\s\d\w\.\,\!\?\:\;\“\”\‘\’\…\—\–\-]+?)[\(（]([a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ\s\!\?\,\.\:\;\’\'-]+)[\)）]\s*(?:[-–—]\s*)?[\(（]?([^\(\)（）]+)[\)）]?$', ex_str, re.IGNORECASE)
    if mA:
        cn, py, vn = mA.groups()
        return cn.strip(), py.strip(), vn.strip(' -()（）')

    # Case B: Hanzi Pinyin (Meaning) where Pinyin is directly after Hanzi punctuation or space
    mB = re.match(r'^([\u4e00-\u9fff\u3000-\u303f\uff01-\uff0f\uff1a-\uff20\uff3b-\uff40\uff5b-\uff65\s\d]+?)\s*([a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ\s\!\?\,\.\:\;\’\'-]+?)\s*[\(（](.*?)[\)）]$', ex_str, re.IGNORECASE)
    if mB:
        cn, py, vn = mB.groups()
        return cn.strip(), py.strip(), vn.strip(' -()（）')

    # Case C: Fallback regex to split Hanzi, Pinyin, Vietnamese
    mC = re.match(r'^(.*?)\s*([\(（].*?[\)）])?\s*[-–—]?\s*(.*)$', ex_str)
    if mC:
        cn, py, vn = mC.groups()
        py = py.strip('()（）') if py else ''
        return cn.strip(), py.strip(), vn.strip(' -()（）')

    return ex_str, '', ''

def fetch_lesson_data(lesson_num):
    sheet_name = f'BÀI {lesson_num}'
    encoded_name = urllib.parse.quote(sheet_name)
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_name}'
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8')

    reader = list(csv.reader(io.StringIO(content)))
    words = []
    
    for row in reader[1:]:
        if not any(row):
            continue
        stt, hanzi, pinyin, pos, meaning, ex, *rest = (row + ['']*7)[:7]
        hanzi = hanzi.strip()
        if not hanzi or hanzi == 'HÁN TỰ':
            continue
            
        pinyin = pinyin.strip()
        pos = pos.strip()
        if not pos and hanzi in DEFAULT_TYPES:
            pos = DEFAULT_TYPES[hanzi]
            
        meaning = meaning.strip()
        ex = ex.strip()
        
        ex_cn, ex_py, ex_vn = parse_example(ex)
        
        words.append({
            "hanzi": hanzi,
            "pinyin": pinyin,
            "meaning": meaning,
            "lesson": str(lesson_num),
            "type": pos,
            "ex_cn": ex_cn,
            "ex_py": ex_py,
            "ex_vn": ex_vn
        })
        
    return words

def main():
    print("=== Fetching HSK1 Lessons 1 to 6 from Google Sheet ===")
    
    new_l1_l6_words = []
    for l in range(1, 7):
        words = fetch_lesson_data(l)
        print(f"  Lesson {l}: fetched {len(words)} words.")
        new_l1_l6_words.extend(words)
        
    print(f"Total fetched for Lessons 1-6: {len(new_l1_l6_words)} words.")

    # Load existing hsk1_vocab_data.json
    with open('hsk1_vocab_data.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)

    # Retain words from lessons 7 and above
    other_lessons_words = [item for item in existing_data if str(item.get('lesson', '')) not in {'1', '2', '3', '4', '5', '6'}]
    print(f"Preserved {len(other_lessons_words)} words from lessons 7+.")

    # Combine new L1-L6 words with existing L7+ words
    updated_data = new_l1_l6_words + other_lessons_words

    with open('hsk1_vocab_data.json', 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Successfully updated hsk1_vocab_data.json! Total words: {len(updated_data)}")

if __name__ == '__main__':
    main()
