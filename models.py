from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    A model representing a User in the application.

    Attributes:
        id (int): The primary key of the user.
        username (str): The username of the user.
        password (str): The hashed password of the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

class TodoItem(db.Model):
    """
    A model representing a To-Do item. Each item is associated with a user, has a task, and a completion status.

    Attributes:
        id (int): The primary key of the to-do item.
        task (str): The task description.
        completed (bool): Whether the task is completed or not.
        user_id (int): The foreign key referencing the user that owns the task.
    """
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Task {self.task}>"
