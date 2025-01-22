from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# View Page
@app.route('/view')
def view_results():
    # Load SVG content
    with open('static/usa.svg', 'r') as svg_file:
        svg_content = svg_file.read()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all candidates and vote data
    cursor.execute('SELECT * FROM Candidates')
    candidates = cursor.fetchall()

    # Calculate total votes
    total_votes = sum(candidate['votes'] for candidate in candidates)

    # Prepare a list of candidates with calculated percentages
    candidate_list = []
    for candidate in candidates:
        candidate_dict = dict(candidate)  # Convert sqlite3.Row to a dictionary
        if total_votes > 0:
            candidate_dict['percentage'] = (candidate_dict['votes'] / total_votes) * 100
        else:
            candidate_dict['percentage'] = 0
        candidate_list.append(candidate_dict)

    # Fetch votes by state
    cursor.execute('''
        SELECT C.state_short_name, C.state_full_name, V.candidate_id, COUNT(*) AS vote_count
        FROM Votes V
        JOIN Users U ON V.user_id = U.id
        JOIN Cities C ON U.state = C.state_short_name
        GROUP BY C.state_short_name, C.state_full_name, V.candidate_id
    ''')
    votes_by_state = cursor.fetchall()

    # Calculate state colors based on vote counts
    state_colors = {}
    total_votes_by_state = {}

    for state in votes_by_state:
        state_short_name = state[0]
        state_full_name = state[1]
        candidate_id = state[2]
        vote_count = state[3]

        if state_short_name not in state_colors:
            state_colors[state_short_name] = {'name': state_full_name, 'votes': {}}
            total_votes_by_state[state_short_name] = 0  # Initialize total votes for each state

        # Add the vote count for this candidate in the state
        state_colors[state_short_name]['votes'][candidate_id] = vote_count
        total_votes_by_state[state_short_name] += vote_count  # Increment total votes for the state

    # Determine the leading candidate per state and calculate percentages
    for state, data in state_colors.items():
        total_votes = total_votes_by_state[state]
        trump_votes = data['votes'].get(1, 0)
        harris_votes = data['votes'].get(2, 0)

        # Calculate percentages for each candidate in the state
        if total_votes > 0:
            trump_percentage = (trump_votes / total_votes) * 100
            harris_percentage = (harris_votes / total_votes) * 100
        else:
            trump_percentage = harris_percentage = 0

        # Add percentage to the data
        state_colors[state]['trump_percentage'] = round(trump_percentage, 2)
        state_colors[state]['harris_percentage'] = round(harris_percentage, 2)

        # Determine the leading candidate per state
        if trump_votes > harris_votes:
            state_colors[state]['color'] = 'red'
        elif harris_votes > trump_votes:
            state_colors[state]['color'] = 'blue'
        else:
            state_colors[state]['color'] = 'gray'  # Tie or no data

    conn.close()

    # Pass the necessary data to the template
    return render_template('view.html', candidates=candidate_list, state_colors=state_colors, svg_content=svg_content)

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['email'] = user['email']  # Change this to store the email
            return redirect(url_for('vote'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

# Voting Page
@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    candidates = conn.execute('SELECT * FROM Candidates').fetchall()

    if request.method == 'POST':
        candidate_id = request.form['candidate']
        user_id = session['user_id']

        # Check if the user has already voted
        vote_check = conn.execute('SELECT * FROM Votes WHERE user_id = ?', (user_id,)).fetchone()
        conn.close()

        if vote_check:
            # User already voted
            return render_template(
                'message.html',
                message="You have already voted.",
                button_label="OK",
                redirect_url=url_for('view_results')
            )
        else:
            # Record the vote
            conn = get_db_connection()
            conn.execute('INSERT INTO Votes (user_id, candidate_id) VALUES (?, ?)', (user_id, candidate_id))
            conn.execute('UPDATE Candidates SET votes = votes + 1 WHERE id = ?', (candidate_id,))
            conn.commit()
            conn.close()

            # First-time voter message
            return render_template(
                'message.html',
                message="Thank you for voting!",
                button_label="OK",
                redirect_url=url_for('view_results')
            )

    conn.close()
    return render_template('vote.html', candidates=candidates)

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user inputs
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        ssn = request.form['ssn']
        phone = request.form['phone']
        email = request.form['email']
        city = request.form['city']
        state = request.form['state']
        password = request.form['password']

        # Insert user into the database
        conn = get_db_connection()
        try:
            conn.execute('''INSERT INTO Users (first_name, last_name, ssn, phone, email, city, state, password)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                         (first_name, last_name, ssn, phone, email, city, state, password))
            conn.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Error: SSN or email already exists.', 'error')
        finally:
            conn.close()

    return render_template('register.html')

# Get states for registration
@app.route('/get_states', methods=['GET'])
def get_states():
    conn = get_db_connection()
    states = conn.execute('SELECT DISTINCT state_full_name FROM Cities').fetchall()
    conn.close()
    return jsonify([state['state_full_name'] for state in states])

# Get cities for selected state
@app.route('/get_cities/<state>', methods=['GET'])
def get_cities(state):
    conn = get_db_connection()
    cities = conn.execute('SELECT city FROM Cities WHERE state_full_name = ?', (state,)).fetchall()
    conn.close()
    return jsonify([city['city'] for city in cities])

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)



