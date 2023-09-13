from bottle import Bottle, request, response, HTTPResponse, HTTPError
import json
from truckpad.bottle.cors import CorsPlugin, enable_cors
from db_connection import connection
from decimal import Decimal

app = Bottle()

# Create a student list
@enable_cors
@app.post('/student')
def create_student():
    data = request.json
    name = data.get('name')
    date_of_birth = data.get('dateOfBirth')
    student_class = data.get('studentClass')
    year = data.get('year')
    quarter = data.get('quarter')
    math_grade = data.get('mathGrade')
    computer_grade = data.get('computerGrade')
    literature_grade = data.get('literatureGrade')

    # Check if a student with the same name, birthday, classname exists 
    with connection.cursor() as cursor:
        cursor.execute('SELECT id \
                        FROM students \
                        WHERE name = %s AND date_of_birth = %s AND student_class = %s', (name, date_of_birth, student_class, )) 
        result = cursor.fetchone() 
        if result:
            student_id = result[0]
        else:
            student_id = None
    # Insert student into the database
    if student_id is None:
        print("hhh")
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO students (name, date_of_birth, student_class) VALUES (%s, %s, %s) RETURNING id',
                (name, date_of_birth, student_class)
            )
            student_id = cursor.fetchone()[0]

    with connection.cursor() as cursor:
                
        cursor.execute(
            'INSERT INTO grades (student_id, year, quarter, mathematics, computer_science, literature)'
            'VALUES (%s, %s, %s, %s, %s, %s)',
            (student_id, year, quarter, math_grade, computer_grade, literature_grade)
        )
    
    connection.commit()
    
    response.status = 201  # Created
    return {'id': student_id}
 
# Retrieve all student lists
@enable_cors
@app.get('/student-lists')
def get_student_lists():
    with connection.cursor() as cursor:
        cursor.execute('SELECT students.*, grades.year, grades.quarter, grades.mathematics, grades.computer_science, grades.literature FROM students \
                        INNER JOIN grades ON students.id = grades.student_id')
        students = cursor.fetchall()
    
    students_json = []
    for student in students:
        student_dict = {
            'id': student[0],
            'name': student[1],
            'date_of_birth': student[2].strftime('%Y-%m-%d'),  # Convert date to string
            'student_class': student[3],
            'year' : student[4],
            'quarter': student[5],
            'mathematics': student[6],
            'computer_science': student[7],
            'literature': student[8],
        }
        students_json.append(student_dict)

    # Set the response content type to JSON
    response.content_type = 'application/json'

    # Return the JSON data
    return json.dumps({'students': students_json})

# Retrieve student list number
@enable_cors
@app.get('/student-list-number')
def get_student_list_number():
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM grades')
        result = cursor.fetchone()
        if result is None:
            number = None
        else:
            number = result[0]
    print(number)

    # Set the response content type to JSON
    response.content_type = 'application/json'

    # Return the JSON data
    return json.dumps({'number': number})

# Retrieve all student lists per page
@enable_cors
@app.get('/student-lists/<start_pos>/<limit>')
def get_students_per_page(start_pos, limit):
    with connection.cursor() as cursor:
        cursor.execute('SELECT students.*, grades.year, grades.quarter, grades.mathematics, grades.computer_science, grades.literature FROM students \
                        INNER JOIN grades ON students.id = grades.student_id \
                        ORDER BY student_id \
                        LIMIT %s \
                        OFFSET %s', (limit, start_pos))
        students = cursor.fetchall()
    
    students_json = []
    for student in students:
        student_dict = {
            'id': student[0],
            'name': student[1],
            'date_of_birth': student[2].strftime('%Y-%m-%d'),  # Convert date to string
            'student_class': student[3],
            'year' : student[4],
            'quarter': student[5],
            'mathematics': student[6],
            'computer_science': student[7],
            'literature': student[8],
        }
        students_json.append(student_dict)

    # Set the response content type to JSON
    response.content_type = 'application/json'

    # Return the JSON data
    return json.dumps({'students': students_json})

# Retrieve all years
@enable_cors
@app.get('/years')
def get_years():
    with connection.cursor() as cursor:
        cursor.execute('SELECT year FROM grades \
                        GROUP BY year \
                        ORDER BY year')
        results = cursor.fetchall()
    
    results_json = []
    if results:
        for result in results:
            result_dict = {
                'year' : result[0],
            }
            results_json.append(result_dict)
    # Set the response content type to JSON
    response.content_type = 'application/json'

    # Return the JSON data
    return json.dumps({'years': results_json})

