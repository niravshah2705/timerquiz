# timerquiz
A simple application of timer quiz, it does read quiz from csv file &amp; provide detailed result

# Environment Setup Steps 

python3 -m venv .env
source ./.env/bin/activate.fish


# Dependency Setup Steps 
pip install -r requirements.txt

# Generate csv questions with AI 
Prompt: 
"prepare more 50 questions for Logical Reasoning, verbal reasoning, numerical reasoning & add Common questions about architecture history and provide output in csv format as Section name, question, options, correct answers, type single/multiple also correct answer as a , b , c or d pattern. if multiple use "a,b" as a answer, add quotes too"

Format csv file questions.txt as current file & start application 

# Run application locally
python app.py

# Access application from browser
http://127.0.0.1:5000/

# Future enhancement
- Add authentication
- Add admin panel
- Add questions from AI generated topic
