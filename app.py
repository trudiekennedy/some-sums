'''
Flask web front-end for someSums. Runs a single-player, session-based version of
the quiz: the existing CLI logic in game_functions can't be reused as-is since it
blocks on input() for multiple attempts in one call, so this layer reimplements the
per-attempt and per-round orchestration over flask.session instead.
'''
import os
import random

from dotenv import load_dotenv
from flask import Flask, render_template, request, session, jsonify, redirect, url_for

from game_functions.questions import generate_question, score_for_attempt
from data_files.vibes import vibes

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

QUESTIONS_PER_ROUND = 5


def _start_new_question():
    question, answer = generate_question()
    session['current_question_text'] = question
    session['current_answer'] = answer
    session['attempts_so_far'] = 0


@app.route('/')
def index():
    session.clear()
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    name = request.form.get('name', '').strip()
    rounds_raw = request.form.get('rounds', '')

    error = None
    rounds = None
    if not name:
        error = "Please tell me your name!"
    else:
        try:
            rounds = int(rounds_raw)
        except ValueError:
            error = "Please enter a number for the rounds!"
        else:
            if rounds <= 0:
                error = "Give me a number of rounds greater than 0!"

    if error:
        return render_template('index.html', error=error, name=name, rounds=rounds_raw)

    session['player_name'] = name
    session['rounds_requested'] = rounds
    session['current_round'] = 1
    session['current_question_num'] = 1
    session['round_score'] = 0
    session['round_scores'] = []
    _start_new_question()

    return redirect(url_for('quiz'))


@app.route('/quiz')
def quiz():
    if 'current_question_text' not in session:
        return redirect(url_for('index'))

    return render_template(
        'quiz.html',
        name=session['player_name'],
        current_round=session['current_round'],
        rounds_requested=session['rounds_requested'],
        current_question_num=session['current_question_num'],
        questions_per_round=QUESTIONS_PER_ROUND,
        question_text=session['current_question_text'],
        round_score=session['round_score'],
    )


@app.route('/api/answer', methods=['POST'])
def api_answer():
    if 'current_question_text' not in session:
        return jsonify({"error": "No active question."}), 400

    body = request.get_json(silent=True) or {}
    raw_answer = body.get('answer')

    try:
        user_answer = int(raw_answer)
    except (TypeError, ValueError):
        return jsonify({
            "resolved": False,
            "valid": False,
            "message": "Invalid input! Please enter a number.",
        })

    name = session['player_name']
    correct_answer = session['current_answer']
    attempts_so_far = session['attempts_so_far']
    correct = user_answer == correct_answer

    response = {
        "valid": True,
        "correct": correct,
        "resolved": False,
        "score_awarded": 0,
        "attempts_so_far": attempts_so_far,
        "message": "",
        "correct_answer": None,
        "round_score": session['round_score'],
        "round_complete": False,
        "game_complete": False,
        "next_question": None,
    }

    if correct:
        score_awarded = score_for_attempt(attempts_so_far)
        if attempts_so_far == 0:
            message = f"{random.choice(vibes.get('positive_vibes'))}{name}! 10 points to you!"
        elif attempts_so_far == 1:
            message = "Good job! 5 points!"
        else:
            message = f"You got it, {name}! Have a point!"
        response.update({
            "resolved": True,
            "score_awarded": score_awarded,
            "message": message,
        })
    elif attempts_so_far < 2:
        session['attempts_so_far'] = attempts_so_far + 1
        response.update({
            "attempts_so_far": session['attempts_so_far'],
            "message": f"{random.choice(vibes.get('encouraging_vibes'))}{name}!",
        })
        return jsonify(response)
    else:
        response.update({
            "resolved": True,
            "score_awarded": 0,
            "message": f"The correct answer was {correct_answer}.",
            "correct_answer": correct_answer,
        })

    # Question is resolved (correct, or 3rd wrong attempt) - advance state.
    session['round_score'] += response['score_awarded']
    response['round_score'] = session['round_score']

    if session['current_question_num'] < QUESTIONS_PER_ROUND:
        session['current_question_num'] += 1
        _start_new_question()
        response['next_question'] = session['current_question_text']
        return jsonify(response)

    # Round just finished.
    session['round_scores'] = session['round_scores'] + [session['round_score']]
    session['round_score'] = 0
    response['round_score'] = 0
    response['round_complete'] = True

    if session['current_round'] < session['rounds_requested']:
        session['current_round'] += 1
        session['current_question_num'] = 1
        _start_new_question()
        response['next_question'] = session['current_question_text']
    else:
        response['game_complete'] = True

    return jsonify(response)


@app.route('/summary')
def summary():
    if 'round_scores' not in session or 'rounds_requested' not in session:
        return redirect(url_for('index'))

    round_scores = session['round_scores']
    rounds_requested = session['rounds_requested']
    total_score = sum(round_scores)
    avg_score = total_score / rounds_requested if rounds_requested else 0

    return render_template(
        'summary.html',
        name=session.get('player_name'),
        rounds_requested=rounds_requested,
        total_score=total_score,
        avg_score=avg_score,
    )


if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug, use_reloader=False)
