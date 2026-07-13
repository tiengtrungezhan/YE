import json
import os

words = [
    "四", "妈妈", "六", "妹妹", "两", "几", "岁", "多大", "没", "女儿", "他", "是的", "弟弟", "和", "今天", "九"
]

hsk1_path = 'hsk1_vocab_data.json'
with open(hsk1_path, 'r', encoding='utf-8') as f:
    hsk1 = json.load(f)

for w in words:
    matches = []
    for item in hsk1:
        if w in item['hanzi']:
            matches.append(f"{item['hanzi']} ({item['pinyin']}: {item['meaning']})")
    if matches:
        print(f"Substrings of '{w}' in HSK1:")
        for m in matches:
            print(f"  - {m}")
    else:
        print(f"No match for '{w}' in HSK1")
