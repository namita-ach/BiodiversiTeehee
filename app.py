from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Use your password
        database="BiodiversityTrackingSystem"  # Your database name
    )
@app.route('/')
def home():
    return render_template('homepage.html')  # You can create an index.html for the homepage

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            # Access form data
            userid = request.form['UserID']
            username = request.form['Username']
            password = request.form['Password']
            userrole = request.form['UserRole']
        except KeyError as e:
            flash(f"Missing form field: {e}")
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert user into database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Users (UserID, Username, PasswordHash, UserRole) VALUES (%s, %s, %s, %s)",
               (userid, username, hashed_password, userrole))

        connection.commit()
        cursor.close()
        connection.close()
        
        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')

        if not username or not password:
            flash('Username and password are required.')
            return render_template('login.html')

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT UserID, PasswordHash, UserRole FROM users WHERE Username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        print(f"User fetched from DB: {user}")  # Debugging line

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            session['user_id'] = user[0]  # Assuming UserID is now used
            session['role'] = user[2]

            print(f"Session User ID: {session['user_id']}, Role: {session['role']}")  # Debugging line

            if user[2] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user[2] == 'user' or 'volunteer' or 'researcher' or 'cityplanner' or 'cityscientist' or 'policy':
                return redirect(url_for('secpage'))
        
        flash('Invalid username or password.')

    return render_template('login.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    # Admin-specific content
    return render_template('admin_dashboard.html')

@app.route('/secpage')
def secpage():
    if 'user_id' not in session:
        flash("You need to log in first.")
        return redirect(url_for('login'))

    # Render different content based on role
    if session['role'] == 'admin':
        return render_template('admin_dashboard.html')  # Admin specific content
    else:
        return render_template('secpage.html')  # User specific content

@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create':
            username = request.form.get('username')
            password = request.form.get('password')
            userrole = request.form.get('userrole')

            if not username or not password:
                flash('Username and password are required.')
                return redirect(url_for('manage_users'))  # Redirect to avoid resubmission

            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert user into database
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (Username, PasswordHash, UserRole) VALUES (%s, %s, %s)",
                           (username, hashed_password, userrole))
            connection.commit()
            cursor.close()
            connection.close()

            flash('Account created successfully! Please log in.')
            return redirect(url_for('manage_users'))  # Redirect to avoid resubmission

        elif action == 'delete':
            userid = request.form.get('userid')
            # Delete user from database
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM users WHERE UserID = %s", (userid,))
            connection.commit()
            cursor.close()
            connection.close()

            return redirect(url_for('manage_users'))  # Redirect to avoid resubmission

    # Fetch all users from the database
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT UserID, Username, UserRole FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('manage_users.html', users=users)

@app.route('/find_collaborators', methods=['GET', 'POST'])
def find_collaborators():
    if request.method == 'POST':
        selected_role = request.form.get('role')
        if selected_role:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT UserID, Username FROM users WHERE UserRole = %s", (selected_role,))
            collaborators = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template('find_collaborators.html', collaborators=collaborators, selected_role=selected_role)

    return render_template('find_collaborators.html')

@app.route('/biodiversity_metric')
def biodiversity_metric():
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
@app.route('/add', methods=['GET', 'POST'])
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

            return redirect(url_for('biodiversity_metric'))
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return "Database error", 500
        finally:
            cursor.close()
            connection.close()

    return render_template('add_metric.html')

# Route to update a biodiversity metric
@app.route('/update/<int:metric_id>', methods=['GET', 'POST'])
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

            return redirect(url_for('biodiversity_metric'))

        return render_template('update_metric.html', metric=metric)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

@app.route('/aggregate')
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

# Route to view metrics by species
@app.route('/species/<int:species_id>')
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

@app.route('/delete/<int:metric_id>', methods=['POST'])
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

        return redirect(url_for('biodiversity_metric'))
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Cannot delete or update a parent row: a foreign key constraint fails (`BiodiversityTracking`.`BiodiversityMetricLog`, CONSTRAINT `BiodiversityMetricLog_ibfk_1` FOREIGN KEY (`MetricID`) REFERENCES `BiodiversityMetric` (`MetricID`))", 500
    finally:
        cursor.close()
        connection.close()

def get_available_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    conn.close()
    return tables

# Fetch columns for a specific table
def get_table_columns(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()
    conn.close()
    return columns

@app.route('/contribute_data_index')
def contribute_data_index():
    tables = get_available_tables()
    return render_template('contribute_data_index.html', tables=tables)

@app.route('/contribute_select', methods=['GET', 'POST'])
def contribute_select():
    tables = get_available_tables()
    return render_template('contribute_select.html', tables=tables)

@app.route('/contribute_data', methods=['POST'])
def contribute_data():
    selected_table = request.form.get('selected_table')
    if not selected_table:
        return "No table selected", 400

    # Retrieve column names for the selected table
    columns = get_table_columns(selected_table)

    if 'column_data' in request.form:
        # Collect data for each column
        data = {col: request.form[col] for col in columns}

        # Insert data into the selected table
        conn = get_db_connection()
        cursor = conn.cursor()
        column_names = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        insert_query = f"INSERT INTO {selected_table} ({column_names}) VALUES ({placeholders})"
        cursor.execute(insert_query, list(data.values()))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('contribute_data_index'))

    # Render the form with columns
    return render_template('contribute_form.html', selected_table=selected_table, columns=columns)

@app.route('/report_generation_index')
def report_generation_index():
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

# Route for the homepage displaying all initiatives
@app.route('/track_initiative_index')
def track_initiative_index():
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
