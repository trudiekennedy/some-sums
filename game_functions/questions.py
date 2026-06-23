'''
Functions associated with creating and asking questions.
Utilises random package to generate Math questions. 
'''
import random

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