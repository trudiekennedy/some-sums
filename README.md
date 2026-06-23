# Some Sums
A personal project for my youngest niece who keeps on asking me to fire random arithmetic questions at her so she can show off what she's been learning at school.
Figured I would try and make it easier on myself & create something that will do the questions (and the answers!) for me instead of me trying to work it all out.

Unlike my niece, quick-fire arithmetic was never my strong-suit.

## Installation
To use this project, you will need Python 3 installed on your machine. You can download the latest version of Python from the official Python website.

Install the dependencies with:

`pip install -r requirements.txt`

## Usage
There are two ways to play: a command-line version, and a web version.

### Command line
Run it from the command line using the following command:

`python main.py`

### Web front-end
The web version is a single-player, browser-based quiz with a colourful, kid-friendly look.

1. Copy `.env.example` to `.env` and set `SECRET_KEY` to a long random string (e.g. `python -c "import secrets; print(secrets.token_hex(32))"`).
2. Run `python app.py` and open `http://127.0.0.1:5000` in your browser.

You'll enter your name and the number of rounds you want to play, then answer each question in place on the page - no reloads needed until the game ends.

### Both versions
Each round asks 5 arithmetic questions. The user can define the number of rounds they want to play.

To cover what a 9-year-old might have learnt so far:
- The addition and subtraction questions are based on numbers up to 100.
- The multiplication and division questions go up to the 12-times table. Division questions are always built from
  an exact divisor and quotient, so the dividend is never 0.

The user has 3 attempts to get the question right: they'll get 10 points if right on the first attempt, 5 on the second, 1 on the last. 
Both versions give a random selection of postive & encouraging responses to the user as they play. 

## Project structure
- `main.py` - CLI entry point; starts the command-line game.
- `app.py` - Flask entry point; starts the web front-end, with game progress kept in the browser session.
- `templates/`, `static/` - the web front-end's HTML, CSS and JS.
- `game_functions/questions.py` - generates arithmetic questions (`generate_question`) and asks the user for an
  answer, scoring and responding accordingly (`ask_question`, with the scoring rule shared via `score_for_attempt`).
- `game_functions/gameplay.py` - runs a single round of 5 questions (`play_round`) and orchestrates a full CLI game of
  one or more rounds (`play_game`).
- `data_files/vibes.py` - the positive and encouraging phrases used to respond to correct/incorrect answers.

## Testing
Tests live under `tests/` and use `pytest`. Fast unit tests (CLI logic + Flask routes) run with:

`pytest -m unit`

There's also one end-to-end browser test (using Playwright) that drives the web front-end in a real browser. Install the browser binaries once with `playwright install`, then run it with:

`pytest -m e2e`

## Working on
Adding user accounts and persistent score history to the web front-end.
