from flask import Flask, render_template, request

app = Flask(__name__)

# Grading Logic Ported from gptcalculator.py
def get_grade_point(marks):
    if marks >= 90: return 10
    elif marks >= 80: return 9
    elif marks >= 70: return 8
    elif marks >= 60: return 7
    elif marks >= 55: return 6
    elif marks >= 50: return 5.5
    elif marks > 40: return 5
    elif marks == 40: return 4
    else: return 0

def get_practical_gp(marks):
    if marks >= 45: return 10
    elif marks >= 39: return 9
    elif marks >= 35: return 8
    elif marks >= 30: return 7
    elif marks >= 25: return 6
    elif marks >= 22: return 5
    else: return 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/sgpa', methods=['GET', 'POST'])
def sgpa():
    if request.method == 'POST':
        try:
            n_theory = int(request.form.get('n_theory', 0))
            n_practical = int(request.form.get('n_practical', 0))
            total_weighted_gp = 0
            total_credits = 0
            
            for i in range(1, n_theory + 1):
                marks = float(request.form.get(f'th_marks_{i}', 0))
                credit = float(request.form.get(f'th_credit_{i}', 0))
                total_weighted_gp += get_grade_point(marks) * credit
                total_credits += credit
            
            for i in range(1, n_practical + 1):
                marks = float(request.form.get(f'pr_marks_{i}', 0))
                credit = float(request.form.get(f'pr_credit_{i}', 0))
                total_weighted_gp += get_practical_gp(marks) * credit
                total_credits += credit
            
            if total_credits > 0:
                result_val = round(total_weighted_gp / total_credits, 2)
                return render_template('result.html', type='SGPA', result=result_val)
            return render_template('sgpa.html', error='Total credits must be greater than 0.')
        except ValueError:
            return render_template('sgpa.html', error='Invalid input values.')
    return render_template('sgpa.html')

@app.route('/cgpa', methods=['GET', 'POST'])
def cgpa():
    if request.method == 'POST':
        try:
            n_sem = int(request.form.get('n_sem', 0))
            total_sgpa_weighted = 0
            total_sem_credits = 0
            
            for i in range(1, n_sem + 1):
                sgpa_val = float(request.form.get(f'sem_sgpa_{i}', 0))
                credits = float(request.form.get(f'sem_credit_{i}', 0))
                total_sgpa_weighted += sgpa_val * credits
                total_sem_credits += credits
            
            if total_sem_credits > 0:
                result_val = round(total_sgpa_weighted / total_sem_credits, 2)
                return render_template('result.html', type='CGPA', result=result_val)
            return render_template('cgpa.html', error='Total credits must be greater than 0.')
        except ValueError:
            return render_template('cgpa.html', error='Invalid input values.')
    return render_template('cgpa.html')

if __name__ == '__main__':
    app.run()
