import random
import time

# Captures player's name
name = input("What is your name? ")

# A list of positive affirmations to praise correct answers
positive_vibes = ["Nice one, ", "Wowee! You're on fire, ", "Got it one, ", "By gum! You're good, ", "Good stuff, ",
                  "Are you sure you're not using a calculator?! Great work, ", "You've been practising, "]
encouraging_vibes = ["Oof! Unlucky, ", "Hit the post with that, ", "Keep trying, ", "Close - try again, ",
                     "You can do it! Have another go, ", "This one's tough, but you can work it out, "]


def generate_question():
    """This function randomly generates the arithmetic questions: for addition and subtraction, numbers used will be
    between 1 & 100; for division and multiplication, numbers will be between 1 & 12 to support what an 8-year-old
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
        num1 = random.randint(1, 12)
        num2 = random.randint(1, 12)
        if op == '*':
            answer = num1 * num2
        else:
            answer = num1 // num2
            num1 = answer * num2

    question = f"What is {num1} {op} {num2}?"
    return question, answer


def ask_question(question, answer):
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
            if attempts == 0:
                score = 10
                print(f"{random.choice(positive_vibes)}{name}! 10 points to you!")
            elif attempts == 1:
                score = 5
                print("Good job! 5 points!")
            else:
                score = 1
                print(f"You got it, {name}! Have a point!")
            break
        else:
            attempts += 1
            if attempts < 3:
                print(f"{random.choice(encouraging_vibes)}{name}!")
    if attempts == 3:
        print(f"The correct answer was {answer}.")
    return score


def play_round(round_num):
    """Generates a round of the arithmetic game. Each round asks 5 questions, calling the ask_question
    function & will add up the score earned on each question. Function will time how long the round takes.
    Returns: total score for the round & duration """
    
    total_score = 0
    print(f"\nRound {round_num}.")
    
    # Records start time of the round. 
    start_time = time.time()
    
    # Calls generate_question 5 times & adds score of answer to total score
    for i in range(1, 6):
        print(f"\nQuestion {i}:\n")
        question, answer = generate_question()
        score = ask_question(question, answer)
        total_score += score
        
    # Records end time of round and then works out duration for return statement. 
    end_time = time.time()
    duration = end_time - start_time
    
    # Lets user know the score for the round.
    print(f"\nYour total score for round {round_num} is {total_score}!")
    return total_score, duration


def play_game():
    """This function plays a full game of the arithmetic quiz. The user is asked how many rounds they'd like to play
    and keeps track of the scores.
    Returns: score or average score depending on number of rounds and duration of the game"""
    print(f"Welcome {name}! Let's do some sums!\n")
    rounds = 0
    
    # Handles user not inputting a number or 0 for number of rounds.
    while True:
        try:
            rounds = int(input("How many rounds do you want to play? "))
        except ValueError:
            print("Please enter a number!")
            continue
        if rounds == 1:
            print(f"Ok, {name}! Let's play a round!")
            break
        elif rounds > 1:
            print(f"Let's go {name}! Onto the first round of {rounds}!")
            break
        else:
            print(f"Don't be like that, {name}! Give me a number greater than 0!")
    
    # Stores scores and duration of game.
    
    scores = []
    durations = []

    # Calls the play_round function the number of times defined by user. Stores score & duration in list variables.
    for i in range(1, rounds + 1):
        score, duration = play_round(i)
        scores.append(score)
        durations.append(duration)

    # Adds up total scores & divides by number of rounds to get an average score for the game.
    total_score = sum(scores)
    avg_score = total_score / rounds if rounds > 0 else 0

    # Works out duration of the game. Getting the minutes and seconds as separate variables.
    total_duration = sum(durations)
    minutes = total_duration // 60
    seconds = total_duration % 60

    # If >1 rounds are played, user will be told there average score (to 2 decimal places) & time across the rounds.
    if rounds > 1:
        print(f"\nThat was awesome sauce {name}! Your average score across {rounds} rounds was {avg_score:.2f}.")
        print(f"Thanks for playing - "
              f"it took you {minutes:.0f} minutes and {seconds:.0f} seconds to play {rounds} rounds!")
    # Else user will be told their score and time for the 1 round they played.
    else:
        print(f"\nGood job {name}! Your total score is {total_score}.")
        print(f"Thanks for playing -"
              f" it took you {minutes:.0f} minutes and {seconds:.0f} seconds to complete this game!")


play_game()
