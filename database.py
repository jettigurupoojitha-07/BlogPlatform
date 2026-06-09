import sqlite3

conn = sqlite3.connect('blog.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    user_id INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS comments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment TEXT,
    post_id INTEGER,
    user_id INTEGER
)
''')

conn.commit()
conn.close()

print("Database Created")