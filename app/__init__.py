from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

# Inicijalizacija ekstenzija
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    # Učitavanje env varijabli
    load_dotenv()
    
    app = Flask(__name__)
    
    # Konfiguracija aplikacije
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicijalizacija ekstenzija
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Konfiguracija login managera
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Prijavite se da biste pristupili ovoj stranici.'
    login_manager.login_message_category = 'info'
    
    # Konfiguracija login managera za user loader
    @login_manager.user_loader
    def load_user(id):
        # Odloženi import da izbegneš cirkularni import
        from app.models.user import User
        return User.query.get(int(id))
    
    # Registrovanje blueprinta
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.shopping import shopping_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(shopping_bp)
    
    # Kreiranje baze podataka ako ne postoji
    with app.app_context():
        db.create_all()
        
        # Odloženi import za admin kreiranje
        from app.models.user import User
        from werkzeug.security import generate_password_hash
        
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            admin = User(
                username='admin',
                email='miiihaaas@gmail.com',
                password_hash=generate_password_hash('admin'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print('Admin korisnik kreiran!')
    
    return app