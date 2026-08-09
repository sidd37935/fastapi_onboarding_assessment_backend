-- ============================================================
-- Database Setup Script
-- Run this once in MySQL to create the database, tables,
-- and insert sample questions before starting the API.
-- ============================================================

CREATE DATABASE IF NOT EXISTS onboarding_app;
USE onboarding_app;

-- Table 1: persons
-- Stores basic info collected during onboarding (Screen 1)
CREATE TABLE IF NOT EXISTS persons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: questions
-- Stores MCQ-style questions shown on Screen 2
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text VARCHAR(255) NOT NULL
);

-- Table 3: question_options
-- Each question can have multiple options (1 row per option)
CREATE TABLE IF NOT EXISTS question_options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    option_text VARCHAR(100) NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Table 4: answers
-- Stores which option a person chose for each question
CREATE TABLE IF NOT EXISTS answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    question_id INT NOT NULL,
    selected_option_id INT NOT NULL,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (question_id) REFERENCES questions(id),
    FOREIGN KEY (selected_option_id) REFERENCES question_options(id)
);

-- ============================================================
-- Sample Questions (auto-generated, 4 questions as requested)
-- ============================================================

INSERT INTO questions (question_text) VALUES
('What is your favourite car brand?'),
('What is your favourite colour?'),
('Which city do you live in?'),
('What do you do for work?');

-- Options for Question 1: Favourite car brand
INSERT INTO question_options (question_id, option_text) VALUES
(1, 'Tesla'),
(1, 'BMW'),
(1, 'Toyota'),
(1, 'Maruti Suzuki');

-- Options for Question 2: Favourite colour
INSERT INTO question_options (question_id, option_text) VALUES
(2, 'Red'),
(2, 'Blue'),
(2, 'Green'),
(2, 'Black');

-- Options for Question 3: City
INSERT INTO question_options (question_id, option_text) VALUES
(3, 'Mumbai'),
(3, 'Delhi'),
(3, 'Bangalore'),
(3, 'Varanasi');

-- Options for Question 4: What do you do
INSERT INTO question_options (question_id, option_text) VALUES
(4, 'Student'),
(4, 'Software Engineer'),
(4, 'Business Owner'),
(4, 'Other');
