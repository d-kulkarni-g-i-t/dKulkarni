from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock user data (Replace this with your actual user data retrieval logic)
users = {
    "student": {"USN": "S123", "DOB": "01-01-2000"},
    "teacher": {"empID": "T001", "DOJ": "01-01-2010"},
    "admin": {"empID": "A001", "DOJ": "01-01-2010"}
}

@app.route('/')
def index():
    error = request.args.get('error')
    return render_template('login.html', error=error)

@app.route('/login', methods=['POST'])
def login():
    role = request.form['role']
    if role in users:
        # Check user credentials (Replace this with your actual authentication logic)
        if role == "student" and request.form['usn'] == users[role]["USN"] and request.form['password'] == users[role]["DOB"]:
            return redirect(url_for(f'{role}_dashboard', username=request.form['usn']))
        elif role == "teacher" and request.form['empid'] == users[role]["empID"] and request.form['password'] == users[role]["DOJ"]:
            return redirect(url_for(f'{role}_dashboard', username=request.form['empid']))
        elif role == "admin" and request.form['empid'] == users[role]["empID"] and request.form['password'] == users[role]["DOJ"]:
            return redirect(url_for(f'{role}_dashboard', username=request.form['empid']))
        else:
            error = "Invalid credentials. Please try again."
    else:
        error = "Invalid role. Please select a valid role."

    return redirect(url_for('index', error=error))

@app.route('/student/dashboard')
def student_dashboard():
    username = request.args.get('username')
    return render_template('student_dashboard.html', username=username)

@app.route('/teacher/dashboard')
def teacher_dashboard():
    username = request.args.get('username')
    return render_template('teacher_dashboard.html', username=username)

@app.route('/admin/dashboard')
def admin_dashboard():
    username = request.args.get('username')
    return render_template('admin_dashboard.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
