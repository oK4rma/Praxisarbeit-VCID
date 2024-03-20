from flask import Blueprint

# Erstellt ein Blueprint namens 'rental' für die Verwaltung von Mietvorgängen in der Anwendung. 
bp = Blueprint("rental", __name__)
# Importiert verschiedene Module (routes) nach der Blueprint-Erstellung.
from app.rental import routes  # noqa: E402, F401
