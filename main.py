from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uzver:supperpupperpassword@db/bewisedb'
db = SQLAlchemy(app)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), unique=True, nullable=False)
    answer_text = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/get_questions', methods=['POST'])
def get_questions():
    data = request.get_json()
    questions_num = data.get('questions_num', 1)
    saved_questions = []

    while len(saved_questions) < questions_num:
        response = requests.get(f'https://jservice.io/api/random?count=1')
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

    previous_questions = Question.query.all()
    return jsonify([q.serialize() for q in previous_questions])


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

