import os

os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-unit-tests')

from app import app as flask_app
from unittest.mock import patch
import pytest


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    return flask_app.test_client()


def start_game(client, name="Alex", rounds=2):
    return client.post('/start', data={'name': name, 'rounds': str(rounds)})


@pytest.mark.unit
def test_index_renders_start_form(client):
    '''
    Checks that the home page renders the name/rounds form.
    '''
    response = client.get('/')
    assert response.status_code == 200
    assert b'name="name"' in response.data
    assert b'name="rounds"' in response.data


@pytest.mark.unit
def test_index_clears_existing_session(client):
    '''
    Checks that visiting the home page always starts a clean session.
    '''
    with client.session_transaction() as sess:
        sess['player_name'] = 'Stale'
        sess['round_scores'] = [10]
    client.get('/')
    with client.session_transaction() as sess:
        assert 'player_name' not in sess
        assert 'round_scores' not in sess


@pytest.mark.unit
@patch('app.generate_question')
def test_start_with_valid_input_redirects_to_quiz(mock_generate_question, client):
    '''
    Checks that a valid start form submission redirects to /quiz.
    '''
    mock_generate_question.return_value = ("What is 2 + 2?", 4)
    response = start_game(client)
    assert response.status_code == 302
    assert response.headers['Location'] == '/quiz'


@pytest.mark.unit
@patch('app.generate_question')
def test_start_with_valid_input_seeds_session(mock_generate_question, client):
    '''
    Checks that a valid start form submission seeds the session correctly.
    '''
    mock_generate_question.return_value = ("What is 2 + 2?", 4)
    start_game(client, name="Alex", rounds=2)
    with client.session_transaction() as sess:
        assert sess['player_name'] == 'Alex'
        assert sess['rounds_requested'] == 2
        assert sess['current_round'] == 1
        assert sess['current_question_num'] == 1
        assert sess['round_score'] == 0
        assert sess['round_scores'] == []
        assert sess['current_question_text'] == "What is 2 + 2?"
        assert sess['current_answer'] == 4
        assert sess['attempts_so_far'] == 0


@pytest.mark.unit
def test_start_with_empty_name_reprompts(client):
    '''
    Checks that an empty name re-renders the form with an error and doesn't seed the session.
    '''
    response = start_game(client, name="", rounds=2)
    assert response.status_code == 200
    assert b'Please tell me your name!' in response.data
    with client.session_transaction() as sess:
        assert 'player_name' not in sess


@pytest.mark.unit
def test_start_with_non_numeric_rounds_reprompts(client):
    '''
    Checks that a non-numeric rounds value re-renders the form with an error.
    '''
    response = start_game(client, name="Alex", rounds="oops")
    assert response.status_code == 200
    assert b'Please enter a number for the rounds!' in response.data


@pytest.mark.unit
def test_start_with_zero_rounds_reprompts(client):
    '''
    Checks that a 0 (or negative) rounds value re-renders the form with an error.
    '''
    response = start_game(client, name="Alex", rounds=0)
    assert response.status_code == 200
    assert b'Give me a number of rounds greater than 0!' in response.data


@pytest.mark.unit
def test_quiz_redirects_to_index_without_active_session(client):
    '''
    Checks that /quiz redirects home if there is no active game.
    '''
    response = client.get('/quiz')
    assert response.status_code == 302
    assert response.headers['Location'] == '/'


@pytest.mark.unit
@patch('app.generate_question')
def test_quiz_renders_first_question_from_session(mock_generate_question, client):
    '''
    Checks that /quiz renders the question stored in the session.
    '''
    mock_generate_question.return_value = ("What is 2 + 2?", 4)
    start_game(client)
    response = client.get('/quiz')
    assert response.status_code == 200
    assert b'What is 2 + 2?' in response.data
    assert b'>4<' not in response.data


@pytest.mark.unit
@patch('app.generate_question')
def test_answer_correct_first_attempt_scores_10(mock_generate_question, client):
    '''
    Checks that a correct first-attempt answer scores 10 points.
    '''
    mock_generate_question.return_value = ("What is 2 + 2?", 4)
    start_game(client, rounds=1)
    response = client.post('/api/answer', json={'answer': 4})
    data = response.get_json()
    assert data['correct'] is True
    assert data['resolved'] is True
    assert data['score_awarded'] == 10


@pytest.mark.unit
@patch('app.generate_question')
def test_answer_wrong_then_correct_scores_5(mock_generate_question, client):
    '''
    Checks that a correct second-attempt answer scores 5 points and the first
    wrong attempt doesn't resolve the question.
    '''
    mock_generate_question.return_value = ("What is 2 + 2?", 4)
    start_game(client, rounds=1)

    first = client.post('/api/answer', json={'answer': 1}).get_json()
    assert first['resolved'] is False
    assert first['attempts_so_far'] == 1

    second = client.post('/api/answer', json={'answer': 4}).get_json()
    assert second['resolved'] is True
    assert second['score_awarded'] == 5