# Retrieve some students info (only id and name)
@enable_cors
@app.get('/student-info')
def get_studentsInfo():
    with connection.cursor() as cursor:
        cursor.execute('SELECT id, name FROM students')
        students = cursor.fetchall()
    students_json = []
    for student in students:
        student_dict = {
            'id': student[0],
            'name': student[1],
        }
        students_json.append(student_dict)

    # Set the response content type to JSON
    response.content_type = 'application/json'

    # Return the JSON data
    return json.dumps({'students': students_json})
    
# Retrieve a specific student by ID
@enable_cors
@app.get('/student/<student_id>')
def get_student(student_id):
    with connection.cursor() as cursor:
        cursor.execute('SELECT students.*, grades.year, grades.quarter, grades.mathematics, grades.computer_science, grades.literature FROM students \
                                  INNER JOIN grades ON students.id = grades.student_id \
                                  WHERE student_id = %s', (student_id ,))
        
        results = cursor.fetchall()
        results_json = []
        print(results)
        for result in results:
            result = {
                'id': result[0],
                'name': result[1],
                'date_of_birth': result[2].strftime('%Y-%m-%d'),  # Convert date to string
                'student_class': result[3],
                'year' : result[4],
                'quarter': result[5],
                'mathematics': result[6],
                'computer_science': result[7],
                'literature': result[8],
            }
            results_json.append(result)
        
        # Set the response content type to JSON
        response.content_type = 'application/json'

        # Return the JSON data
        return json.dumps(results_json)
    
        if not student:
            raise HTTPError(404, 'Student not found')
        
# Calculate and return student average per quarter
@enable_cors
@app.route('/statistics/student-per-quarter/<student_id>', method='GET')
def get_student_average_per_quarter(student_id):
    try:
        with connection.cursor() as cursor:
            # Calculate student average per quarter
            cursor.execute('''
                SELECT quarter, year, AVG(mathematics + computer_science + literature)/3 AS average
                FROM grades
                WHERE student_id = %s
                GROUP BY year, quarter
                ORDER BY year, quarter
            ''', (student_id,))
            
            results = cursor.fetchall()
            print(results)
            results_json = []
            print(results)
            for result in results:
                result = {
                    'quarter' : result[0],
                    'year': result[1],
                    'average': round(float(result[2]), 3),
                }
                results_json.append(result)
            
            # Set the response content type to JSON
            response.content_type = 'application/json'

            # Return the JSON data
            return json.dumps(results_json)
    
    except Exception as e:
        raise HTTPError(500, str(e))

# Calculate and return subject grades per quarter
@enable_cors
@app.route('/statistics/subject-grades/<subject>', method = 'GET')
def get_subject_grades_per_quarter(subject):
    try:
        with connection.cursor() as cursor:
            # Calculate subject grades per quarter
            cursor.execute('''
                SELECT year, quarter, AVG({}) as avg_subject
                FROM grades
                GROUP BY year, quarter
                ORDER BY year, quarter
            '''.format(subject))
            
            results = cursor.fetchall()
            results_json = []
            print(results)
            for result in results:
                result = {
                    'year' : result[0],
                    'quarter': result[1],
                    'average': round(float(result[2]), 3),
                }
                results_json.append(result)
            
            # Set the response content type to JSON
            response.content_type = 'application/json'

            # Return the JSON data
            return json.dumps(results_json)
    
    except Exception as e:
        raise HTTPError(500, str(e))

# Calculate and return year-quarter general average
@enable_cors
@app.route('/statistics/year-quarter/<year>/<quarter>', method = 'GET')
def get_year_quarter_general_average(year, quarter):
    try:
        with connection.cursor() as cursor:
            # Calculate year-quarter general average
            cursor.execute('''
                SELECT AVG(mathematics) as math, AVG(computer_science) as com, AVG(literature) as lit
                FROM grades
                WHERE year = %s AND quarter = %s
                GROUP BY year, quarter
            ''', (year, quarter, ))
            
            result = cursor.fetchone()
            print(result)
            if result is None:
                return {'status': 'no data'}
            else:
                result = {
                    'mathematics' : round(float(result[0]), 3),
                    'computer_science': round(float(result[1]), 3),
                    'literature': round(float(result[2]), 3),
                }

                
                # Set the response content type to JSON
                response.content_type = 'application/json'

                # Return the JSON data
                return json.dumps(result)
    
    except Exception as e:
        raise HTTPError(500, str(e))
