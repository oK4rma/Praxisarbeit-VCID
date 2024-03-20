from flask import Blueprint

# Erstellt ein Blueprint namens 'api'. Dies wird verwendet, um eine Gruppe von Routen zu organisieren.
bp = Blueprint("api", __name__)
# Importiert verschiedene Module (tokens, errors, vehicles, account, reservations) nach der Blueprint-Erstellung.
from app.api import tokens, errors, vehicles, accounting, reservations  # noqa: E402, F401
