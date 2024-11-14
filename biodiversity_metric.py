'''from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from datetime import datetime

biodiversity_metric = Flask(__name__)

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

# Route to display all biodiversity metrics
@biodiversity_metric.route('/')
def home():
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM BiodiversityMetric")
        metrics = cursor.fetchall()

        return render_template('index.html', metrics=metrics)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

# Route to add a new biodiversity metric
@biodiversity_metric.route('/add', methods=['GET', 'POST'])
def add_metric():
    if request.method == 'POST':
        species_id = request.form['species_id']
        initiative_id = request.form['initiative_id']
        metric_value = request.form['metric_value']
        measurement_date = request.form['measurement_date']

        connection = get_db_connection()
        if not connection:
            return "Database connection error", 500

        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO BiodiversityMetric (SpeciesID, InitiativeID, MetricValue, MeasurementDate)
                VALUES (%s, %s, %s, %s)
            """, (species_id, initiative_id, metric_value, measurement_date))
            connection.commit()

            return redirect(url_for('home'))
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return "Database error", 500
        finally:
            cursor.close()
            connection.close()

    return render_template('add_metric.html')

# Route to update a biodiversity metric
@biodiversity_metric.route('/update/<int:metric_id>', methods=['GET', 'POST'])
def update_metric(metric_id):
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor()

        # Get current metric data
        cursor.execute("SELECT * FROM BiodiversityMetric WHERE MetricID = %s", (metric_id,))
        metric = cursor.fetchone()

        if request.method == 'POST':
            new_value = request.form['metric_value']
            cursor.execute("""
                UPDATE BiodiversityMetric
                SET MetricValue = %s
                WHERE MetricID = %s
            """, (new_value, metric_id))
            connection.commit()

            # Log the change in the log table
            cursor.execute("""
                INSERT INTO BiodiversityMetricLog (MetricID, ChangeDescription)
                VALUES (%s, %s)
            """, (metric_id, f"Updated to {new_value}"))
            connection.commit()

            return redirect(url_for('home'))

        return render_template('update_metric.html', metric=metric)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

# Route to delete a biodiversity metric
# Route to delete a biodiversity metric
@biodiversity_metric.route('/delete/<int:metric_id>', methods=['POST'])
def delete_metric(metric_id):
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor()

        # First, delete any related entries in BiodiversityMetricLog
        cursor.execute("DELETE FROM BiodiversityMetricLog WHERE MetricID = %s", (metric_id,))
        
        # Now, delete the metric from BiodiversityMetric
        cursor.execute("DELETE FROM BiodiversityMetric WHERE MetricID = %s", (metric_id,))
        
        # Commit both deletions
        connection.commit()

        # Log the deletion (optional)
        cursor.execute("""
            INSERT INTO BiodiversityMetricLog (MetricID, ChangeDescription)
            VALUES (%s, %s)
        """, (metric_id, "Metric entry deleted"))
        connection.commit()

        return redirect(url_for('home'))
    except mysql.connector.Error as err:
        # Return specific error messages
        error_message = (
            "Cannot delete or update a parent row: a foreign key constraint fails. "
            "There are one or more records in the BiodiversityMetricLog table that reference this MetricID. "
            "Therefore, MySQL prevents you from deleting it to maintain data integrity."
        )
        
        print(error_message)  # Optional: log to console for debugging
        return error_message, 500  # Return the error message to the client
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    biodiversity_metric.run(debug=True)'''

from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from datetime import datetime

biodiversity_metric = Flask(__name__)

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

# Route to display all biodiversity metrics
@biodiversity_metric.route('/')
def home():
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM BiodiversityMetric")
        metrics = cursor.fetchall()
        return render_template('biodiversity_metric.html', metrics=metrics)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

# Route to add a new biodiversity metric
@biodiversity_metric.route('/add', methods=['GET', 'POST'])
def add_metric():
    if request.method == 'POST':
        species_id = request.form['species_id']
        initiative_id = request.form['initiative_id']
        metric_value = request.form['metric_value']
        measurement_date = request.form['measurement_date']

        connection = get_db_connection()
        if not connection:
            return "Database connection error", 500

        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO BiodiversityMetric (SpeciesID, InitiativeID, MetricValue, MeasurementDate)
                VALUES (%s, %s, %s, %s)
            """, (species_id, initiative_id, metric_value, measurement_date))
            connection.commit()

            return redirect(url_for('home'))
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return "Database error", 500
        finally:
            cursor.close()
            connection.close()

    return render_template('add_metric.html')

# Route to update a biodiversity metric
@biodiversity_metric.route('/update/<int:metric_id>', methods=['GET', 'POST'])
def update_metric(metric_id):
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor()

        # Get current metric data
        cursor.execute("SELECT * FROM BiodiversityMetric WHERE MetricID = %s", (metric_id,))
        metric = cursor.fetchone()

        if request.method == 'POST':
            new_value = request.form['metric_value']
            cursor.execute("""
                UPDATE BiodiversityMetric
                SET MetricValue = %s
                WHERE MetricID = %s
            """, (new_value, metric_id))
            connection.commit()

            # Log the change in the log table
            cursor.execute("""
                INSERT INTO BiodiversityMetricLog (MetricID, ChangeDescription)
                VALUES (%s, %s)
            """, (metric_id, f"Updated to {new_value}"))
            connection.commit()

            return redirect(url_for('home'))

        return render_template('update_metric.html', metric=metric)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

# Route to delete a biodiversity metric
@biodiversity_metric.route('/delete/<int:metric_id>', methods=['POST'])
def delete_metric(metric_id):
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor()

        # Delete the metric
        cursor.execute("DELETE FROM BiodiversityMetric WHERE MetricID = %s", (metric_id,))
        connection.commit()

        # Log the deletion
        cursor.execute("""
            INSERT INTO BiodiversityMetricLog (MetricID, ChangeDescription)
            VALUES (%s, %s)
        """, (metric_id, "Metric entry deleted"))
        connection.commit()

        return redirect(url_for('home'))
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Cannot delete or update a parent row: a foreign key constraint fails (`BiodiversityTracking`.`BiodiversityMetricLog`, CONSTRAINT `BiodiversityMetricLog_ibfk_1` FOREIGN KEY (`MetricID`) REFERENCES `BiodiversityMetric` (`MetricID`))", 500
    finally:
        cursor.close()
        connection.close()

# Route to view metrics by species
@biodiversity_metric.route('/species/<int:species_id>')
def view_by_species(species_id):
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM BiodiversityMetric WHERE SpeciesID = %s", (species_id,))
        metrics = cursor.fetchall()
        return render_template('species_metrics.html', metrics=metrics)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

# Route to fetch aggregated metrics
@biodiversity_metric.route('/aggregate')
def aggregate():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT SpeciesID, 
               MAX(MetricValue) - MIN(MetricValue) AS MetricRange
        FROM BiodiversityMetric
        GROUP BY SpeciesID;
    """)
    aggregate_results = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('aggregate.html', aggregate_results=aggregate_results)

if __name__ == '__main__':
    biodiversity_metric.run(debug=True)
