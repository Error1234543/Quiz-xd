def build_html_from_questions(questions, title="Quiz"):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
body {{ font-family: Arial; }}
.question {{ margin-bottom: 20px; padding: 10px; border: 1px solid #ccc; border-radius:5px; }}
.option {{ margin: 5px 0; cursor: pointer; padding:5px; border-radius:3px; }}
.option.correct {{ background-color: #c8e6c9; }}
.option.wrong {{ background-color: #ffcdd2; }}
.solution {{ display:none; color:#1565c0; }}
</style>
</head>
<body>
<h2>{title}</h2>
<form id="quizForm">
"""

    for idx, q in enumerate(questions):
        html += f"<div class='question'><p>Q{idx+1}: {q['q']}</p>"
        for opt_idx, opt in enumerate(q['options']):
            html += f"<div class='option'><input type='radio' name='q{idx}' value='{chr(65+opt_idx)}'> {opt}</div>"
        html += f"<p class='solution' id='sol{idx}'>Solution: {q['solution']} | Correct Answer: {q['answer']}</p>"
        html += "</div>"

    html += """
<input type="button" value="Submit" onclick="checkQuiz()">
</form>
<p id="result"></p>
<script>
function checkQuiz() {
    let correct = 0;
    let total = 0;
    let results = '';
    const questions = document.querySelectorAll('.question');
    questions.forEach((q, idx) => {
        const selected = q.querySelector('input[type=radio]:checked');
        const sol = q.querySelector('.solution');
        if(!selected) {
            results += 'Q'+(idx+1)+' not answered.<br>';
            sol.style.display='block';
            return;
        }
        total++;
        if(selected.value == questions[idx].querySelector('.solution').innerText.split('Correct Answer: ')[1].trim()) {
            correct++;
            selected.parentElement.classList.add('correct');
        } else {
            selected.parentElement.classList.add('wrong');
            sol.style.display='block';
        }
    });
    document.getElementById('result').innerHTML = 'Total Correct: '+correct+' / '+questions.length;
}
</script>
</body>
</html>
"""
    return html