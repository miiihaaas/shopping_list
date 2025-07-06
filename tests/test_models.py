import unittest
from app import create_app, db
from app.models.user import User
from app.models.workspace import Workspace
from app.models.shopping_item import ShoppingItem
from datetime import datetime, timedelta

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_model(self):
        # Test kreiranja korisnika
        user = User(username='test_user', email='test@example.com', password_hash='test_hash')
        db.session.add(user)
        db.session.commit()
        
        # Provera da li je korisnik uspešno kreiran
        user_from_db = User.query.filter_by(username='test_user').first()
        self.assertEqual(user_from_db.email, 'test@example.com')
        self.assertEqual(user_from_db.password_hash, 'test_hash')
        self.assertFalse(user_from_db.is_admin)
    
    def test_workspace_model(self):
        # Test kreiranja workspace-a
        workspace = Workspace(name='Test Workspace')
        db.session.add(workspace)
        db.session.commit()
        
        # Provera da li je workspace uspešno kreiran
        workspace_from_db = Workspace.query.filter_by(name='Test Workspace').first()
        self.assertIsNotNone(workspace_from_db)
        self.assertEqual(workspace_from_db.name, 'Test Workspace')
        self.assertIsNotNone(workspace_from_db.created_at)
    
    def test_shopping_item_model(self):
        # Kreiranje korisnika i workspace-a za test
        user = User(username='test_user', email='test@example.com', password_hash='test_hash')
        workspace = Workspace(name='Test Workspace')
        db.session.add(user)
        db.session.add(workspace)
        db.session.commit()
        
        # Test kreiranja stavke za kupovinu
        item = ShoppingItem(
            name='Test Item',
            workspace_id=workspace.id,
            added_by=user.id
        )
        db.session.add(item)
        db.session.commit()
        
        # Provera da li je stavka uspešno kreirana
        item_from_db = ShoppingItem.query.filter_by(name='Test Item').first()
        self.assertIsNotNone(item_from_db)
        self.assertEqual(item_from_db.name, 'Test Item')
        self.assertEqual(item_from_db.workspace_id, workspace.id)
        self.assertEqual(item_from_db.added_by, user.id)
        self.assertFalse(item_from_db.purchased)
        self.assertIsNotNone(item_from_db.created_at)

if __name__ == '__main__':
    unittest.main()
