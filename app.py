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

def random_recipe():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Unable to connect to database"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM recipes ORDER BY RANDOM() LIMIT 1;")  # Modify 'recipes' to your table name
        random_row = cursor.fetchone()
        column_names = [desc[0] for desc in cursor.description]
        random_recipe = dict(zip(column_names, random_row))
        return jsonify({"random_recipe": random_recipe})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# POST Route to filter recipes based on chromosome values
@app.route('/api/v1/filter-recipes', methods=['POST'])
def filter_recipes():
    data = request.get_json()
    if not data or "chromosome_values" not in data:
        return jsonify({"error": "Request body must contain 'chromosome_values'"}), 400

    chromosome_values = data["chromosome_values"]
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Unable to connect to database"}), 500
    
    cursor = conn.cursor()
    try:
        query = """
        SELECT * 
        FROM recipes 
        WHERE category IN %s;
        """
        cursor.execute(query, (tuple(chromosome_values),))
        matching_recipes = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        recipes = [dict(zip(column_names, row)) for row in matching_recipes]
        return jsonify({"matching_recipes": recipes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
