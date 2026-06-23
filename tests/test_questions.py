from game_functions.questions import generate_question
from unittest.mock import patch
import re
import pytest

QUESTION_PATTERN = re.compile(r"^What is (\d+) ([+\-*/]) (\d+)\?$")

@pytest.mark.unit
def test_generate_q_returns_question_and_answer():
  '''
  Checks that generate_question function returns two values, a question and an answer.
  '''
  result = generate_question()
  assert len(result) == 2

@pytest.mark.unit
def test_generate_q_returns_a_question_string():
  '''
  Checks question returned is a string
  '''
  question, answer = generate_question()
  assert isinstance(question, str)

@pytest.mark.unit
def test_generate_q_returns_answer_as_int():
  '''
  Checks answer returned is an integer
  '''
  question, answer = generate_question()
  assert isinstance(answer, int)

@pytest.mark.unit
def test_question_uses_numbers_100_or_less():
  '''
  Checks that addition and subtraction questions use numbers 100 or less.
  '''
  for _ in range(200):
    question, answer = generate_question()
    match = QUESTION_PATTERN.match(question)
    num1, op, num2 = int(match.group(1)), match.group(2), int(match.group(3))
    if op in ['+', '-']:
      assert num1 <= 100
      assert num2 <= 100

@pytest.mark.unit
def test_question_has_an_operator():
  '''
  Checks that only '*, /, +, -' operators are used in the question
  '''
  for _ in range(200):
    question, answer = generate_question()
    match = QUESTION_PATTERN.match(question)
    assert match is not None
    assert match.group(2) in ['+', '-', '*', '/']

@pytest.mark.unit
def test_multiplication_numbers_within_12():
  '''
  Checks that multiplication questions only use numbers between 1 and 12.
  '''
  for _ in range(200):
    question, answer = generate_question()
    match = QUESTION_PATTERN.match(question)
    num1, op, num2 = int(match.group(1)), match.group(2), int(match.group(3))
    if op == '*':
      assert 1 <= num1 <= 12
      assert 1 <= num2 <= 12

@pytest.mark.unit
def test_division_numbers_within_12():
  '''
  Checks that division questions use a divisor and quotient between 1 and 12, and
  that the dividend is always a non-zero multiple of the divisor.
  '''
  for _ in range(200):
    question, answer = generate_question()
    match = QUESTION_PATTERN.match(question)
    num1, op, num2 = int(match.group(1)), match.group(2), int(match.group(3))
    if op == '/':
      assert 1 <= num2 <= 12
      assert 1 <= answer <= 12
      assert num1 >= 1
      assert num1 == num2 * answer

@pytest.mark.unit
@patch('game_functions.questions.random.randint')
@patch('game_functions.questions.random.choice')
def test_addition_returns_correct_answer(mock_choice, mock_randint):
  '''
  Checks that an addition question returns the correct answer.
  '''
  mock_choice.return_value = '+'
  mock_randint.side_effect = [5, 7]
  question, answer = generate_question()
  assert question == "What is 5 + 7?"
  assert answer == 12

@pytest.mark.unit
@patch('game_functions.questions.random.randint')
@patch('game_functions.questions.random.choice')
def test_subtraction_returns_correct_answer(mock_choice, mock_randint):
  '''
  Checks that a subtraction question returns the correct answer.
  '''
  mock_choice.return_value = '-'
  mock_randint.side_effect = [10, 4]
  question, answer = generate_question()
  assert question == "What is 10 - 4?"
  assert answer == 6

@pytest.mark.unit
@patch('game_functions.questions.random.randint')
@patch('game_functions.questions.random.choice')
def test_multiplication_returns_correct_answer(mock_choice, mock_randint):
  '''
  Checks that a multiplication question returns the correct answer.
  '''
  mock_choice.return_value = '*'
  mock_randint.side_effect = [6, 7]
  question, answer = generate_question()
  assert question == "What is 6 * 7?"
  assert answer == 42

@pytest.mark.unit
@patch('game_functions.questions.random.randint')
@patch('game_functions.questions.random.choice')
def test_division_returns_correct_answer(mock_choice, mock_randint):
  '''
  Checks that a division question builds the dividend from the divisor and quotient,
  so that the division is exact.
  '''
  mock_choice.return_value = '/'
  mock_randint.side_effect = [3, 4]
  question, answer = generate_question()
  assert question == "What is 12 / 3?"
  assert answer == 4

@pytest.mark.unit
def test_division_answer_always_exact():
  '''
  Checks that division questions always produce an exact (non-remainder) answer.
  '''
  for _ in range(200):
    question, answer = generate_question()
    match = QUESTION_PATTERN.match(question)
    num1, op, num2 = int(match.group(1)), match.group(2), int(match.group(3))
    if op == '/':
      assert num1 % num2 == 0
      assert num1 // num2 == answer

@pytest.mark.unit
def test_division_dividend_is_never_zero():
  '''
  Checks that division questions never use 0 as the dividend.
  '''
  for _ in range(200):
    question, answer = generate_question()
    match = QUESTION_PATTERN.match(question)
    num1, op, num2 = int(match.group(1)), match.group(2), int(match.group(3))
    if op == '/':
      assert num1 != 0