from flask import Flask, request, render_template, redirect, flash, jsonify, session
from surveys import satisfaction_survey as survey
from flask_debugtoolbar import DebugToolbarExtension


RESPONSES_KEY = "responses"

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)



@app.route('/')
def show_survey():
    """survey intro"""
    title = survey.title
    instructions = survey.instructions
    
    return render_template('instruction.html', title=title, instructions=instructions)


@app.route('/begin', methods=['POST'])    
def start_survey():
    session[RESPONSES_KEY] = []
    
    return redirect('/questions/0')




@app.route('/questions/<int:qid>')
def all_questions(qid):
    """Display current question"""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):

        return redirect("/")

    if (len(responses) == len(survey.questions)):

        return redirect("/complete") 

    if (len(responses) != qid):

        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")       

    questions = survey.questions[qid]
    return render_template("surveyQuestions.html", question_num=qid, question=questions)


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")