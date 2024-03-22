from flask import Blueprint

# Erstellt ein Blueprint namens 'auth' für die Authentifizierungs-Features der Anwendung. 
bp = Blueprint("auth", __name__)
# Importiert verschiedene Module (routes) nach der Blueprint-Erstellung.
from app.auth import routes  # noqa: E402, F401
