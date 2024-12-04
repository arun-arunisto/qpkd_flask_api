from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from .login_mgr import login_manager

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(500))

    def __init__(self, name, email, password):
        self.public_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)


#this decorator will help us to monitor the user logged in or not
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)