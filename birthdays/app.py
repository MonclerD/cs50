import os
import re

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        if not name or not month or not day:
            flash("All fields are required!")
            return redirect("/")
        if not re.match(r"^[A-Za-z .'-]{2,50}$", name):
            flash("Name must be 2-50 characters long include letters, spaces, periods, hyphens, and apostrophes")
            return redirect("/")

        try:
            month = int(month)
            day = int(day)
            if month < 1 or month > 12 or day < 1 or day > 31:
                flash("Invalid date!")
                return redirect("/")
        except ValueError:
            flash("Month and day must be numbers")
            return redirect("/")

        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)
        return redirect("/")

    else:
        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", birthdays=birthdays)


