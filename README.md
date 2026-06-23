# Some Sums
A personal project for my youngest niece who keeps on asking me to fire random arithmetic questions at her so she can show off what she's been learning at school.
Figured I would try and make it easier on myself & create something that will do the questions (and the answers!) for me instead of me trying to work it all out.

Unlike my niece, quick-fire arithmetic was never my strong-suit.

## Installation
To use this script, you will need Python 3 installed on your machine. You can download the latest version of Python from the official Python website.


## Usage
To use the script, simply run it from the command line using the following command:

`main.py`

This script is a simple quiz that asks 5 arithmetic questions per round. The user can define the number of rounds they want to play.

To cover what a 9-year-old might have learnt so far:
- The addition and subtraction questions are based on numbers up to 100.
- The multiplication and division questions go up to the 12-times table. Division questions are always built from
  an exact divisor and quotient, so the dividend is never 0.

The user has 3 attempts to get the question right: they'll get 10 points if right on the first attempt, 5 on the second, 1 on the last. 
The script gives a random selection of postive & encouraging responses to the user as they play. 

## Project structure
- `main.py` - entry point; starts the game.
- `game_functions/questions.py` - generates arithmetic questions (`generate_question`) and asks the user for an
  answer, scoring and responding accordingly (`ask_question`).
- `game_functions/gameplay.py` - runs a single round of 5 questions (`play_round`) and orchestrates a full game of
  one or more rounds (`play_game`).
- `data_files/vibes.py` - the positive and encouraging phrases used to respond to correct/incorrect answers.

## Testing
Unit tests live under `tests/` and use `pytest`. Run them with:

`pytest -m unit`

## Working on
Creating a fun front-end to make the game more appealing to the eye!
