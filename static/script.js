// ======================================================
// TEACHER - ADD QUESTION
// ======================================================

async function addQuestion() {

    const question =
        document.getElementById("question").value.trim();

    const correctAnswer =
        document.getElementById("correctAnswer").value.trim();

    const message =
        document.getElementById("teacherMessage");


    if (!question) {

        message.innerHTML =
            "Please enter a question.";

        message.style.color = "red";

        return;
    }


    if (!correctAnswer) {

        message.innerHTML =
            "Please enter the correct answer.";

        message.style.color = "red";

        return;
    }


    try {

        const response = await fetch(
            "/teacher/questions",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    question: question,

                    correct_answer: correctAnswer

                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            message.innerHTML =
                data.detail || "Error adding question.";

            message.style.color = "red";

            return;
        }


        message.innerHTML =
            "Question added successfully!";

        message.style.color = "green";


        document.getElementById("question").value = "";

        document.getElementById("correctAnswer").value = "";


        loadTeacherQuestions();

    }

    catch (error) {

        message.innerHTML =
            "Cannot connect to server.";

        message.style.color = "red";

        console.error(error);
    }
}


// ======================================================
// SHOW QUESTIONS ON TEACHER PAGE
// ======================================================

async function loadTeacherQuestions() {

    const list =
        document.getElementById("questionList");


    if (!list) {

        return;
    }


    try {

        const response =
            await fetch("/exam/questions");


        const data =
            await response.json();


        list.innerHTML = "";


        if (data.questions.length === 0) {

            list.innerHTML =
                "<p>No questions added yet.</p>";

            return;
        }


        data.questions.forEach(
            (question, index) => {

                const div =
                    document.createElement("div");

                div.className =
                    "teacher-question";


                div.innerHTML = `

                    <div class="teacher-question-number">
                        Question ${index + 1}
                    </div>

                    <p>
                        ${escapeHtml(question.question)}
                    </p>

                `;


                list.appendChild(div);

            }
        );

    }

    catch (error) {

        console.error(error);
    }
}


// ======================================================
// STUDENT LOGIN
// ======================================================

async function studentLogin() {

    const studentId =
        document.getElementById("studentId").value.trim();

    const studentName =
        document.getElementById("studentName").value.trim();

    const message =
        document.getElementById("loginMessage");


    if (!studentId) {

        message.innerHTML =
            "Please enter Student ID.";

        message.style.color = "red";

        return;
    }


    if (!studentName) {

        message.innerHTML =
            "Please enter Student Name.";

        message.style.color = "red";

        return;
    }


    try {

        const response = await fetch(
            "/student/login",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    student_id: studentId,

                    name: studentName

                })
            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            message.innerHTML =
                data.detail || "Login failed.";

            message.style.color = "red";

            return;
        }


        // Save student information
        localStorage.setItem(
            "student_id",
            data.student_id
        );

        localStorage.setItem(
            "student_name",
            data.name
        );


        // Go to exam
        window.location.href =
            "/exam";

    }

    catch (error) {

        message.innerHTML =
            "Cannot connect to server.";

        message.style.color = "red";

        console.error(error);
    }
}


// ======================================================
// LOAD EXAM QUESTIONS
// ======================================================

async function loadExam() {

    const examContainer =
        document.getElementById(
            "examQuestions"
        );


    if (!examContainer) {

        return;
    }


    const studentId =
        localStorage.getItem(
            "student_id"
        );

    const studentName =
        localStorage.getItem(
            "student_name"
        );


    if (!studentId) {

        window.location.href =
            "/login";

        return;
    }


    const studentInfo =
        document.getElementById(
            "studentInfo"
        );


    studentInfo.innerHTML = `

        <div class="student-info">

            <strong>Student ID:</strong>
            ${escapeHtml(studentId)}

            <br>

            <strong>Student Name:</strong>
            ${escapeHtml(studentName)}

        </div>

    `;


    try {

        const response =
            await fetch(
                "/exam/questions"
            );


        const data =
            await response.json();


        examContainer.innerHTML = "";


        if (data.questions.length === 0) {

            examContainer.innerHTML = `

                <p class="loading">
                    No questions available.
                </p>

            `;

            return;
        }


        data.questions.forEach(
            (question, index) => {

                const div =
                    document.createElement(
                        "div"
                    );

                div.className =
                    "exam-question";


                div.innerHTML = `

                    <div class="question-number">

                        Question ${index + 1}

                    </div>


                    <div class="question-text">

                        ${escapeHtml(
                            question.question
                        )}

                    </div>


                    <label>
                        Your Answer
                    </label>


                    <textarea
                        class="answer-box"
                        id="answer-${question.id}"
                        placeholder="Enter your answer here..."
                    ></textarea>

                `;


                examContainer.appendChild(div);

            }
        );

    }

    catch (error) {

        examContainer.innerHTML = `

            <p style="color:red">
                Cannot load exam questions.
            </p>

        `;

        console.error(error);
    }
}


