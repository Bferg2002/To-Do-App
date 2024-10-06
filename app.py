from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)

# Database configuration using SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db = SQLAlchemy(app)

# Define a model for To-Do items
class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """
        Return a string representation of the To-Do item.

        :return: A string that includes the task name.
        """
        return f"<Task {self.task}>"

# Route for the homepage to display the to-do list
@app.route('/')
def index():
    """
    Homepage route to display the to-do list.

    Fetches all tasks from the database and passes them to the
    'index.html' template for rendering.

    :return: The rendered HTML template.
    """
    tasks = TodoItem.query.all()  # Fetch all tasks from the database
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    """
    Adds a new task to the database from the form data and redirects
    back to the homepage.

    The new task is added to the database and the homepage is refreshed
    to display the new task.
    """
    task_content = request.form['task']
    new_task = TodoItem(task=task_content)

    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete/<int:id>')
def delete_task(id):
    """
    Deletes a task from the database and redirects back to the homepage.

    Args:
        id (int): The ID of the task to be deleted
    """
    task = TodoItem.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('index'))

# Route to mark a task as complete
@app.route('/complete/<int:id>')
def complete_task(id):
    """Toggle a task as complete or incomplete
    
    :param int id: The ID of the task to toggle
    """
    task = TodoItem.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
