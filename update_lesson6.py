import json
import os
import subprocess

# Files
hsk1_path = 'hsk1_vocab_data.json'
hsk2_path = 'hsk2_vocab_data.json'

# Load HSK 1 data
with open(hsk1_path, 'r', encoding='utf-8') as f:
    hsk1_data = json.load(f)

# Load HSK 2 data
with open(hsk2_path, 'r', encoding='utf-8') as f:
    hsk2_data = json.load(f)

# 22 target words for HSK1 Lesson 6
target_words = [
    "手机", "电话", "号码", "明天", "去", "哪儿", "想", "超市", "买", 
    "东西", "些", "牛奶", "吃", "晚饭", "那边", "包子", "非常", "好吃", 
    "米饭", "怎么", "做", "出租车"
]

# Define missing words data (not found in HSK1 or HSK2)
new_words_data = {
    "电话": {
        "hanzi": "电话",
        "pinyin": "diànhuà",
        "meaning": "điện thoại",
        "lesson": "6",
        "type": "Danh từ",
        "ex_cn": "这是你的电话吗？",
        "ex_py": "Zhè shì nǐ de diànhuà ma?",
        "ex_vn": "Đây là điện thoại của bạn phải không?"
    },
    "号码": {
        "hanzi": "号码",
        "pinyin": "hàomǎ",
        "meaning": "số điện thoại, số",
        "lesson": "6",
        "type": "Danh từ",
        "ex_cn": "请告诉我你的电话号码。",
        "ex_py": "Qǐng gàosu wǒ nǐ de diànhuà hàomǎ.",
        "ex_vn": "Xin hãy cho tôi biết số điện thoại của bạn."
    },
    "去": {
        "hanzi": "去",
        "pinyin": "qù",
        "meaning": "đi",
        "lesson": "6",
        "type": "Động từ",
        "ex_cn": "你去哪儿？",
        "ex_py": "Nǐ qù nǎr?",
        "ex_vn": "Bạn đi đâu thế?"
    },
    "哪儿": {
        "hanzi": "哪儿",
        "pinyin": "nǎr",
        "meaning": "ở đâu, chỗ nào",
        "lesson": "6",
        "type": "Đại từ",
        "ex_cn": "超市在哪儿？",
        "ex_py": "Chāoshì zài nǎr?",
        "ex_vn": "Siêu thị ở đâu?"
    },
    "买": {
        "hanzi": "买",
        "pinyin": "mǎi",
        "meaning": "mua",
        "lesson": "6",
        "type": "Động từ",
        "ex_cn": "你想买什么？",
        "ex_py": "Nǐ xiǎng mǎi shénme?",
        "ex_vn": "Bạn muốn mua gì?"
    },
    "晚饭": {
        "hanzi": "晚饭",
        "pinyin": "wǎnfàn",
        "meaning": "bữa tối, cơm tối",
        "lesson": "6",
        "type": "Danh từ",
        "ex_cn": "我们去吃晚饭吧。",
        "ex_py": "Wǒmen qù chī wǎnfàn ba.",
        "ex_vn": "Chúng ta đi ăn tối đi."
    },
    "那边": {
        "hanzi": "那边",
        "pinyin": "nàbiān",
        "meaning": "phía bên kia, đằng kia",
        "lesson": "6",
        "type": "Danh từ",
        "ex_cn": "超市在那边。",
        "ex_py": "Chāoshì zài nàbiān.",
        "ex_vn": "Siêu thị ở đằng kia."
    },
    "米饭": {
        "hanzi": "米饭",
        "pinyin": "mǐfàn",
        "meaning": "cơm",
        "lesson": "6",
        "type": "Danh từ",
        "ex_cn": "我想吃米饭。",
        "ex_py": "Wǒ xiǎng chī mǐfàn.",
        "ex_vn": "Tôi muốn ăn cơm."
    }
}

# Update or move words
updated_hsk1 = []
updated_hsk2 = list(hsk2_data)

# To track which words from target_words have been processed
processed_words = set()

# Process existing HSK1 words
for item in hsk1_data:
    hz = item['hanzi']
    if hz in target_words:
        print(f"Updating '{hz}' in HSK1 to Lesson 6 (was Lesson {item.get('lesson')})")
        item['lesson'] = '6'
        processed_words.add(hz)
    elif item.get('lesson') == '6':
        # Move other HSK1 Lesson 6 words to lesson 0
        print(f"Moving non-target word '{hz}' from Lesson 6 to Lesson 0")
        item['lesson'] = '0'
    updated_hsk1.append(item)

# Process words from target_words that were not in HSK1
for word in target_words:
    if word in processed_words:
        continue
    
    # Check if word is in HSK2
    hsk2_match = None
    for item in updated_hsk2:
        if item['hanzi'] == word:
            hsk2_match = item
            break
            
    if hsk2_match:
        print(f"Moving '{word}' from HSK2 (was Lesson {hsk2_match.get('lesson')}) to HSK1 Lesson 6")
        updated_hsk2.remove(hsk2_match)
        hsk2_match['lesson'] = '6'
        updated_hsk1.append(hsk2_match)
    else:
        # Add new word
        if word in new_words_data:
            print(f"Adding new word '{word}' to HSK1 Lesson 6")
            updated_hsk1.append(new_words_data[word])
        else:
            print(f"Warning: word '{word}' not found in HSK1, HSK2, or new_words_data!")

# Write updated HSK1 and HSK2 files back
with open(hsk1_path, 'w', encoding='utf-8') as f:
    json.dump(updated_hsk1, f, ensure_ascii=False, indent=2)

with open(hsk2_path, 'w', encoding='utf-8') as f:
    json.dump(updated_hsk2, f, ensure_ascii=False, indent=2)

print("\nSaved updated HSK1 and HSK2 vocab files.")

# Rebuild all_hanzi.json based on all HSK levels in the directory
all_hanzi_chars = set()
for lvl in range(1, 7):
    vocab_file = f'hsk{lvl}_vocab_data.json'
    if os.path.exists(vocab_file):
        with open(vocab_file, 'r', encoding='utf-8') as f:
            v_data = json.load(f)
            for item in v_data:
                # Include all characters except spaces/punctuation if any
                for char in item['hanzi']:
                    if char.strip():
                        all_hanzi_chars.add(char)

# Save updated all_hanzi.json
all_hanzi_list = sorted(list(all_hanzi_chars))
with open('all_hanzi.json', 'w', encoding='utf-8') as f:
    json.dump(all_hanzi_list, f, ensure_ascii=False)
print(f"Saved updated all_hanzi.json containing {len(all_hanzi_list)} unique characters.")

# Run the game generator script
print("\nRunning generate_games.py to rebuild html games...")
res = subprocess.run(['python3', 'generate_games.py'], capture_output=True, text=True)
print("STDOUT:")
print(res.stdout)
print("STDERR:")
print(res.stderr)
