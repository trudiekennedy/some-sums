'''
Functions associated with creating and asking questions.
Utilises random package to generate Math questions. 
'''
import random
from data_files.vibes import vibes

def generate_question():
    """This function randomly generates the arithmetic questions: for addition and subtraction, numbers used will be
    between 1 & 100; for division and multiplication, numbers will be between 1 & 12 to support what a 9-year-old
    will have covered in Maths.
    Returns: question and answer of a maths problem to be used in the quiz"""

    operations = ['+', '-', '*', '/']

    # Randomly selects an operator from operations list.
    op = random.choice(operations)

    # Using the randomly chosen operator,  the program will calculate the answer.
    # Plus and subtraction sums.
    if op == '+' or op == "-":
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        if op == "+":
            answer = num1 + num2
        else:
            answer = num1 - num2
    # Multiplication and division sums.
    else:
        if op == '*':
            num1 = random.randint(1, 12)
            num2 = random.randint(1, 12)
            answer = num1 * num2
        else:
            # Picks the divisor and quotient directly so the dividend (num1) is
            # always an exact, non-zero multiple of the divisor.
            num2 = random.randint(1, 12)
            answer = random.randint(1, 12)
            num1 = num2 * answer

    question = f"What is {num1} {op} {num2}?"
    return question, answer


def score_for_attempt(attempts):
    """Maps the number of attempts already used (0, 1, or 2) to the points awarded
    for a correct answer: 10 on the first attempt, 5 on the second, 1 on the third."""
    if attempts == 0:
        return 10
    elif attempts == 1:
        return 5
    else:
        return 1


def ask_question(question, answer, name):
    """Asks the user to input the answer to the question and compares the user answer with the answer. User has
    3 attempts to answer the problem and will get a score dependent on which attempt they answer.
    Returns: a score for the question."""
    attempts = 0
    score = 0
    while attempts < 3:
        user_answer = input(f"{question} ")

        # Will only allow an integer as an answer: raises error if not.
        try:
            user_answer = int(user_answer)
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        # Determines the score based on the number of attempts. Gives varied responses to user depending on attempts.
        if user_answer == answer:
            score = score_for_attempt(attempts)
            if attempts == 0:
                print(f"{random.choice(vibes.get('positive_vibes'))}{name}! 10 points to you!")
            elif attempts == 1:
                print("Good job! 5 points!")
            else:
                print(f"You got it, {name}! Have a point!")
            break
        else:
            attempts += 1
            if attempts < 3:
                print(f"{random.choice(vibes.get('encouraging_vibes'))}{name}!")
    if attempts == 3:
        print(f"The correct answer was {answer}.")
    return score