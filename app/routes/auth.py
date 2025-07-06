from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User, db
from app.forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Ako je korisnik već prijavljen, redirektujemo ga na početnu stranicu
    if current_user.is_authenticated:
        return redirect(url_for('shopping.list'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user is None or not check_password_hash(user.password_hash, form.password.data):
            flash('Neispravna email adresa ili lozinka.', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        # Redirekt na stranicu koju je korisnik prvobitno pokušao da pristupi
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('shopping.list')
            
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Prijava', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Uspešno ste se odjavili.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Ako je korisnik već prijavljen, redirektujemo ga na početnu stranicu
    if current_user.is_authenticated:
        return redirect(url_for('shopping.list'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Uspešno ste se registrovali. Možete se prijaviti.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Registracija', form=form)
