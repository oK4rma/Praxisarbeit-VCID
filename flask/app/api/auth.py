from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.api.errors import error_response
from app.models import User

# Erstellt eine Instanz für die Basis-Authentifizierung.
basic_auth = HTTPBasicAuth()
# Erstellt eine Instanz für die Token-Authentifizierung.
token_auth = HTTPTokenAuth()

# Dekorator, der eine Funktion zur Überprüfung von Benutzername und Passwort definiert.
@basic_auth.verify_password
def verify_password(username, password):
    # Sucht den Benutzer anhand des Benutzernamens.
    user = User.query.filter_by(username=username).first()
    # Überprüft das Passwort, wenn der Benutzer existiert.
    if user and user.check_password(password):
        # Gibt den Benutzer zurück, wenn das Passwort korrekt ist.
        return user

# Dekorator, der eine Funktion zur Überprüfung von Tokens definiert.
@token_auth.verify_token
def verify_token(token):
    # Überprüft das Token und gibt den Benutzer zurück, wenn das Token gültig ist.
    return User.check_token(token) if token else None

# Dekorator, der eine Funktion zur Fehlerbehandlung für Basis-Authentifizierung definiert.
@basic_auth.error_handler
def basic_auth_error(status):
    # Gibt eine Fehlerantwort zurück.
    return error_response(status)

# Dekorator, der eine Funktion zur Fehlerbehandlung für Token-Authentifizierung definiert.
@token_auth.error_handler
def token_auth_error(status):
    # Gibt eine Fehlerantwort zurück.
    return error_response(status)
