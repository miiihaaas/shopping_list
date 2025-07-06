from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Lozinka', validators=[DataRequired()])
    remember_me = BooleanField('Zapamti me')
    submit = SubmitField('Prijavi se')

class RegistrationForm(FlaskForm):
    username = StringField('Korisničko ime', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Lozinka', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Ponovite lozinku', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registruj se')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Korisničko ime je već zauzeto, izaberite drugo.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Ova email adresa je već registrovana.')

class WorkspaceForm(FlaskForm):
    name = StringField('Naziv workspace-a', validators=[DataRequired(), Length(min=2, max=64)])
    submit = SubmitField('Sačuvaj')

class ShoppingItemForm(FlaskForm):
    name = StringField('Naziv stavke', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Dodaj')

class UserWorkspaceForm(FlaskForm):
    user_id = SelectField('Korisnik', coerce=int, validators=[DataRequired()])
    workspace_id = SelectField('Workspace', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Dodeli workspace')
