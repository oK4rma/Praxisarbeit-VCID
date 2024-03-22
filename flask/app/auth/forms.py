from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import User

# Definiert ein Anmeldeformular mit Benutzername und Passwort.
class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        # Validierung: Eingabe erforderlich
        validators=[DataRequired()],
        # Stildefinition
        render_kw={"class": "input input-bordered"},
    )

    password = PasswordField(
        "Password",
        # Validierung: Eingabe erforderlich
        validators=[DataRequired()],
        # Stildefinition
        render_kw={"class": "input input-bordered"},
    )

    submit = SubmitField(
        "Sign In",
        # Stildefinition für den Anmeldebutton
        render_kw={"class": "btn btn-primary"},
    )

# Definiert ein Registrierungsformular mit Benutzername, E-Mail und Passwort.
class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        # Validierung: Eingabe erforderlich
        validators=[DataRequired()],
        # Stildefinition
        render_kw={"class": "input input-bordered"},
    )

    email = StringField(
        "Email",
        # Validierung: Eingabe und gültige E-Mail erforderlich
        validators=[DataRequired(), Email()],
        # Stildefinition
        render_kw={"class": "input input-bordered"},
    )

    password = PasswordField(
        "Password",
        # Validierung: Eingabe erforderlich
        validators=[DataRequired()],
        # Stildefinition
        render_kw={"class": "input input-bordered"},
    )

    passwordRepeat = PasswordField(
        "Repeat Password",
        # Validierung: Eingabe erforderlich und muss mit dem Passwort übereinstimmen
        validators=[DataRequired(), EqualTo("password")],
        # Stildefinition
        render_kw={"class": "input input-bordered"},
    )

    submit = SubmitField(
        "Register",
        # Stildefinition
        render_kw={"class": "btn btn-primary"},
    )
    
    # Benutzerdefinierte Validierungsmethode für den Benutzernamen: Überprüft, ob der Benutzername bereits vergeben ist.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            # Fehler, wenn der Benutzername bereits vergeben ist.
            raise ValueError("Username already taken")