@pytest.mark.unit
@patch('app.generate_question')
def test_answer_three_wrong_attempts_reveals_answer_and_scores_0(mock_generate_question, client):
    '''
    Checks that 3 wrong attempts reveals the correct answer and scores 0.
    '''
    mock_generate_question.return_value = ("What is 2 + 2?", 4)
    start_game(client, rounds=1)

    client.post('/api/answer', json={'answer': 1})
    client.post('/api/answer', json={'answer': 2})
    third = client.post('/api/answer', json={'answer': 3}).get_json()

    assert third['resolved'] is True
    assert third['score_awarded'] == 0
    assert third['correct_answer'] == 4
    assert "The correct answer was 4." in third['message']


@pytest.mark.unit
@patch('app.generate_question')
def test_answer_invalid_input_does_not_consume_attempt(mock_generate_question, client):
    '''
    Checks that non-integer input doesn't count as a used attempt.
    '''
    mock_generate_question.return_value = ("What is 2 + 2?", 4)
    start_game(client, rounds=1)

    response = client.post('/api/answer', json={'answer': 'abc'})
    data = response.get_json()
    assert data['valid'] is False

    with client.session_transaction() as sess:
        assert sess['attempts_so_far'] == 0


@pytest.mark.unit
@patch('app.generate_question')
def test_answer_advances_question_within_round(mock_generate_question, client):
    '''
    Checks that resolving a question advances to the next question in the same round.
    '''
    mock_generate_question.side_effect = [
        ("What is 2 + 2?", 4),
        ("What is 3 + 3?", 6),
    ]
    start_game(client, rounds=1)

    response = client.post('/api/answer', json={'answer': 4}).get_json()
    assert response['round_complete'] is False
    assert response['next_question'] == "What is 3 + 3?"

    with client.session_transaction() as sess:
        assert sess['current_question_num'] == 2
        assert sess['current_question_text'] == "What is 3 + 3?"


@pytest.mark.unit
@patch('app.generate_question')
def test_answer_completes_round_and_starts_next(mock_generate_question, client):
    '''
    Checks that completing 5 questions finishes the round and starts the next one.
    '''
    mock_generate_question.side_effect = [
        ("What is 1?", 1), ("What is 2?", 2), ("What is 3?", 3),
        ("What is 4?", 4), ("What is 5?", 5), ("What is 6?", 6),
    ]
    start_game(client, rounds=2)

    for answer in [1, 2, 3, 4]:
        client.post('/api/answer', json={'answer': answer})
    fifth = client.post('/api/answer', json={'answer': 5}).get_json()

    assert fifth['round_complete'] is True
    assert fifth['game_complete'] is False
    assert fifth['next_question'] == "What is 6?"

    with client.session_transaction() as sess:
        assert sess['current_round'] == 2
        assert sess['current_question_num'] == 1
        assert sess['round_scores'] == [50]
        assert sess['round_score'] == 0


@pytest.mark.unit
@patch('app.generate_question')
def test_answer_completes_final_round_sets_game_complete(mock_generate_question, client):
    '''
    Checks that completing the last round sets game_complete with no next question.
    '''
    mock_generate_question.side_effect = [
        ("What is 1?", 1), ("What is 2?", 2), ("What is 3?", 3),
        ("What is 4?", 4), ("What is 5?", 5),
    ]
    start_game(client, rounds=1)

    for answer in [1, 2, 3, 4]:
        client.post('/api/answer', json={'answer': answer})
    fifth = client.post('/api/answer', json={'answer': 5}).get_json()

    assert fifth['round_complete'] is True
    assert fifth['game_complete'] is True
    assert fifth['next_question'] is None


@pytest.mark.unit
def test_summary_without_completed_game_redirects_to_index(client):
    '''
    Checks that /summary redirects home if there's no completed game data.
    '''
    response = client.get('/summary')
    assert response.status_code == 302
    assert response.headers['Location'] == '/'


@pytest.mark.unit
def test_summary_shows_total_for_single_round(client):
    '''
    Checks that /summary shows the total score for a single round.
    '''
    with client.session_transaction() as sess:
        sess['player_name'] = 'Alex'
        sess['round_scores'] = [23]
        sess['rounds_requested'] = 1
    response = client.get('/summary')
    assert response.status_code == 200
    assert b'23' in response.data
    assert b'Alex' in response.data


@pytest.mark.unit
def test_summary_shows_average_for_multiple_rounds(client):
    '''
    Checks that /summary shows the average score across multiple rounds.
    '''
    with client.session_transaction() as sess:
        sess['player_name'] = 'Alex'
        sess['round_scores'] = [10, 20]
        sess['rounds_requested'] = 2
    response = client.get('/summary')
    assert response.status_code == 200
    assert b'15.00' in response.data
