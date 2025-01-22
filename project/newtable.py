import sqlite3

def create_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS new_recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    usage_count INTEGER DEFAULT 0,
                    user_id INTEGER,
                    link TEXT,
                    added_time TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )''')  

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