// ======================================================
// SUBMIT EXAM
// ======================================================

async function submitExam() {

    const studentId =
        localStorage.getItem(
            "student_id"
        );


    if (!studentId) {

        window.location.href =
            "/login";

        return;
    }


    const message =
        document.getElementById(
            "examMessage"
        );


    try {

        const response =
            await fetch(
                "/exam/questions"
            );


        const data =
            await response.json();


        let successCount = 0;


        for (
            const question
            of data.questions
        ) {

            const answerBox =
                document.getElementById(
                    `answer-${question.id}`
                );


            const studentAnswer =
                answerBox
                    ? answerBox.value.trim()
                    : "";


            const answerResponse =
                await fetch(
                    "/exam/answer",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            student_id:
                                studentId,

                            question_id:
                                question.id,

                            student_answer:
                                studentAnswer

                        })
                    }
                );


            if (answerResponse.ok) {

                successCount++;

            }

        }


        message.innerHTML =
            `Exam submitted successfully! ` +
            `${successCount} answers saved.`;

        message.style.color = "green";


        setTimeout(
            function() {

                window.location.href =
                    "/result";

            },
            1500
        );

    }

    catch (error) {

        message.innerHTML =
            "Error submitting exam.";

        message.style.color = "red";

        console.error(error);
    }
}


// ======================================================
// GET RESULT
// ======================================================

async function getResult() {

    const studentId =
        document.getElementById(
            "resultStudentId"
        ).value.trim();


    const message =
        document.getElementById(
            "resultMessage"
        );


    const resultBox =
        document.getElementById(
            "resultBox"
        );


    if (!studentId) {

        message.innerHTML =
            "Please enter Student ID.";

        message.style.color = "red";

        return;
    }


    try {

        const response =
            await fetch(
                `/result/${encodeURIComponent(
                    studentId
                )}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            message.innerHTML =
                data.detail || "Result not found.";

            message.style.color = "red";

            resultBox.style.display =
                "none";

            return;
        }


        message.innerHTML = "";

        resultBox.style.display =
            "block";


        resultBox.innerHTML = `

            <div class="result-row">

                <span class="result-label">
                    Student ID
                </span>

                <span class="result-value">
                    ${escapeHtml(
                        data.student_id
                    )}
                </span>

            </div>


            <div class="result-row">

                <span class="result-label">
                    Student Name
                </span>

                <span class="result-value">
                    ${escapeHtml(
                        data.student_name
                    )}
                </span>

            </div>


            <div class="result-row">

                <span class="result-label">
                    Total Questions
                </span>

                <span class="result-value">
                    ${data.total_questions}
                </span>

            </div>


            <div class="result-row">

                <span class="result-label">
                    Answered Questions
                </span>

                <span class="result-value">
                    ${data.answered_questions}
                </span>

            </div>


            <div class="result-row">

                <span class="result-label">
                    Correct Answers
                </span>

                <span class="result-value">
                    ${data.correct_answers}
                </span>

            </div>


            <div class="result-row">

                <span class="result-label">
                    Marks
                </span>

                <span class="result-value">
                    ${data.marks}
                </span>

            </div>


            <div class="final-score">

                ${data.percentage}%

            </div>

        `;

    }

    catch (error) {

        message.innerHTML =
            "Cannot connect to server.";

        message.style.color = "red";

        console.error(error);
    }
}


// ======================================================
// HTML SECURITY
// ======================================================

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent =
        text;

    return div.innerHTML;
}


// ======================================================
// PAGE LOADING
// ======================================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        // Teacher page
        loadTeacherQuestions();


        // Exam page
        loadExam();

    }
);