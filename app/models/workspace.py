from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

class Workspace(db.Model):
    __tablename__ = 'workspaces'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship('User', back_populates='workspace')
    shopping_items = db.relationship('ShoppingItem', back_populates='workspace')

    def __repr__(self):
        return f'<Workspace {self.name}>'
