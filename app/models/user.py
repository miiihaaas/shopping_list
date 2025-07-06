# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from datetime import datetime

# db = SQLAlchemy()

# class User(db.Model, UserMixin):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128))
#     is_admin = db.Column(db.Boolean, default=False)
#     workspace_id = db.Column(db.Integer, db.ForeignKey('workspaces.id'))
#     workspace = db.relationship('Workspace', back_populates='users')
#     shopping_items = db.relationship('ShoppingItem', back_populates='added_by_user')

#     def __repr__(self):
#         return f'<User {self.username}>'

from flask_login import UserMixin
from datetime import datetime
from app import db  # Importuj db iz app/__init__.py

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspaces.id'))
    workspace = db.relationship('Workspace', back_populates='users')
    shopping_items = db.relationship('ShoppingItem', back_populates='added_by_user')

    def __repr__(self):
        return f'<User {self.username}>'