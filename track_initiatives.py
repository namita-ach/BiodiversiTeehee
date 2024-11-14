from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'namita2024',
    'database': 'BiodiversityTracking'
}

# Function to get database connection
def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

# Route for the homepage displaying all initiatives
@app.route('/')
def index():
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor(dictionary=True)
        
        # Fetch all sustainability initiatives
        cursor.execute("SELECT * FROM SustainabilityInitiative")
        initiatives = cursor.fetchall()

        return render_template('track_initiative_index.html', initiatives=initiatives)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

# Route to track initiatives by species
@app.route('/track_species', methods=['GET', 'POST'])
def track_by_species():
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Fetch all species for the dropdown
        cursor.execute("SELECT SpeciesID, CommonName FROM Species")
        species_list = cursor.fetchall()

        initiatives = []
        if request.method == 'POST':
            species_id = request.form['species_id']
            
            # Query initiatives for the selected species
            cursor.execute("""
                SELECT SI.InitiativeName, S.CommonName, SI.StartDate, SI.EndDate
                FROM SustainabilityInitiative AS SI
                JOIN BiodiversityMetric AS BM ON SI.InitiativeID = BM.InitiativeID
                JOIN Species AS S ON BM.SpeciesID = S.SpeciesID
                WHERE S.SpeciesID = %s
            """, (species_id,))
            initiatives = cursor.fetchall()

        return render_template('track_by_species.html', species_list=species_list, initiatives=initiatives)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

# Route to track species by initiative
@app.route('/track_initiative', methods=['GET', 'POST'])
def track_by_initiative():
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Fetch all initiatives for the dropdown
        cursor.execute("SELECT InitiativeID, InitiativeName FROM SustainabilityInitiative")
        initiative_list = cursor.fetchall()

        species = []
        if request.method == 'POST':
            initiative_id = request.form['initiative_id']
            
            # Query species for the selected initiative
            cursor.execute("""
                SELECT S.CommonName, S.SpeciesID
                FROM Species AS S
                JOIN BiodiversityMetric AS BM ON S.SpeciesID = BM.SpeciesID
                WHERE BM.InitiativeID = %s
            """, (initiative_id,))
            species = cursor.fetchall()

        return render_template('track_by_initiative.html', initiative_list=initiative_list, species=species)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
