from flask_sqlalchemy import SQLAlchemy
from src.authentication_app import User, db

class CommunicationModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #qk
    quantum_key = db.Column(db.String(500))
    send_user = db.Column(db.Integer, db.ForeignKey('User.id'))
    message = db.Column(db.String(1000))
    receive_user = db.Column(db.Integer, db.ForeignKey('User.id'))
    