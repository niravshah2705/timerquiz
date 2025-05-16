from flask import Flask, render_template, request, redirect, url_for
import csv
import time

from datetime import timedelta

app = Flask(__name__)

# Configuration for the timer (in seconds)
QUESTION_TIMEOUT = 90  # Example: 60 seconds per question

def load_questions(csv_file):
    # ... (same load_questions function as before) ...
    sections = {}
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            section = row['section'].strip()
            if section not in sections:
                sections[section] = []
            options = [row[f'option_{i+1}'].strip() for i in range(4) if row.get(f'option_{i+1}') and row[f'option_{i+1}'].strip()]
            sections[section].append({
                'question': row['question'].strip(),
                'options': options,
                'correct_answer': row['correct_answer'].strip(),
                'type': row['type'].strip().lower(),
                'section': section  # Add section to each question
            })
    return sections

def evaluate_answer(user_answer, correct_answer, question_type):
    # ... (same evaluate_answer function as before) ...
    correct_options = sorted([ans.strip().lower() for ans in correct_answer.split(',')])
    return user_answer == correct_options

# Global variable to store questions (for simplicity in this example)
questions_data = load_questions('questions.csv')
all_questions_list = [q for section_questions in questions_data.values() for q in section_questions]
num_questions = len(all_questions_list)
current_question_index = 0
user_answers = {}
start_times = {}
end_times = {}

@app.route('/')
def index():
    return render_template('index.html', num_questions=num_questions)

@app.route('/question/<int:question_id>')
def question(question_id):
    if 0 <= question_id < num_questions:
        question_data = all_questions_list[question_id]
        print("Question Data:", question_data)
        start_times[question_id] = time.time()
        return render_template('question.html', question_data=question_data, question_id=question_id,chr=chr,enumerate=enumerate,ord=ord, timeout=QUESTION_TIMEOUT)
    else:
        return "Invalid question ID"

@app.route('/submit_answer/<int:question_id>', methods=['POST'])
def submit_answer(question_id):
    end_times[question_id] = time.time()
    time_taken = end_times[question_id] - start_times[question_id]

    question_data = all_questions_list[question_id]
    user_answer = request.form.getlist('answer') # Use getlist for multiple choices

    user_answers[question_id] = {
        'user_answer': sorted([ans.lower() for ans in user_answer]),
        'correct_answer': sorted([ans.strip().lower() for ans in question_data['correct_answer'].split(',')]),
        'time_taken': time_taken
    }

    if question_id < num_questions - 1:
        return redirect(url_for('question', question_id=question_id + 1))
    else:
        return redirect(url_for('results'))

@app.route('/results')
def results():
    score = 0
    detailed_results = []
    total_time = 0

    for q_id, answer_data in user_answers.items():
        question_data = all_questions_list[q_id]
        is_correct = answer_data['user_answer'] == answer_data['correct_answer']
        if is_correct:
            score += 1
        total_time += answer_data['time_taken']
        detailed_results.append({
            'question': question_data['question'],
            'user_answer': ", ".join(answer_data['user_answer']),
            'correct_answer': ", ".join(answer_data['correct_answer']),
            'time_taken': timedelta(seconds=round(answer_data['time_taken'])),
            'is_correct': is_correct
        })

    return render_template('results.html', score=score, total_time=timedelta(seconds=round(total_time)), detailed_results=detailed_results, num_questions=num_questions)

if __name__ == '__main__':
    app.run(debug=True)