import os
import sqlite3
import re
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# Secret key used for session management and flash messages
app.secret_key = 'super_secret_student_management_key'

# Define database folder and path
# Placing the SQLite database in a 'data' subfolder allows easy Docker volume mounting
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DATABASE = os.path.join(DATA_DIR, 'students.db')


def get_db_connection():
    """Create and return a connection to the SQLite database with Row factory."""
    conn = sqlite3.connect(DATABASE)
    # Allows accessing columns by column name instead of index (e.g., student['name'])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the students table automatically if it does not already exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Initialize database table upon app startup
init_db()


def validate_student_data(name, email, course, phone):
    """Perform basic input validation. Returns (is_valid, error_message)."""
    if not name or not email or not course or not phone:
        return False, "All fields are required. Please fill out every field."
    
    # Simple regex for basic email format validation
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(email_regex, email):
        return False, "Please enter a valid email address (e.g., student@example.com)."
    
    # Basic phone length validation (at least 7 characters)
    if len(phone) < 7:
        return False, "Please enter a valid phone number (at least 7 digits)."
    
    return True, ""


# -------------------------------------------------------------
# 1. READ / VIEW STUDENTS (Dashboard)
# -------------------------------------------------------------
@app.route('/')
def index():
    """Display all registered students."""
    conn = get_db_connection()
    # Fetch all students ordered by newest first
    students = conn.execute('SELECT * FROM students ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', students=students)


# -------------------------------------------------------------
# 2. CREATE / ADD STUDENT
# -------------------------------------------------------------
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    """Render the add student form and handle student creation."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        course = request.form.get('course', '').strip()
        phone = request.form.get('phone', '').strip()

        # Validate inputs
        is_valid, error_message = validate_student_data(name, email, course, phone)
        if not is_valid:
            flash(error_message, 'danger')
            return render_template('add_student.html', name=name, email=email, course=course, phone=phone)

        # Insert record using parameterized query to prevent SQL injection
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO students (name, email, course, phone) VALUES (?, ?, ?, ?)',
            (name, email, course, phone)
        )
        conn.commit()
        conn.close()

        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_student.html')


# -------------------------------------------------------------
# 3. UPDATE / EDIT STUDENT
# -------------------------------------------------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    """Render the edit form with existing details and handle updates."""
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()

    if student is None:
        conn.close()
        flash(f'Student with ID {id} was not found.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        course = request.form.get('course', '').strip()
        phone = request.form.get('phone', '').strip()

        # Validate inputs
        is_valid, error_message = validate_student_data(name, email, course, phone)
        if not is_valid:
            conn.close()
            flash(error_message, 'danger')
            # Retain entered values if validation failed
            temp_student = {'id': id, 'name': name, 'email': email, 'course': course, 'phone': phone}
            return render_template('edit_student.html', student=temp_student)

        # Update record using parameterized SQL query
        conn.execute(
            'UPDATE students SET name = ?, email = ?, course = ?, phone = ? WHERE id = ?',
            (name, email, course, phone, id)
        )
        conn.commit()
        conn.close()

        flash('Student details updated successfully!', 'success')
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_student.html', student=student)


# -------------------------------------------------------------
# 4. DELETE STUDENT
# -------------------------------------------------------------
@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    """Delete a student record by ID."""
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()

    if student is None:
        conn.close()
        flash(f'Student with ID {id} was not found.', 'danger')
        return redirect(url_for('index'))

    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash(f'Student "{student["name"]}" deleted successfully!', 'success')
    return redirect(url_for('index'))


# -------------------------------------------------------------
# APPLICATION ENTRYPOINT
# -------------------------------------------------------------
if __name__ == '__main__':
    # host='0.0.0.0' allows external connections inside Docker container
    # port=5000 is the standard Flask port exposed in Dockerfile
    app.run(host='0.0.0.0', port=5000, debug=False)

