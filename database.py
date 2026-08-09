"""
database.py
------------
Handles the MySQL connection. Keeping this separate from main.py
keeps the connection logic reusable and easy to change later
(e.g. if you switch to a connection pool or a different DB).
"""

import mysql.connector
from mysql.connector import Error

# ---------------------------------------------------------
# UPDATE THESE WITH YOUR OWN MYSQL CREDENTIALS
# ---------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # change if you use a different MySQL user
    "password": "Pandey@123",          # put your MySQL password here
    "database": "onboarding_app"
}


def get_connection():
    """
    Opens and returns a new MySQL connection.
    Called fresh inside every API endpoint (simple approach,
    good enough for an assignment / small project).
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        raise
