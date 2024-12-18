from flask import Flask, g
import sqlite3
import os

db_app = Flask(__name__)
DATABASE = os.path.join(os.getcwd(), "database.db")

def get_db():
    db = getattr(g, '_database', None)  # Check if database is already connected
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)  # Connect to SQLite database
        db.row_factory = sqlite3.Row  # This allows accessing rows as dictionaries
    return db

def get_data_from_db():
    db = get_db()  # Get database connection
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Menu")  # Query the 'Menu' table
    data = cursor.fetchall()  # Fetch all rows from the query
    return data

# Run this part of the code within the Flask app context
with db_app.app_context():
    menu_data = get_data_from_db()  # Get data from the database
    with open('output.txt', 'w', encoding='utf-8') as f:
        for row in menu_data:
            f.write(str(dict(row)) + '\n')
