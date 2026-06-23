from game_functions.questions import ask_question
from data_files.vibes import vibes
from unittest.mock import patch
import pytest

@pytest.mark.unit
@patch('builtins.input', return_value='5')
def test_ask_question_presents_question(mock_input):
  '''
  Checks that question is asked.
  '''
  ask_question("What is 2 + 3?", 5, "Alex")
  mock_input.assert_called_once_with("What is 2 + 3? ")

@pytest.mark.unit
@patch('builtins.input', return_value='5')
def test_ask_question_scores_10_answered_first_time(mock_input):
  '''
  Checks that score is 10 when user answers correctly first time.
  '''
  score = ask_question("What is 2 + 3?", 5, "Alex")
  assert score == 10

@pytest.mark.unit
@patch('builtins.input', side_effect=['1', '5'])
def test_ask_question_scores_5_on_second_attempt(mock_input):
  '''
  Checks that score is 5 when user answers correctly on second attempt.
  '''
  score = ask_question("What is 2 + 3?", 5, "Alex")
  assert score == 5

@pytest.mark.unit
@patch('builtins.input', side_effect=['1', '2', '5'])
def test_ask_question_scores_1_on_third_attempt(mock_input):
  '''
  Checks score is 1 when user answers on third attempt.
  '''
  score = ask_question("What is 2 + 3?", 5, "Alex")
  assert score == 1

@pytest.mark.unit
@patch('builtins.input', side_effect=['1', '2', '3'])
def test_ask_question_shares_correct_answer_if_not_answered_in_3(mock_input, capsys):
  '''
  Checks answer is provided if not answered in 3.
  '''
  score = ask_question("What is 2 + 3?", 5, "Alex")
  captured = capsys.readouterr()
  assert "The correct answer was 5." in captured.out
  assert score == 0

@pytest.mark.unit
@patch('game_functions.questions.random.choice')
@patch('builtins.input', return_value='5')
def test_ask_question_gives_positive_vibes_when_answered_first_time(mock_input, mock_choice, capsys):
  '''
  Checks that a random positive vibe is presented to the user when
  they answer correctly on first attempt.
  '''
  mock_choice.return_value = "Nice one, "
  ask_question("What is 2 + 3?", 5, "Alex")
  captured = capsys.readouterr()
  mock_choice.assert_any_call(vibes.get('positive_vibes'))
  assert "Nice one, Alex! 10 points to you!" in captured.out

@pytest.mark.unit
@patch('game_functions.questions.random.choice')
@patch('builtins.input', side_effect=['1', '5'])
def test_ask_question_gives_encouraging_vibes_if_not_answered(mock_input, mock_choice, capsys):
  '''
  Checks that a random encouraging vibe is presented to the user when
  they don't answer correctly.
  '''
  mock_choice.return_value = "Keep trying, "
  ask_question("What is 2 + 3?", 5, "Alex")
  captured = capsys.readouterr()
  mock_choice.assert_any_call(vibes.get('encouraging_vibes'))
  assert "Keep trying, Alex!" in captured.out

@pytest.mark.unit
@patch('builtins.input', return_value='5')
def test_ask_question_returns_score(mock_input):
  '''
  Checks that the score is returned after the question is answered.
  '''
  score = ask_question("What is 2 + 3?", 5, "Alex")
  assert isinstance(score, int)

@pytest.mark.unit
@patch('builtins.input', side_effect=['abc', '5'])
def test_ask_question_handles_non_integer_input(mock_input, capsys):
  '''
  Checks that a non-integer input is rejected with a message and does not
  count towards the 3 attempts.
  '''
  score = ask_question("What is 2 + 3?", 5, "Alex")
  captured = capsys.readouterr()
  assert "Invalid input! Please enter a number." in captured.out
  assert score == 10
