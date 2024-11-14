from flask import Flask, render_template, request, redirect, url_for
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

# Homepage route displaying Species and SustainabilityInitiative tables
@app.route('/')
def home():
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor()

        # Fetch data from Species and SustainabilityInitiative tables
        cursor.execute("SELECT CommonName, ScientificName FROM Species")
        species_list = cursor.fetchall()

        cursor.execute("SELECT InitiativeName, Description FROM SustainabilityInitiative")
        initiatives_list = cursor.fetchall()

        return render_template('report_generation_index.html', species_list=species_list, initiatives_list=initiatives_list)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

# Route to generate biodiversity report
@app.route('/generate_report', methods=['GET', 'POST'])
def generate_report():
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor()

        # Fetch unique species and initiatives
        cursor.execute("SELECT DISTINCT CommonName FROM Species")
        species_list = cursor.fetchall()

        cursor.execute("SELECT DISTINCT InitiativeName FROM SustainabilityInitiative")
        initiatives_list = cursor.fetchall()

        report_data = None
        if request.method == 'POST':
            # Get form inputs
            species_name = request.form['species_name']
            initiative_name = request.form['initiative_name']

            # Query for matching metrics
            cursor.execute("""
                SELECT S.CommonName, S.ScientificName, SI.InitiativeName, AVG(BM.MetricValue) AS AvgMetricValue
                FROM Species AS S
                JOIN BiodiversityMetric AS BM ON S.SpeciesID = BM.SpeciesID
                JOIN SustainabilityInitiative AS SI ON BM.InitiativeID = SI.InitiativeID
                WHERE S.CommonName = %s AND SI.InitiativeName = %s
                GROUP BY S.CommonName, S.ScientificName, SI.InitiativeName
            """, (species_name, initiative_name))

            report_data = cursor.fetchall()

        return render_template('generate_report.html', species_list=species_list, initiatives_list=initiatives_list, report_data=report_data)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
