from flask import Blueprint

# Erstellt ein Blueprint namens 'errors' für die Fehlerbehandlung in der Anwendung.
bp = Blueprint("errors", __name__)
# Importiert verschiedene Module (handlers) nach der Blueprint-Erstellung.
from app.errors import handlers  # noqa: E402, F401
