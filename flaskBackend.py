import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "Welcome to the home page!"

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.route('/api/species', methods=['GET'])
def get_species():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM species")
    species = cursor.fetchall()
    conn.close()
    return jsonify(species)

@app.route('/api/species', methods=['POST'])
def add_species():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO species (name, category, location, date_observed) VALUES (%s, %s, %s, %s)",
                   (data['name'], data['category'], data['location'], data['date_observed']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 201

@app.route('/api/species/<int:id>', methods=['PUT'])
def update_species(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE species SET name=%s, category=%s, location=%s, date_observed=%s WHERE id=%s",
        (data['name'], data['category'], data['location'], data['date_observed'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "updated"}), 200

@app.route('/api/species/<int:id>', methods=['DELETE'])
def delete_species(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM species WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
