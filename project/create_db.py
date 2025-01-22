import sqlite3

def create_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    age INTEGER,
                    weight REAL,
                    gender TEXT,
                    password TEXT NOT NULL)''')

    # Create Recipes table
    c.execute('''CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    usage_count INTEGER DEFAULT 0)''')

    # Create Recipe Usage History table
    c.execute('''CREATE TABLE IF NOT EXISTS recipe_usage_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    recipe_id INTEGER,
                    date TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(recipe_id) REFERENCES recipes(id))''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()






