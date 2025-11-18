import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "students.db")

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Create Students table if it doesn't exist.
    Columns: idno, lastname, firstname, course, level, photo
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            idno TEXT PRIMARY KEY,
            lastname TEXT NOT NULL,
            firstname TEXT NOT NULL,
            course TEXT NOT NULL,
            level TEXT NOT NULL,
            photo TEXT
        )
    """)
    conn.commit()
    conn.close()

def getall(table):
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table} ORDER BY idno")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def getbyid(table, idno):
    if not idno:
        return None
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table} WHERE idno=?", (idno,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def insert(table, idno, lastname, firstname, course, level, photo):
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"""
        INSERT INTO {table} (idno, lastname, firstname, course, level, photo)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (idno, lastname, firstname, course, level, photo))
    conn.commit()
    conn.close()

def update(table, idno, lastname, firstname, course, level, photo=None):
    conn = connect()
    cur = conn.cursor()
    if photo is not None:
        cur.execute(f"""
            UPDATE {table}
            SET lastname=?, firstname=?, course=?, level=?, photo=?
            WHERE idno=?
        """, (lastname, firstname, course, level, photo, idno))
    else:
        cur.execute(f"""
            UPDATE {table}
            SET lastname=?, firstname=?, course=?, level=?
            WHERE idno=?
        """, (lastname, firstname, course, level, idno))
    conn.commit()
    conn.close()

def delete(table, idno):
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table} WHERE idno=?", (idno,))
    conn.commit()
    conn.close()
