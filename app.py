from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)

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
    return render_template('admin_dashboard.html', admin=admin, username=username)


from flask import session

@app.route('/admin/register_admission', methods=['GET', 'POST'])
def register_admission():
    if request.method == 'POST':
        usn = request.form['usn']
        name = request.form['name']
        password = request.form['password']
        # Logic to insert data into 'students' table
        conn = sqlite3.connect('rvu.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (usn, name, password) VALUES (?, ?, ?)', (usn, name, password))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_dashboard', username=session.get('username')))
    return render_template('register_admissions.html')


@app.route('/admin/update_student_info', methods=['GET', 'POST'])
def update_student_info():
    if request.method == 'POST':
        usn = request.form['usn']
        name = request.form['name']
        password = request.form['password']
        # Logic to update data in 'students' table
        conn = sqlite3.connect('rvu.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE students SET name = ?, password = ? WHERE usn = ?', (name, password, usn))
        conn.commit()
        conn.close()
        flash('Student information updated successfully', 'success')
        return redirect(url_for('admin_dashboard', username=request.args.get('username')))
    return render_template('update_student_info.html', username=request.args.get('username'))

@app.route('/admin/delete_students')
def delete_students():
    # Your logic for deleting students
    return "Delete Students"

@app.route('/admin/student_list')
def student_list():
    # Your logic for displaying student list
    return "Student List"

@app.route('/admin/announcements')
def announcements():
    # Your logic for managing announcements
    return "Announcements"

@app.route('/admin/manage_events')
def manage_events():
    # Your logic for managing events
    return "Manage Events"


if __name__ == '__main__':
    app.run(debug=True)
