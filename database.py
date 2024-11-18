# Quan ly co so du lieu
# Ket noi PostgreSQL
import sqlite3
import pandas as pd

def Connect():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute(
    ''' CREATE TABLE IF NOT EXISTS students 
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            major TEXT,
            point REAL
        )
    '''
    )
    conn.commit()
    return conn

def AddStudent(conn, name, age, major, point):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, age, major, gpa) VALUES (?, ?, ?, ?)',
                  (name, age, major, point))
    conn.commit()
def GetStudent(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * from students')
    return cursor.fetchall()


def export_to_excel(conn):
    data = GetStudent(conn)
    df = pd.DataFrame(data, columns=['ID', 'Tên', 'Tuổi', 'Ngành', 'GPA'])
    df.to_excel('students.xlsx', index=False)

