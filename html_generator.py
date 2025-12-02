def build_html_from_questions(questions, title="Quiz"):
    """
    Generates a full professional HTML quiz page from questions JSON
    questions = [
        {"q": "Question text", "options": ["A","B","C","D"], "answer":"A", "solution":"Solution text"},
        ...
    ]
    """
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
body {{
    font-family: 'Arial', sans-serif;
    background-color: #f2f2f2;
    padding: 20px;
}}
h2 {{
    text-align:center;
    color:#0d47a1;
}}
.question {{
    margin-bottom: 25px;
    padding: 15px;
    border-radius: 10px;
    background-color: #ffffff;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}}
.option {{
    margin: 8px 0;
    padding: 8px 12px;
    cursor: pointer;
    border-radius: 5px;
    border: 1px solid #ccc;
    transition: all 0.2s ease;
}}
.option:hover {{
    background-color: #e3f2fd;
}}
.option.correct {{
    background-color: #c8e6c9 !important;
}}
.option.wrong {{
    background-color: #ffcdd2 !important;
}}
.solution {{
    display:none;
    margin-top: 10px;
    color:#1565c0;
    font-weight: bold;
}}
#submitBtn {{
    display:block;
    margin: 20px auto;
    padding: 12px 25px;
    font-size: 16px;
    cursor:pointer;
    border:none;
    border-radius:8px;
    background-color:#0d47a1;
    color:#fff;
    transition: 0.3s;
}}
#submitBtn:hover {{
    background-color:#1565c0;
}}
#result {{
    text-align:center;
    font-size:18px;
    font-weight:bold;
    margin-top:20px;
}}
</style>
</head>
<body>
<h2>{title}</h2>
<form id="quizForm">
"""

    # Add questions
    for idx, q in enumerate(questions):
        html += f"<div class='question'><p><strong>Q{idx+1}:</strong> {q['q']}</p>"
        for opt_idx, opt in enumerate(q['options']):
            html += f"<div class='option'><input type='radio' name='q{idx}' value='{chr(65+opt_idx)}'> {opt}</div>"
        html += f"<p class='solution' id='sol{idx}'>Solution: {q['solution']} | Correct Answer: {q['answer']}</p>"
        html += "</div>"

    # Submit button
    html += "<input type='button' id='submitBtn' value='Submit' onclick='checkQuiz()'>"
    html += "</form>"
    html += "<p id='result'></p>"

    # JavaScript
    html += """
<script>
function checkQuiz() {
    let correct = 0;
    const questions = document.querySelectorAll('.question');
    questions.forEach((q, idx) => {
        const selected = q.querySelector('input[type=radio]:checked');
        const sol = q.querySelector('.solution');
        sol.style.display='none';
        q.querySelectorAll('.option').forEach(o => {
            o.classList.remove('correct','wrong');
        });

        if(!selected) {
            sol.style.display='block';
            return;
        }
        if(selected.value == sol.innerText.split('Correct Answer: ')[1].trim()) {
            correct++;
            selected.parentElement.classList.add('correct');
        } else {
            selected.parentElement.classList.add('wrong');
            sol.style.display='block';
        }
    });
    document.getElementById('result').innerHTML = 'Total Correct: ' + correct + ' / ' + questions.length;
}
</script>
</body>
</html>
"""
    return html