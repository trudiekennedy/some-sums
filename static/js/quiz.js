(function () {
  var quizEl = document.getElementById('quiz');
  var form = document.getElementById('answer-form');
  var input = document.getElementById('answer-input');
  var submitButton = document.getElementById('answer-submit');
  var questionText = document.getElementById('question-text');
  var feedback = document.getElementById('feedback');
  var scoreDisplay = document.getElementById('score-display');
  var roundNumEl = document.getElementById('round-num');
  var questionNumEl = document.getElementById('question-num');

  var questionsPerRound = parseInt(quizEl.dataset.questionsPerRound, 10);
  var currentRound = parseInt(quizEl.dataset.currentRound, 10);
  var currentQuestionNum = parseInt(quizEl.dataset.currentQuestionNum, 10);

  var ADVANCE_DELAY_MS = 900;

  function setFeedback(message, animationClass) {
    feedback.textContent = message;
    feedback.classList.remove('correct-pulse', 'incorrect-shake');
    if (animationClass) {
      // Re-trigger the animation even if the same class was just used.
      void feedback.offsetWidth;
      feedback.classList.add(animationClass);
    }
  }

  function advanceToNextQuestion(nextQuestion) {
    currentQuestionNum += 1;
    questionNumEl.textContent = currentQuestionNum;
    questionText.textContent = nextQuestion;
    input.value = '';
    input.focus();
  }

  function advanceToNextRound(nextQuestion) {
    currentRound += 1;
    currentQuestionNum = 1;
    roundNumEl.textContent = currentRound;
    questionNumEl.textContent = currentQuestionNum;
    questionText.textContent = nextQuestion;
    input.value = '';
    input.focus();
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    var value = input.value;
    if (value === '') {
      return;
    }

    submitButton.disabled = true;

    fetch('/api/answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answer: value }),
    })
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (!data.valid) {
          setFeedback(data.message, null);
          submitButton.disabled = false;
          return;
        }

        scoreDisplay.textContent = data.round_score;

        if (!data.resolved) {
          setFeedback(data.message, 'incorrect-shake');
          input.value = '';
          input.focus();
          submitButton.disabled = false;
          return;
        }

        setFeedback(data.message, data.correct ? 'correct-pulse' : 'incorrect-shake');

        setTimeout(function () {
          if (data.game_complete) {
            window.location.href = '/summary';
            return;
          }
          if (data.round_complete) {
            advanceToNextRound(data.next_question);
          } else {
            advanceToNextQuestion(data.next_question);
          }
          submitButton.disabled = false;
        }, ADVANCE_DELAY_MS);
      });
  });
})();
