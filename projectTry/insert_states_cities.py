import sqlite3
import csv

# Create a connection to your SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the Cities table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cities (
        id INTEGER PRIMARY KEY,
        city TEXT,
        state_short_name TEXT,
        state_full_name TEXT,
        county TEXT,
        city_alias TEXT
    )
''')

# Function to import data from CSV into the database
def import_cities_from_csv(csv_file):
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        # Use the csv.reader for your style (delimited by '|')
        reader = csv.reader(file, delimiter='|')

        # Skip the header row if it exists
        next(reader)

        # Insert data into the Cities table
        for row in reader:
            if len(row) == 5:  # Ensure the row has the correct number of fields
                cursor.execute('''
                    INSERT INTO Cities (city, state_short_name, state_full_name, county, city_alias)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row[0], row[1], row[2], row[3], row[4]))

        conn.commit()

# Call the function to import cities from the CSV file
import_cities_from_csv('states_cities.csv')

# Close the connection
conn.close()

print("Cities data has been successfully imported into the database.")


