import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Update Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            ssn TEXT UNIQUE NOT NULL, -- Social Security Number
            phone TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Candidates table remains unchanged
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            party TEXT NOT NULL,
            image TEXT NOT NULL,
            votes INTEGER DEFAULT 0
        )
    ''')

    # Votes table remains unchanged
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            candidate_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (candidate_id) REFERENCES Candidates(id)
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print("Database initialized!")
