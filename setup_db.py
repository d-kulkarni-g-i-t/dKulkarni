import sqlite3

# Connect to the database (or create it)
conn = sqlite3.connect('rvu.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    usn TEXT PRIMARY KEY,
    name TEXT,
    password TEXT,
    attendance INTEGER,
    marks_subject1 INTEGER,
    marks_subject2 INTEGER,
    marks_subject3 INTEGER,
    marks_subject4 INTEGER,
    overall INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS teachers (
    empid TEXT PRIMARY KEY,
    name TEXT,
    password TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS admins (
    empid TEXT PRIMARY KEY,
    name TEXT,
    password TEXT
)
''')

# Insert sample data
cursor.execute('''
INSERT INTO students (usn, name, password, attendance, marks_subject1, marks_subject2, marks_subject3, marks_subject4, overall)
VALUES
    ('S123', 'S1', '01-01-2000', 90, 85, 88, 92, 89,90),
    ('S124', 'S2', '02-02-2000', 95, 90, 91, 89, 91,92)
''')

cursor.execute('''
INSERT INTO teachers (empid, name, password)
VALUES
    ('T001', 'T1', '01-01-2010'),
    ('T002', 'T2', '02-02-2011')
''')

cursor.execute('''
INSERT INTO admins (empid, name, password)
VALUES
    ('A001', 'Admin1', '01-01-2010'),
    ('A002', 'Admin2', '02-02-2011')
''')

# Save (commit) the changes and close the connection
conn.commit()
conn.close()

print("Database setup completed with sample data.")
