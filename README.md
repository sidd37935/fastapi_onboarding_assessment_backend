# Sample Onboarding & Assessment API

A simple Python backend (FastAPI) for a 3-screen assessment app:
1. Onboarding (collect name, phone, email)
2. Questions (MCQ - pick an option)
3. Report (summary of answers)

## Project structure

```
onboarding_api/
├── database_setup.sql   <- Run this in MySQL first (creates tables + sample questions)
├── database.py           <- MySQL connection settings
├── main.py                <- The 4 APIs
└── requirements.txt
```

## Step 1: Set up the database

Open MySQL (Workbench, terminal, or any client you use) and run the
entire `database_setup.sql` file. This will:
- Create a database called `onboarding_app`
- Create 4 tables: persons, questions, question_options, answers
- Insert 4 sample questions with options (car brand, colour, city, occupation)

```bash
mysql -u root -p < database_setup.sql
```

## Step 2: Update your MySQL credentials

Open `database.py` and update the `DB_CONFIG` dictionary with your
own MySQL username and password:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_PASSWORD_HERE",
    "database": "onboarding_app"
}
```

## Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the server

```bash
uvicorn main:app --reload
```

The API will start at: http://127.0.0.1:8000

## Step 5: Test it

FastAPI auto-generates an interactive docs page. Open this in your browser:

**http://127.0.0.1:8000/docs**

You can test all 4 APIs directly from there without needing Postman.

### Suggested testing order:

1. **POST /onboard** — Submit name, phone_number, email
   → Note down the `person_id` you get back

2. **GET /questions** — See all 4 questions with their options
   → Note down a `question_id` and an `option_id` you like

3. **POST /answer** — Submit using the `person_id`, `question_id`,
   and `selected_option_id` from steps 1 & 2
   → Repeat this for a few different questions

4. **GET /report/{person_id}** — Pass the person_id from step 1
   → See the full report: person info + all their answers

## Notes

- Sample questions included: favourite car brand, favourite colour,
  city, and occupation — covering the MCQ + city/area type questions
  mentioned in your task.
- Each API maps to one of the 4 screens/requirements your team described.
- This is intentionally kept simple (no auth, no advanced validation)
  since it's meant as a backend-only assignment demo.
