from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'bramharoopasaraswati108'

# Helper function to query the database
def query_db(query, args=(), one=False):
    conn = sqlite3.connect('rvu.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    error = request.args.get('error')
    return render_template('login.html', error=error)

@app.route('/login', methods=['POST'])
def login():
    role = request.form['role']
    username = request.form['username']
    password = request.form['password']
    
    if role == 'student':
        user = query_db('SELECT * FROM students WHERE usn = ?', [username], one=True)
    elif role == 'teacher':
        user = query_db('SELECT * FROM teachers WHERE empid = ?', [username], one=True)
    elif role == 'admin':
        user = query_db('SELECT * FROM admins WHERE empid = ?', [username], one=True)
    else:
        user = None

    if user:
        if user['password'] == password:
            return redirect(url_for(f'{role}_dashboard', username=username))
        else:
            error = "Invalid credentials. Please try again."
    else:
        error = "Username doesn't exist. Contact the admin."
    
    return redirect(url_for('index', error=error))

@app.route('/student/dashboard')
def student_dashboard():
    username = request.args.get('username')
    student = query_db('SELECT * FROM students WHERE usn = ?', [username], one=True)
    return render_template('student_dashboard.html', student=student)

@app.route('/teacher/dashboard')
def teacher_dashboard():
    username = request.args.get('username')
    teacher = query_db('SELECT * FROM teachers WHERE empid = ?', [username], one=True)
    return render_template('teacher_dashboard.html', teacher=teacher)

@app.route('/admin/dashboard')
def admin_dashboard():
    username = request.args.get('username')
    admin = query_db('SELECT * FROM admins WHERE empid = ?', [username], one=True)
    return render_template('admin_dashboard.html', admin=admin)

@app.route('/admin/register_admission', methods=['GET', 'POST'])
def register_admission():
    username = request.args.get('username')  # Get the username from the query parameters
    if request.method == 'POST':
        usn = request.form['usn']
        name = request.form['name']
        password = request.form['password']
        conn = sqlite3.connect('rvu.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (usn, name, password) VALUES (?, ?, ?)', (usn, name, password))
        conn.commit()
        conn.close()
        flash('Student registered successfully', 'success')
        return redirect(url_for('admin_dashboard', username=username))
    return render_template('register_admissions.html', username=username)

@app.route('/admin/update_student_info', methods=['GET', 'POST'])
def update_student_info():
    username = request.args.get('username')  # Get the username from the query parameters
    if request.method == 'POST':
        usn = request.form['usn']
        name = request.form['name']
        password = request.form['password']
        attendance = request.form['attendance']
        marks_subject1 = request.form['marks_subject1']
        marks_subject2 = request.form['marks_subject2']
        marks_subject3 = request.form['marks_subject3']
        marks_subject4 = request.form['marks_subject4']
        # Logic to update data in 'students' table
        conn = sqlite3.connect('rvu.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE students 
            SET name = ?, password = ?, attendance = ?, marks_subject1 = ?, marks_subject2 = ?, marks_subject3 = ?, marks_subject4 = ? 
            WHERE usn = ?
        ''', (name, password, attendance, marks_subject1, marks_subject2, marks_subject3, marks_subject4, usn))
        conn.commit()
        conn.close()
        flash('Student information updated successfully', 'success')
        return redirect(url_for('admin_dashboard', username=username))
    return render_template('update_student_info.html', username=username)

@app.route('/admin/delete_student', methods=['GET', 'POST'])
def delete_student():
    username = request.args.get('username')  # Get the username from the query parameters
    if request.method == 'POST':
        usn = request.form['usn']
        conn = sqlite3.connect('rvu.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE usn = ?', (usn,))
        conn.commit()
        conn.close()
        flash('Student record deleted successfully', 'success')
        return redirect(url_for('admin_dashboard', username=username))
    return render_template('delete_student.html', username=username)

@app.route('/admin/student_list')
def student_list():
    username = request.args.get('username')  # Get the username from the query parameters
    students = query_db('SELECT * FROM students') 
    return render_template('student_list.html', students=students, username=username)

@app.route('/admin/announcements')
def announcements():
    return "Anouncements tab"

@app.route('/admin/delete_teacher', methods=['GET', 'POST'])
def delete_teacher():
    username = request.args.get('username')  # Get the username from the query parameters
    if request.method == 'POST':
        empid = request.form['empid']
        conn = sqlite3.connect('rvu.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM teachers WHERE empid = ?', (empid,))
        conn.commit()
        conn.close()
        flash('Teacher record deleted successfully', 'success')
        return redirect(url_for('admin_dashboard', username=username))
    return render_template('delete_teacher.html', username=username)

@app.route('/admin/delete_admin', methods=['GET', 'POST'])
def delete_admin():
    username = request.args.get('username')  # Get the username from the query parameters
    if request.method == 'POST':
        empid = request.form['empid']
        conn = sqlite3.connect('rvu.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM admins WHERE empid = ?', (empid,))
        conn.commit()
        conn.close()
        flash('Admin record deleted successfully', 'success')
        return redirect(url_for('admin_dashboard', username=username))
    return render_template('delete_admin.html', username=username)


@app.route('/admin/manage_events')
def manage_events():
    return "manage_events"
if __name__ == '__main__':
    app.run(debug=True)
