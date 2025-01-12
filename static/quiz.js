let quizData = [];
let currentQuestion = 0;
let score = 0;
let isAnswered = false;
let shuffledQuestions = [];

async function loadQuizData() {
    try {
        const response = await fetch('/static/quiz-data.json');
        const data = await response.json();
        quizData = data.questions;
    } catch (error) {
        console.error('Error loading quiz data:', error);
    }
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function startQuiz(event) {
    event.preventDefault();
    document.getElementById('quizModal').style.display = 'flex';
    currentQuestion = 0;
    score = 0;
    document.getElementById('score').textContent = score;
    // Shuffle questions at the start
    shuffledQuestions = shuffleArray([...quizData]);
    loadQuestion();
}

function loadQuestion() {
    if (currentQuestion >= shuffledQuestions.length) {
        showFinalScore();
        return;
    }

    const question = shuffledQuestions[currentQuestion];
    document.getElementById('questionText').textContent = question.question;
    
    const optionsContainer = document.getElementById('optionsContainer');
    optionsContainer.innerHTML = '';
    
    question.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.className = 'option-btn';
        button.textContent = option;
        button.onclick = () => checkAnswer(index);
        optionsContainer.appendChild(button);
    });

    document.getElementById('feedback').textContent = '';
    document.getElementById('nextBtn').style.display = 'none';
    isAnswered = false;
}

function checkAnswer(selectedIndex) {
    if (isAnswered) return;
    
    isAnswered = true;
    const question = shuffledQuestions[currentQuestion];
    const buttons = document.querySelectorAll('.option-btn');
    
    buttons.forEach(button => button.disabled = true);
    
    if (selectedIndex === question.correct) {
        score += 1;
        document.getElementById('score').textContent = score;
        buttons[selectedIndex].classList.add('correct');
        document.getElementById('feedback').textContent = 'إجابة صحيحة! ' + question.explanation;
    } else {
        buttons[selectedIndex].classList.add('wrong');
        buttons[question.correct].classList.add('correct');
        document.getElementById('feedback').textContent = 'إجابة خاطئة. ' + question.explanation;
    }
    
    document.getElementById('nextBtn').style.display = 'block';
}

function nextQuestion() {
    currentQuestion++;
    loadQuestion();
}

function endQuiz() {
    showFinalScore();
}

function showFinalScore() {
    const modal = document.getElementById('quizModal');
    const content = modal.querySelector('.quiz-content');
    const percentage = Math.round((score / shuffledQuestions.length) * 100);
    
    content.innerHTML = `
        <h2>نتيجة الاختبار</h2>
        <div class="final-score">
            <p>مجموع النقاط: ${score}</p>
            <p>عدد الأسئلة: ${shuffledQuestions.length}</p>
            <p>النسبة المئوية: ${percentage}%</p>
        </div>
        <button onclick="closeQuiz()" class="exit-btn">إغلاق</button>
    `;
}

function closeQuiz() {
    document.getElementById('quizModal').style.display = 'none';
}

// Load quiz data when page loads
document.addEventListener('DOMContentLoaded', loadQuizData); 