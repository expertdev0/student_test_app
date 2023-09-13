# Student Grade Records System

## Overview

This is a web-based application designed to help schools manage and analyze student grade records. It allows teachers to enter student information and grades, store them in a database, and generate various statistics and charts based on the data.

## Technical Stack

- Server:
  - Python version: 3.9.x
  - Bottle micro-framework for the backend
  - postgreSQL

- Client:
  - Node version: 14.20.x 
  - Ember.js for the web-based client
  - HTML, JavaScript, and CSS for the user interface

## Installation

### Server Setup

1. Install the required Python packages using pip:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Go to `backend/config.py` and Configure the database connection

   DB_CONFIG = {
      'host':     'your_postgresql_host',
      'port':     'your_postgresql_port',
      'dbname':   'your_database_name',
      'user':     'your_database_user',
      'password': 'your_database_password'
   }
3. Confirm that you installed PostgreSQL and Use this command to use `database.sql`

   ```bash
   pg_restore -U <your_username> -d <your_database_name> -f database.sql (sql file path)
   psql -U <your_username> -d <your_database_name>
   ```

4. Start the server:

   ```bash
   python main.py
   ```

### Client Setup

1. Navigate to the `frontend` directory in this project.

2. Install Ember.js and its dependencies:

   ```bash
   npm install -g ember-cli
   npm install
   ```

3. Start the Ember development server:

   ```bash
   ember serve
   ```

4. Access the web application by opening a web browser and visiting `http://localhost:4200`.

## Usage

### Data Entry

- Use the create-student page to enter student records, including their name, date of birth, class, and grade information (year, quarter, math grade, computer grade, and literature grade).

### Statistics

#### First Chart: Student General Average per Quarter

- Select a student from the list to load their total subject grade average per quarter.
- Each bar represents the student's average calculated from their three subjects' grades.

#### Second Chart: Subject Grades per Quarter (Filter per Subject)

- Select a subject (e.g., Math) to load grade averages from all students in each quarter.
- Each bar represents the average grade for the selected subject across all students in that quarter.

#### Third Chart: Year-Quarter General Average (Filter per Year - Quarter)

- Select a year and quarter (e.g., 2000 - Q1) to view the averages per subject for the selected quarter.
- Each bar represents the average of student grades for the selected subject in the specified quarter.

## API Endpoints

- **POST** `/student`: Store a student's information and grades.
- **GET** `/student-lists`: Retrieve all student lists.
- **GET** `/student-list-number`: Retrieve student list number.
- **GET** `/student-lists/<start_pos>/<limit>`: Retrieve all student lists per page.
- **GET** `/years`: Retrieve all years.
- **GET** `/student-info`: Retrieve some students info (only id and name)
- **GET** `/student/<student_id>`: Retrieve a student by ID.
- **GET** `/statistics/student-per-quarter/<student_id>`: Calculate and return student average per quarter.
- **GET** `/statistics/subject-grades/<subject>`: Calculate and return subject grades per quarter.
- **GET** `/statistics/year-quarter/<year>/<quarter>`: Calculate and return year-quarter general average.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow the standard open-source contribution guidelines.

## Acknowledgments

- Special thanks to the developers of Bottle and Ember.js for providing excellent frameworks for this project.

Feel free to customize this README file according to your specific project needs. Include any additional information, usage examples, or troubleshooting tips that may be relevant to your users.