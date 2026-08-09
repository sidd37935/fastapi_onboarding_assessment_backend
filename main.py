"""
main.py
-------
Sample Assessment Application — Backend (API only)

This implements the 4 APIs your task asked for:
  1. POST /onboard         -> Screen 1: Onboard a new person
  2. GET  /questions       -> Screen 2: Get list of MCQ questions
  3. POST /answer          -> Screen 2: Submit an answer to a question
  4. GET  /report/{id}     -> Screen 3: Generate a report for a person

Run with:
    uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs to test all APIs interactively
(FastAPI auto-generates this Swagger UI for you).
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from database import get_connection

app = FastAPI(title="Sample Onboarding & Assessment API")


# ============================================================
# Request body schemas (these define what JSON the API expects)
# ============================================================

class OnboardRequest(BaseModel):
    name: str
    phone_number: str
    email: EmailStr


class AnswerRequest(BaseModel):
    person_id: int
    question_id: int
    selected_option_ids: list[int]   # supports multiple selections, e.g. [1, 3]


# ============================================================
# API 1: Onboarding (Screen 1)
# ============================================================

@app.post("/onboard")
def onboard_person(payload: OnboardRequest):
    """
    Takes basic info (name, phone, email) and creates a new
    person record. Returns the person_id which is needed for
    the next two APIs.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO persons (name, phone_number, email) VALUES (%s, %s, %s)",
        (payload.name, payload.phone_number, payload.email)
    )
    conn.commit()
    person_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return {
        "message": "Person onboarded successfully",
        "person_id": person_id
    }


# ============================================================
# API 2: Get Questions (Screen 2)
# ============================================================

@app.get("/questions")
def get_questions():
    """
    Returns all questions along with their options, so the
    frontend can render the MCQ screen.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, question_text FROM questions")
    questions = cursor.fetchall()

    # For each question, fetch its options
    for question in questions:
        cursor.execute(
            "SELECT id, option_text FROM question_options WHERE question_id = %s",
            (question["id"],)
        )
        question["options"] = cursor.fetchall()

    cursor.close()
    conn.close()

    return questions


# ============================================================
# API 3: Post Answer (Screen 2)
# ============================================================

@app.post("/answer")
def submit_answer(payload: AnswerRequest):
    """
    Saves the option(s) a person selected for a given question.
    Supports multiple selections (e.g. choosing both Toyota and
    Tesla for "favourite car brand") by inserting one row per
    selected option.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # quick check: make sure the person actually exists
    cursor.execute("SELECT id FROM persons WHERE id = %s", (payload.person_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Person not found")

    if not payload.selected_option_ids:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="At least one option must be selected")

    # remove any previous answers this person gave for this question,
    # so re-submitting (e.g. changing their mind) doesn't pile up duplicates
    cursor.execute(
        "DELETE FROM answers WHERE person_id = %s AND question_id = %s",
        (payload.person_id, payload.question_id)
    )

    # insert one row per selected option
    for option_id in payload.selected_option_ids:
        cursor.execute(
            """INSERT INTO answers (person_id, question_id, selected_option_id)
               VALUES (%s, %s, %s)""",
            (payload.person_id, payload.question_id, option_id)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message": "Answer(s) saved successfully",
        "options_saved": len(payload.selected_option_ids)
    }


# ============================================================
# API 4: Generate Report (Screen 3)
# ============================================================

@app.get("/report/{person_id}")
def generate_report(person_id: int):
    """
    Builds a summary report: person's basic info + every
    question they answered + which option(s) they picked.
    If a person selected multiple options for one question
    (e.g. Toyota + Tesla), they are grouped together under
    that question instead of showing as separate lines.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name, phone_number, email FROM persons WHERE id = %s", (person_id,))
    person = cursor.fetchone()

    if person is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Person not found")

    cursor.execute(
        """
        SELECT q.id AS question_id, q.question_text, o.option_text
        FROM answers a
        JOIN questions q ON a.question_id = q.id
        JOIN question_options o ON a.selected_option_id = o.id
        WHERE a.person_id = %s
        ORDER BY q.id
        """,
        (person_id,)
    )
    raw_rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # group multiple selected options under the same question
    grouped = {}
    for row in raw_rows:
        qid = row["question_id"]
        if qid not in grouped:
            grouped[qid] = {
                "question_text": row["question_text"],
                "selected_options": []
            }
        grouped[qid]["selected_options"].append(row["option_text"])

    answers = list(grouped.values())

    return {
        "person": person,
        "answers": answers,
        "summary": f"{person['name']} answered {len(answers)} question(s)."
    }


# ============================================================
# Root endpoint - just to confirm the API is running
# ============================================================

@app.get("/")
def root():
    return {"message": "Onboarding & Assessment API is running. Visit /docs to test."}
