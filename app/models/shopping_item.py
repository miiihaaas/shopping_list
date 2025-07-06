from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

class ShoppingItem(db.Model):
    __tablename__ = 'shopping_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    purchased = db.Column(db.Boolean, default=False)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspaces.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    added_by_user = db.relationship('User', back_populates='shopping_items')
    workspace = db.relationship('Workspace', back_populates='shopping_items')

    def __repr__(self):
        return f'<ShoppingItem {self.name}>'
