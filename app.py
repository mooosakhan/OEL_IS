from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL connection details
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'  # default MySQL username
MYSQL_PASSWORD = 'caamodel@1'  # replace with your MySQL password
MYSQL_DATABASE = 'usersdb'  # your database name

# Function to get the database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,        # MySQL host
            user=MYSQL_USER,        # MySQL username
            password=MYSQL_PASSWORD, # MySQL password
            database=MYSQL_DATABASE # Correct database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Route for user signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json  # Parse JSON data
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Hash the password
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Insert the user into the database
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        connection.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409
    finally:
        cursor.close()
        connection.close()

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json  # Parse JSON data
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Fetch the user from the database
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user['password'], password):
        cursor.close()
        connection.close()
        return jsonify({"message": "Login successful"}), 200
    else:
        cursor.close()
        connection.close()
        return jsonify({"error": "Invalid username or password"}), 401

# Main driver to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Debug mode enabled for development and troubleshooting
