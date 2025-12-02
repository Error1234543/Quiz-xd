# html_generator.py
def build_html_from_questions(questions, title="Quiz"):
    html = f"""<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
    <style>
    body{{font-family:Arial,sans-serif;padding:20px}}
    .question-box{{margin-bottom:20px;padding:15px;border-radius:8px;border:1px solid #ddd}}
    .correct{{color:green;font-weight:bold}}
    .wrong{{color:red}}
    .solution{{background:#f9f9f9;padding:10px;border-radius:6px;margin-top:8px}}
    .result-box{{margin-top:30px;padding:18px;border-radius:8px;border:2px solid #222;background:#f0fff0}}
    </style>
    </head><body>
    <h1>{title}</h1>
    <div id="content">"""
    correct_count = 0
    for i,q in enumerate(questions, start=1):
        ans = q.get("answer","")
        html += f'<div class="question-box"><h3>Q{i}. {q.get("q","")}</h3>'
        opts = q.get("options",[])
        letters = ["A","B","C","D"]
        for idx,opt in enumerate(opts):
            letter = letters[idx] if idx < len(letters) else f"opt{idx}"
            if letter == ans:
                html += f'<p class="correct">{letter}. {opt} ✔</p>'
                correct_count += 1
            else:
                html += f'<p>{letter}. {opt}</p>'
        html += f'<div class="solution"><b>Solution:</b><div>{q.get("solution","")}</div></div></div>'
    total = len(questions)
    score = int((correct_count/total)*100) if total>0 else 0
    html += f'</div><div class="result-box"><h2>Result</h2><p>Correct: {correct_count}</p><p>Wrong: {total-correct_count}</p><p>Score: {score}%</p></div></body></html>'
    return html