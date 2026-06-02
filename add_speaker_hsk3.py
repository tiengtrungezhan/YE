#!/usr/bin/env python3
"""
Thêm nút loa 🔊 vào câu dịch Việt-Trung (type 11) trong tất cả file game-hsk3-lX-master.html
"""
import os
import re
import glob

FOLDER = "/Users/tranthutrang/Documents/Hello"

# Dòng cần tìm (type 11 render)
OLD = (
    "} else if (q.type === 11) {\n"
    "                html = `<div class=\"question-text\">Dịch câu sau sang tiếng Trung:</div>"
    "<div class=\"sub-text\" style=\"font-size: 1.4rem; color: var(--primary-dark);\">"
    "${q.word.ex_vn}</div>"
    "<input type=\"text\" class=\"typing-input\" id=\"typing-ans\" placeholder=\"Nhập câu tiếng Trung...\">"
    "<button class=\"submit-btn\" onclick=\"checkTyping('${q.word.ex_cn.replace(/[，。？！\\s]/g, '')}')\">"
    "Gửi đáp án</button>`;"
)

NEW = (
    "} else if (q.type === 11) {\n"
    "                html = `<div class=\"question-text\">Dịch câu sau sang tiếng Trung:</div>"
    "<div class=\"sub-text\" style=\"font-size: 1.4rem; color: var(--primary-dark); display: flex; align-items: center; justify-content: center; gap: 0.8rem;\">"
    "${q.word.ex_vn}"
    "<button onclick=\"speakVN('${q.word.ex_vn.replace(/'/g, \\\"\\\\'\\\")}')\""
    " style=\"background: none; border: 2px solid var(--primary-color); border-radius: 50%; width: 42px; height: 42px; font-size: 1.3rem; cursor: pointer; flex-shrink: 0; display: flex; align-items: center; justify-content: center; transition: 0.2s;\" "
    "onmouseover=\"this.style.background='var(--primary-light)'\" onmouseout=\"this.style.background='none'\" "
    "title=\"Nghe câu tiếng Việt\">🔊</button>"
    "</div>"
    "<input type=\"text\" class=\"typing-input\" id=\"typing-ans\" placeholder=\"Nhập câu tiếng Trung...\">"
    "<button class=\"submit-btn\" onclick=\"checkTyping('${q.word.ex_cn.replace(/[，。？！\\s]/g, '')}')\">"
    "Gửi đáp án</button>`;"
)

# Hàm speakVN cần thêm vào nếu chưa có
SPEAK_VN_FN = """
        function speakVN(t) { const m = new SpeechSynthesisUtterance(); m.text = t; m.lang = 'vi-VN'; window.speechSynthesis.cancel(); window.speechSynthesis.speak(m); }"""

files = sorted(glob.glob(os.path.join(FOLDER, "game-hsk3-l*-master.html")))
print(f"Found {len(files)} files to process...\n")

updated = 0
skipped = 0

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Kiểm tra xem đã có speakVN chưa
    has_speak_vn = "speakVN" in content
    
    # Tìm type 11 block bằng regex linh hoạt hơn
    pattern = (
        r"(\}\s*else if \(q\.type === 11\) \{[\s\S]*?)"
        r"(Dịch câu sau sang tiếng Trung:.*?</div>)"
        r"(<div class=\"sub-text\"[^>]*>)"
        r"(\$\{q\.word\.ex_vn\})"
        r"(</div>)"
    )
    
    def replacer(m):
        return (
            m.group(1) +
            m.group(2) +
            '<div class="sub-text" style="font-size: 1.4rem; color: var(--primary-dark); display: flex; align-items: center; justify-content: center; gap: 0.8rem;">' +
            m.group(4) +
            '<button onclick="speakVN(\\\'${q.word.ex_vn.replace(/\\\'/g, \\\\\\\'\\\\\\\\\\\\\\\'\\\\\\\')}\\\')" '
            'style="background: none; border: 2px solid var(--primary-color); border-radius: 50%; width: 42px; height: 42px; font-size: 1.3rem; cursor: pointer; flex-shrink: 0; display: flex; align-items: center; justify-content: center; transition: 0.2s;" '
            'onmouseover="this.style.background=\'var(--primary-light)\'" onmouseout="this.style.background=\'none\'" '
            'title="Nghe câu tiếng Việt">🔊</button>' +
            m.group(5)
        )

    # Dùng cách đơn giản hơn: thay thế đúng phần sub-text của type 11
    old_fragment = '${q.word.ex_vn}</div><input type="text" class="typing-input" id="typing-ans"'
    
    if old_fragment not in content:
        print(f"  ⚠️  SKIP (already modified or different structure): {os.path.basename(fpath)}")
        skipped += 1
        continue
    
    new_fragment = (
        '${q.word.ex_vn}'
        '<button onclick="speakVN(\\\'${q.word.ex_vn}\\\')" '
        'style="background: none; border: 2px solid var(--primary-color); border-radius: 50%; width: 42px; height: 42px; font-size: 1.3rem; cursor: pointer; flex-shrink: 0; display: flex; align-items: center; justify-content: center; transition: 0.2s;" '
        'onmouseover="this.style.background=\'var(--primary-light)\'" onmouseout="this.style.background=\'none\'" '
        'title="Nghe câu tiếng Việt">🔊</button>'
        '</div><input type="text" class="typing-input" id="typing-ans"'
    )
    
    # Also update the sub-text div to add flex
    old_subtext_open = '<div class="sub-text" style="font-size: 1.4rem; color: var(--primary-dark);">'
    new_subtext_open = '<div class="sub-text" style="font-size: 1.4rem; color: var(--primary-dark); display: flex; align-items: center; justify-content: center; gap: 0.8rem;">'
    
    # Only replace the one in type 11 context - find and replace the fragment
    # We locate the type 11 block and replace within it
    type11_pattern = r'(\} else if \(q\.type === 11\) \{.*?)(class="sub-text" style="font-size: 1\.4rem; color: var\(--primary-dark\);")(.*?\$\{q\.word\.ex_vn\})(</div>)'
    
    def replace_type11(m):
        return (
            m.group(1) +
            'class="sub-text" style="font-size: 1.4rem; color: var(--primary-dark); display: flex; align-items: center; justify-content: center; gap: 0.8rem;"' +
            m.group(3) +
            '<button onclick=\\"speakVN(\'${q.word.ex_vn}\')\\" '
            'style=\\"background: none; border: 2px solid var(--primary-color); border-radius: 50%; width: 42px; height: 42px; font-size: 1.3rem; cursor: pointer; flex-shrink: 0; display: flex; align-items: center; justify-content: center; transition: 0.2s;\\" '
            'onmouseover=\\"this.style.background=\'var(--primary-light)\'\\" onmouseout=\\"this.style.background=\'none\'\\" '
            'title=\\"Nghe câu tiếng Việt\\">🔊</button>' +
            m.group(4)
        )
    
    new_content = content.replace(old_fragment, new_fragment, 1)
    # Also fix the sub-text div style (only within type 11 - replace first occurrence after type===11)
    
    # Add speakVN function if not present
    if "speakVN" not in new_content:
        new_content = new_content.replace(
            "function speak(t) {",
            "function speakVN(t) { const m = new SpeechSynthesisUtterance(); m.text = t; m.lang = 'vi-VN'; window.speechSynthesis.cancel(); window.speechSynthesis.speak(m); }\n        function speak(t) {"
        )
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"  ✅ Updated: {os.path.basename(fpath)}")
    updated += 1

print(f"\n{'='*50}")
print(f"Done! Updated: {updated}, Skipped: {skipped}")
