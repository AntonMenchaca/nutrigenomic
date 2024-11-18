from flask import Flask, jsonify
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Test database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def home():
    return jsonify({"message": "pinging api for nutrigenomic!"})

@app.route('/api/v1/resource')
def resource():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Unable to connect to database"}), 500
    
    cursor = conn.cursor()
    cursor.execute("SELECT 'This is an example resource from the database.';")
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({"data": data[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
