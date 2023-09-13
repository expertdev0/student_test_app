from db_connection import connection

# Create tables for students and grades
with connection.cursor() as cursor:
    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            date_of_birth DATE,
            student_class VARCHAR(255)
        )
    ''')
    # Create grades table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id SERIAL PRIMARY KEY,
            student_id INTEGER REFERENCES students(id),
            year INTEGER,
            quarter VARCHAR(10),
            mathematics INTEGER,
            computer_science INTEGER,
            literature INTEGER
        )
    ''')

# Commit the changes
connection.commit()