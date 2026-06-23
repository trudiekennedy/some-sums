import os
import re
import sys

import pytest
from xprocess import ProcessStarter

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_PATH = os.path.join(REPO_ROOT, "app.py")

QUESTION_PATTERN = re.compile(r"^What is (-?\d+) ([+\-*/]) (-?\d+)\?$")


def compute_answer(num1, op, num2):
    if op == '+':
        return num1 + num2
    if op == '-':
        return num1 - num2
    if op == '*':
        return num1 * num2
    return num1 // num2


@pytest.fixture
def flask_server(xprocess):
    class Starter(ProcessStarter):
        pattern = "Running on http://127.0.0.1:5000"
        args = [sys.executable, APP_PATH]
        env = {
            **os.environ,
            "SECRET_KEY": "test-secret-key-for-e2e",
            "FLASK_DEBUG": "0",
        }
        timeout = 15

    xprocess.ensure("flask_server", Starter)
    yield "http://127.0.0.1:5000"
    xprocess.getinfo("flask_server").terminate()


@pytest.mark.e2e
def test_full_round_golden_path(flask_server, page):
    '''
    Drives a full 1-round game through a real browser: fills the start form,
    reads each rendered question, computes the correct answer itself (mirroring
    generate_question's own arithmetic rather than reading the answer off the
    page), submits it, and checks the final summary score.
    '''
    page.goto(flask_server + "/")

    page.fill("#name", "TestKid")
    page.fill("#rounds", "1")
    page.click("button[type=submit]")

    page.wait_for_url(re.compile(r".*/quiz"))

    for _ in range(5):
        question_text = page.locator("#question-text").inner_text()
        match = QUESTION_PATTERN.match(question_text)
        assert match is not None, f"Unexpected question format: {question_text!r}"
        num1, op, num2 = int(match.group(1)), match.group(2), int(match.group(3))
        answer = compute_answer(num1, op, num2)

        page.fill("#answer-input", str(answer))
        page.click("#answer-submit")

        page.locator("#feedback").wait_for(state="visible")
        feedback_text = page.locator("#feedback").inner_text()
        assert "points to you!" in feedback_text

        page.wait_for_timeout(1000)

    page.wait_for_url(re.compile(r".*/summary"))
    summary_text = page.locator(".card").inner_text()
    assert "TestKid" in summary_text
    assert "50" in summary_text
