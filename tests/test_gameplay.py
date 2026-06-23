from game_functions.gameplay import play_game, play_round
from unittest.mock import patch
import pytest

@pytest.mark.unit
@patch('game_functions.gameplay.ask_question')
@patch('game_functions.gameplay.generate_question')
def test_play_round_calls_generate_question_5_times(mock_generate_question, mock_ask_question):
  '''
  Checks that a round asks 5 questions.
  '''
  mock_generate_question.return_value = ("What is 2 + 2?", 4)
  mock_ask_question.return_value = 10
  play_round(1, "Alex")
  assert mock_generate_question.call_count == 5

@pytest.mark.unit
@patch('game_functions.gameplay.ask_question')
@patch('game_functions.gameplay.generate_question')
def test_play_round_calls_ask_question_with_question_answer_and_name(mock_generate_question, mock_ask_question):
  '''
  Checks that each question is asked with the generated question, answer and player name.
  '''
  mock_generate_question.return_value = ("What is 2 + 2?", 4)
  mock_ask_question.return_value = 10
  play_round(1, "Alex")
  assert mock_ask_question.call_count == 5
  mock_ask_question.assert_called_with("What is 2 + 2?", 4, "Alex")

@pytest.mark.unit
@patch('game_functions.gameplay.ask_question')
@patch('game_functions.gameplay.generate_question')
def test_play_round_returns_sum_of_question_scores(mock_generate_question, mock_ask_question):
  '''
  Checks that the total score returned is the sum of the score from each of the 5 questions.
  '''
  mock_generate_question.return_value = ("What is 2 + 2?", 4)
  mock_ask_question.side_effect = [10, 5, 1, 0, 10]
  total_score, duration = play_round(1, "Alex")
  assert total_score == 26

@pytest.mark.unit
@patch('game_functions.gameplay.ask_question')
@patch('game_functions.gameplay.generate_question')
def test_play_round_prints_round_number_and_questions(mock_generate_question, mock_ask_question, capsys):
  '''
  Checks that the round number and each question number are printed.
  '''
  mock_generate_question.return_value = ("What is 2 + 2?", 4)
  mock_ask_question.return_value = 10
  play_round(3, "Alex")
  captured = capsys.readouterr()
  assert "Round 3." in captured.out
  assert "Question 1:" in captured.out
  assert "Question 5:" in captured.out

@pytest.mark.unit
@patch('game_functions.gameplay.ask_question')
@patch('game_functions.gameplay.generate_question')
def test_play_round_prints_total_score_summary(mock_generate_question, mock_ask_question, capsys):
  '''
  Checks that the round's summary message shows the correct total score.
  '''
  mock_generate_question.return_value = ("What is 2 + 2?", 4)
  mock_ask_question.side_effect = [10, 10, 10, 10, 10]
  play_round(2, "Alex")
  captured = capsys.readouterr()
  assert "Your total score for round 2 is 50!" in captured.out

@pytest.mark.unit
@patch('game_functions.gameplay.time.time')
@patch('game_functions.gameplay.ask_question')
@patch('game_functions.gameplay.generate_question')
def test_play_round_returns_duration_based_on_elapsed_time(mock_generate_question, mock_ask_question, mock_time):
  '''
  Checks that the duration returned is the difference between the start and end times.
  '''
  mock_generate_question.return_value = ("What is 2 + 2?", 4)
  mock_ask_question.return_value = 10
  mock_time.side_effect = [100.0, 107.5]
  total_score, duration = play_round(1, "Alex")
  assert duration == 7.5

@pytest.mark.unit
@patch('game_functions.gameplay.play_round')
@patch('builtins.input', side_effect=['Alex', '1'])
def test_play_game_greets_user_by_name(mock_input, mock_play_round):
  '''
  Checks that the user is greeted by the name they entered.
  '''
  mock_play_round.return_value = (10, 5.0)
  play_game()
  mock_input.assert_any_call("What is your name? ")

@pytest.mark.unit
@patch('game_functions.gameplay.play_round')
@patch('builtins.input', side_effect=['Alex', 'oops', '0', '2'])
def test_play_game_reprompts_until_a_valid_round_count_is_given(mock_input, mock_play_round, capsys):
  '''
  Checks that the user is reprompted for a number of rounds when they enter
  a non-number, or a number that isn't greater than 0.
  '''
  mock_play_round.return_value = (10, 5.0)
  play_game()
  captured = capsys.readouterr()
  assert "Please enter a number!" in captured.out
  assert "Don't be like that, Alex! Give me a number greater than 0!" in captured.out
  assert "Let's go Alex! Onto the first round of 2!" in captured.out

@pytest.mark.unit
@patch('game_functions.gameplay.play_round')
@patch('builtins.input', side_effect=['Alex', '1'])
def test_play_game_announces_single_round(mock_input, mock_play_round, capsys):
  '''
  Checks that when 1 round is chosen, the singular "let's play a round" message
  is shown rather than the multi-round message.
  '''
  mock_play_round.return_value = (10, 5.0)
  play_game()
  captured = capsys.readouterr()
  assert "Ok, Alex! Let's play a round!" in captured.out

@pytest.mark.unit
@patch('game_functions.gameplay.play_round')
@patch('builtins.input', side_effect=['Alex', '3'])
def test_play_game_calls_play_round_once_per_round_with_name(mock_input, mock_play_round):
  '''
  Checks that play_round is called once per round requested, with the round
  number and player name.
  '''
  mock_play_round.return_value = (10, 5.0)
  play_game()
  assert mock_play_round.call_count == 3
  mock_play_round.assert_any_call(1, 'Alex')
  mock_play_round.assert_any_call(2, 'Alex')
  mock_play_round.assert_any_call(3, 'Alex')

@pytest.mark.unit
@patch('game_functions.gameplay.play_round')
@patch('builtins.input', side_effect=['Alex', '1'])
def test_play_game_single_round_summary(mock_input, mock_play_round, capsys):
  '''
  Checks the final summary message for a single round shows the total score
  and the time taken.
  '''
  mock_play_round.return_value = (15, 30.0)
  play_game()
  captured = capsys.readouterr()
  assert "Good job Alex! Your total score is 15." in captured.out
  assert "it took you 0 minutes and 30 seconds to complete this game!" in captured.out

@pytest.mark.unit
@patch('game_functions.gameplay.play_round')
@patch('builtins.input', side_effect=['Alex', '2'])
def test_play_game_multiple_rounds_summary_uses_average_score(mock_input, mock_play_round, capsys):
  '''
  Checks the final summary message for multiple rounds shows the average score
  across rounds and the total time taken.
  '''
  mock_play_round.side_effect = [(10, 20.0), (20, 40.0)]
  play_game()
  captured = capsys.readouterr()
  assert "Your average score across 2 rounds was 15.00." in captured.out
  assert "it took you 1 minutes and 0 seconds to play 2 rounds!" in captured.out
