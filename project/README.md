# Recipe Finder

## Video Demonstration

You can watch a demonstration of the Recipe Finder application in action here: [Recipe Finder Demo](https://youtu.be/Bobz0Gv-i18)

# Recipe Finder

## Overview

Recipe Finder is a dynamic and user-friendly web application designed to help users discover, organize, and store their favorite recipes. In today's fast-paced world, meal planning can be a daunting task, especially when ingredients are limited. This application seeks to solve that problem by allowing users to search for recipes based on the ingredients they already have at home, save them for future use, and track their interactions with these recipes. The integration of the Spoonacular API ensures that users can access a broad array of recipes tailored to their input, while the intuitive design allows for a seamless and enjoyable experience.

Built using Flask for the backend, SQLite for the database, and HTML/CSS for the frontend, Recipe Finder is a lightweight yet powerful solution for home cooks, food enthusiasts, and anyone looking to streamline their meal planning process. By providing an organized space to store and view recipes, along with a detailed usage history, this application makes managing meal ideas and exploring new dishes both fun and efficient.

## Features

### User Registration & Login

Recipe Finder offers a secure user registration and login system. Users can create accounts with unique usernames and passwords, ensuring that their recipe collection is private and personalized. The login system also utilizes Flask sessions to keep track of active users and maintain their data securely throughout their session.

### Recipe Search

The application features a robust recipe search functionality powered by the Spoonacular API. Users can search for recipes based on specific ingredients they have at home, and the system will return a list of recipes that can be made using those ingredients. This is a key feature designed to help users make the most out of the ingredients they already have, preventing food waste and inspiring creativity in meal preparation.

### Save Recipes

Once users find recipes they like, they can save them directly to their account. Each saved recipe is stored with a link to the recipe, the recipe’s name, and the time the user saved it. This allows users to easily revisit their favorite recipes whenever they like.

### View Saved Recipes

The "Account" page allows users to view all the recipes they have saved over time. Recipes are displayed in an organized manner, and users can quickly access the recipe details through the saved link. This feature makes it simple for users to track and organize their recipe collection.

### Recipe Usage History

A key feature of Recipe Finder is the ability to track when users interact with saved recipes. Every time a user views, adds, or deletes a recipe, the action is logged in their usage history. This provides users with insight into their cooking habits and helps them revisit recipes they may have forgotten.

### Delete Recipes

Users have full control over their saved recipe collection. If a user no longer wants a particular recipe, they can delete it from their account. This feature ensures that the user's recipe collection remains relevant and up-to-date, free from outdated or unwanted recipes.

## Tech Stack

### Frontend

- **HTML**: Used for structuring the content of the web pages.
- **CSS**: Responsible for styling the web pages to ensure a responsive, user-friendly interface. The application is designed to be mobile-friendly and visually appealing.

### Backend

- **Python (Flask)**: The core of the application is built using Flask, a micro web framework in Python. Flask's simplicity and flexibility made it an ideal choice for this project, as it allows for easy routing, templating, and session management.
- **SQLite**: SQLite is used as the database for storing user information, saved recipes, and recipe usage history. It is lightweight and serverless, which makes it ideal for smaller applications like this one.

### External API

- **Spoonacular API**: The Spoonacular API is integrated into the application to provide a comprehensive recipe search function. It allows the application to fetch recipes based on ingredients that users input, ensuring that the recipe suggestions are relevant and personalized.

### Session Management

- **Flask Sessions**: Flask's session management system is used for user authentication. This ensures that once a user logs in, their session persists across pages, allowing them to save recipes and track their history without having to log in repeatedly.

## Setup Instructions

### Prerequisites

To get started with Recipe Finder, you need to have the following software installed on your machine:

- **Python 3.x**: This project is developed using Python 3, and you'll need it to run the application.
- **pip**: Python's package installer is required to install dependencies.

If you don’t have Python installed, you can download it from [python.org](https://www.python.org/).

### File Structure

/recipe_finder
  /static
    /stylesHome.css                # Contains the styling for the frontend
  /templates
    account.html               # Displays saved recipes and usage history
    recipe_search.html         # Provides the recipe search interface
    login.html                 # Login page template
    register.html              # User registration page template
  app.py                       # Main application file, contains routing and logic
  setup_db.py                  # Initializes the database
  requirements.txt             # Python dependencies for the application

### Explanation of Files

- **app.py**: The core of the Flask web application. It handles routing, user authentication, recipe searching, and interactions with the SQLite database. It also manages user sessions for login and logout functionality.
- **setup_db.py**: A script used to initialize the database by creating the necessary tables if they don’t already exist.
- **templates/**: Contains all the HTML templates used by the Flask application. Each template corresponds to a different page on the website, such as the account page, recipe search page, login page, and
registration page.
- **static/styles.css**: This file contains the CSS styling for the web application, ensuring a pleasant and responsive user experience.

## Design Choices

### Why Flask?
Flask was selected for this project because of its simplicity and flexibility. Flask is a micro-framework, which means it is lightweight and modular, allowing us to add only the components we need. It also has great support for templating, routing, and managing user sessions, which were essential for the functionality of this application.

### Why SQLite?
SQLite was chosen as the database for this application due to its ease of use and minimal setup requirements. SQLite is serverless, meaning it stores data in a local file, which makes it easy to deploy and manage. It is also well-suited for small to medium-sized applications, making it ideal for this project.

### Why Spoonacular API?
The Spoonacular API was chosen for its extensive recipe database and flexibility. It provides an easy-to-use endpoint for searching recipes based on ingredients, which is the core functionality of this application. The API also provides detailed recipe information, such as cooking instructions, serving sizes, and nutritional data, enhancing the user experience.

### Session Management
Flask sessions were used for user authentication, which ensures that users are recognized and their recipe collections and history are associated with their unique accounts. Sessions allow for persistent login states, eliminating the need for users to log in every time they interact with the application.


### Installing Dependencies

Once you have Python and pip installed, you can install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```
### Database Setup
Recipe Finder uses SQLite for data storage. To set up the database, run the following command to initialize the required tables:

```bash
python setup_db.py
```
### Running the Application
To run the application locally, use the following command:
```bash
flask run
```
### or

```bash
python app.py
```





