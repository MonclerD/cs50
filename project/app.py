from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import hashlib
import requests

app = Flask(__name__)
app.secret_key = 'secret_key'


def execute_query(query, params=()):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()


def fetch_data(query, params=()):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(query, params)
    data = c.fetchall()
    conn.close()
    return data


def update_schema():
    try:
        execute_query('''ALTER TABLE recipes ADD COLUMN added_time TEXT;''')
    except sqlite3.OperationalError:

        pass

@app.route('/')
def home():
    logged_in = 'user_id' in session
    return render_template('index.html', logged_in=logged_in)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/recipe_search', methods=['GET', 'POST'])
def recipe_search():
    user_id = session.get('user_id')
    logged_in = bool(user_id)

    if not logged_in:
        return redirect(url_for('login'))

    recipes = []
    if request.method == 'POST':
        ingredients = request.form['ingredients']

        if ingredients:
            apiKey = 'd815bce38aae44e3a97daeb38eb1b50d'
            url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey={apiKey}"

            try:
                response = requests.get(url)
                recipes = response.json()
            except Exception as e:
                print(f"Error fetching recipes: {e}")

        return render_template('recipe_search.html', logged_in=logged_in, ingredients=ingredients, recipes=recipes)

    return render_template('recipe_search.html', logged_in=logged_in)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        age = request.form['age']
        weight = request.form['weight']
        gender = request.form['gender']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        execute_query('''INSERT INTO users (name, surname, email, age, weight, gender, password)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (name, surname, email, age, weight, gender, password_hash))

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        user = fetch_data('''SELECT * FROM users WHERE email = ? AND password = ?''',
                          (email, password_hash))
        if user:
            session['user_id'] = user[0][0]
            return redirect(url_for('account_status'))
        else:
            return 'Invalid credentials!'

    return render_template('login.html')

@app.route('/account')
def account_status():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = fetch_data('''SELECT * FROM users WHERE id = ?''', (user_id,))
    recipes = fetch_data('''SELECT * FROM recipes WHERE user_id = ?''', (user_id,))

    usage_history = fetch_data('''SELECT r.name, h.date
                                  FROM recipe_usage_history h
                                  JOIN recipes r ON r.id = h.recipe_id
                                  WHERE h.user_id = ?''', (user_id,))

    logged_in = True
    return render_template('account.html', user=user[0], recipes=recipes, usage_history=usage_history, logged_in=logged_in)

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    recipe_name = request.form['recipe_name']
    recipe_link = request.form['recipe_link']
    added_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    if not recipe_link.startswith("https://"):
        return "Invalid URL format for the recipe link!"


    execute_query('''INSERT INTO recipes (user_id, name, link, added_time)
                     VALUES (?, ?, ?, ?)''', (user_id, recipe_name, recipe_link, added_time))

    return redirect(url_for('account_status'))

@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))


    execute_query('''DELETE FROM recipes WHERE id = ? AND user_id = ?''', (recipe_id, user_id))

    return redirect(url_for('account_status'))

if __name__ == '__main__':
    update_schema()  
    app.run(debug=True)
