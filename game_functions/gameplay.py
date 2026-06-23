'''
Functions associated with running rounds and a full game of someSums.
'''
import time
from game_functions.questions import generate_question, ask_question


def play_round(round_num, name):
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
        score = ask_question(question, answer, name)
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
    name = input("What is your name? ")
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
        score, duration = play_round(i, name)
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
