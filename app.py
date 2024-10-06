from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, TodoItem  # Import models here

# Create the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Flask-Login user loader callback function
@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user by their user_id.

    Args:
        user_id (int): The ID of the user to load.

    :return: The user object, or None if not found.
    """
    return User.query.get(int(user_id))


# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route for user registration. Handles POST requests to register new users
    by saving their username and hashed password.

    If the user already exists, a flash message is shown, and the user is
    redirected back to the registration page.
    
    :return: Redirect to login if registration is successful, or render registration page.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another one.')
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login. Handles POST requests to log in users by verifying their
    username and password.

    If the login is successful, the user is redirected to the index page, otherwise,
    an error message is shown.
    
    :return: Redirect to index if login is successful, or render login page.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')


# Route for user logout
@app.route('/logout')
@login_required  # Users must be logged in to log out
def logout():
    """
    Route for user logout. Logs out the current user and redirects them to the login page.
    
    :return: Redirect to login page after logging out.
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))


# Route for the homepage to display the to-do list
@app.route('/')
@login_required
def index():
    """
    Homepage route to display the to-do list for the logged-in user.

    Fetches tasks for the current user from the database and passes them to the
    'index.html' template for rendering.

    :return: The rendered HTML template with the list of tasks.
    """
    tasks = TodoItem.query.filter_by(user_id=current_user.id).all()  # Fetch tasks for the logged-in user
    return render_template('index.html', tasks=tasks)


# Route to add a new task
@app.route('/add', methods=['POST'])
@login_required
def add_task():
    """
    Adds a new task to the database from the form data and redirects
    back to the homepage.

    The new task is added to the database and the homepage is refreshed
    to display the new task.

    :return: Redirect to the index page.
    """
    task_content = request.form['task']
    new_task = TodoItem(task=task_content, user_id=current_user.id)  # Associate task with the current user

    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))


# Route to delete a task
@app.route('/delete/<int:id>')
@login_required
def delete_task(id):
    """
    Deletes a task from the database and redirects back to the homepage.

    Args:
        id (int): The ID of the task to be deleted.

    :return: Redirect to the index page.
    """
    task = TodoItem.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('index'))


# Route to mark a task as complete or incomplete
@app.route('/complete/<int:id>')
@login_required
def complete_task(id):
    """
    Toggles a task as complete or incomplete and redirects back to the homepage.

    Args:
        id (int): The ID of the task to toggle.

    :return: Redirect to the index page.
    """
    task = TodoItem.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()

    return redirect(url_for('index'))


# Main entry point for running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
