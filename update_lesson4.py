import json
import os

# Define file paths
hsk1_path = 'hsk1_vocab_data.json'
hsk2_path = 'hsk2_vocab_data.json'

# Load HSK 1 data
with open(hsk1_path, 'r', encoding='utf-8') as f:
    hsk1_data = json.load(f)

# Load HSK 2 data
with open(hsk2_path, 'r', encoding='utf-8') as f:
    hsk2_data = json.load(f)

print(f"Loaded {len(hsk1_data)} words from HSK1 and {len(hsk2_data)} words from HSK2.")

# 1. Update '多少' in HSK1 to Lesson 4
found_duoshao = False
for item in hsk1_data:
    if item['hanzi'] == '多少':
        print(f"Moving '多少' from Lesson {item['lesson']} to Lesson 4")
        item['lesson'] = '4'
        item['type'] = 'Đại từ'  # Update type to Pronoun (Đại từ) which is more accurate than Danh từ
        found_duoshao = True
        break

if not found_duoshao:
    # If not found in HSK1, create it
    print("Adding '多少' as a new word to HSK1 Lesson 4")
    hsk1_data.append({
        "hanzi": "多少",
        "pinyin": "duōshao",
        "meaning": "bao nhiêu",
        "lesson": "4",
        "type": "Đại từ",
        "ex_cn": "这件衣服多少钱？",
        "ex_py": "Zhè jiàn yīfu duōshao qián?",
        "ex_vn": "Chiếc áo này bao nhiêu tiền?"
    })

# 2. Find '零' in HSK2, remove it, and add to HSK1 Lesson 4
ling_item = None
for item in hsk2_data:
    if item['hanzi'] == '零':
        ling_item = item
        break

if ling_item:
    print(f"Removing '零' from HSK2 (was Lesson {ling_item['lesson']})")
    hsk2_data.remove(ling_item)
    ling_item['lesson'] = '4'
    
    # Check if '零' already exists in HSK1 (to prevent duplicates)
    exists_in_hsk1 = any(item['hanzi'] == '零' for item in hsk1_data)
    if not exists_in_hsk1:
        print("Adding '零' to HSK1 Lesson 4")
        hsk1_data.append(ling_item)
    else:
        print("'零' already exists in HSK1, updating its lesson to 4")
        for item in hsk1_data:
            if item['hanzi'] == '零':
                item['lesson'] = '4'
else:
    # If '零' not found in HSK2, check HSK1 or create it
    exists_in_hsk1 = False
    for item in hsk1_data:
        if item['hanzi'] == '零':
            print("Found '零' in HSK1, updating lesson to 4")
            item['lesson'] = '4'
            exists_in_hsk1 = True
            break
    if not exists_in_hsk1:
        print("Creating and adding '零' to HSK1 Lesson 4")
        hsk1_data.append({
            "hanzi": "零",
            "pinyin": "líng",
            "meaning": "số không",
            "lesson": "4",
            "type": "Số từ",
            "ex_cn": "今天零度。",
            "ex_py": "Jīntiān líng dù.",
            "ex_vn": "Hôm nay không độ."
        })

# 3. Add '一' to HSK1 Lesson 4 if not exists
exists_yi = False
for item in hsk1_data:
    if item['hanzi'] == '一':
        print(f"Found '一' in HSK1, moving to Lesson 4 (was Lesson {item['lesson']})")
        item['lesson'] = '4'
        exists_yi = True
        break

if not exists_yi:
    print("Adding '一' to HSK1 Lesson 4")
    hsk1_data.append({
        "hanzi": "一",
        "pinyin": "yī",
        "meaning": "số 1",
        "lesson": "4",
        "type": "Số từ",
        "ex_cn": "一、二、三。",
        "ex_py": "Yī, èr, sān.",
        "ex_vn": "Một, hai, ba."
    })

# 4. Add '二' to HSK1 Lesson 4 if not exists
exists_er = False
for item in hsk1_data:
    if item['hanzi'] == '二':
        print(f"Found '二' in HSK1, moving to Lesson 4 (was Lesson {item['lesson']})")
        item['lesson'] = '4'
        exists_er = True
        break

if not exists_er:
    print("Adding '二' to HSK1 Lesson 4")
    hsk1_data.append({
        "hanzi": "二",
        "pinyin": "èr",
        "meaning": "số 2",
        "lesson": "4",
        "type": "Số từ",
        "ex_cn": "一、二、三。",
        "ex_py": "Yī, èr, sān.",
        "ex_vn": "Một, hai, ba."
    })

# Save updated HSK 1 data
with open(hsk1_path, 'w', encoding='utf-8') as f:
    json.dump(hsk1_data, f, ensure_ascii=False, indent=2)

# Save updated HSK 2 data
with open(hsk2_path, 'w', encoding='utf-8') as f:
    json.dump(hsk2_data, f, ensure_ascii=False, indent=2)

print("\nSaved updated JSON files.")
print(f"HSK1 now has {len(hsk1_data)} words.")
print(f"HSK2 now has {len(hsk2_data)} words.")

# Verify HSK1 Lesson 4 words
lesson4_words = [item for item in hsk1_data if item.get('lesson') == '4']
print(f"\nLesson 4 now has {len(lesson4_words)} words:")
for item in sorted(lesson4_words, key=lambda x: x['hanzi']):
    print(f"  - {item['hanzi']} ({item['pinyin']}): {item['meaning']} [Type: {item['type']}]")
