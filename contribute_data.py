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

# Route for the landing page
@app.route('/')
def index():
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor()
        
        # Fetch all tables excluding log and user tables
        cursor.execute("SHOW TABLES")
        all_tables = [table[0] for table in cursor.fetchall()]
        excluded_tables = {'ContributionLog', 'Users'}
        tables = [table for table in all_tables if table not in excluded_tables]

        return render_template('contribute_data_index.html', tables=tables)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

# Route to select a table and enter data
@app.route('/contribute', methods=['GET', 'POST'])
def contribute_data():
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor()

        # Fetch all tables excluding log tables and user tables
        cursor.execute("SHOW TABLES")
        all_tables = [table[0] for table in cursor.fetchall()]
        excluded_tables = {'ContributionLog', 'Users'}
        tables = [table for table in all_tables if table not in excluded_tables]

        if request.method == 'POST':
            selected_table = request.form['selected_table']

            # Retrieve columns for the selected table
            cursor.execute(f"SHOW COLUMNS FROM {selected_table}")
            columns = [col[0] for col in cursor.fetchall()]

            # If form submission with data
            if 'column_data' in request.form:
                # Construct and execute insert statement for the selected table
                data = {col: request.form[col] for col in columns}
                columns_str = ", ".join(data.keys())
                values_str = ", ".join(["%s"] * len(data))
                cursor.execute(f"INSERT INTO {selected_table} ({columns_str}) VALUES ({values_str})", tuple(data.values()))
                connection.commit()

                return redirect(url_for('index'))

            return render_template('contribute_form.html', selected_table=selected_table, columns=columns)

        return render_template('contribute_select.html', tables=tables)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
