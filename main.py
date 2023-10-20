from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uzver:supperpupperpassword@db/bewisedb'
db = SQLAlchemy(app)

@app.route('/', '/get_questions', methods=['GET'])
def home():
    return render_template('index.html')

class Question(db.Model):
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer)
    question_text = db.Column(db.String(200), unique=True, nullable=False)
    answer_text = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    def serialize(self):
        return {
            'index': self.index,
            'id': self.id,
            'question_text': self.question_text,
            'answer_text': self.answer_text,
            'creation_date': self.creation_date.isoformat()
        }

with app.app_context():
    db.create_all()

@app.route('/get_questions', methods=['POST'])
def get_questions():

    data = request.get_json()
    questions_num = int(data.get('questions_num', 1))
    saved_questions = []

    while len(saved_questions) < questions_num:
        response = requests.get(f'https://jservice.io/api/random?count={questions_num}')
        question_data = response.json()[0]

        if not Question.query.filter_by(id=question_data['id']).first():
            new_question = Question(
                id=question_data['id'],
                question_text=question_data['question'],
                answer_text=question_data['answer'],
                creation_date=question_data['airdate']
            )
            db.session.add(new_question)
            db.session.commit()
            saved_questions.append(new_question)
    last_question_index = Question.query.order_by(Question.index.desc()).first().index
    previous_question = Question.query.get(last_question_index - 1)
    return jsonify(previous_question.serialize() if previous_question else {})


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)

