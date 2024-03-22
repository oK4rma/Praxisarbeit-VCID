from app import create_app

# Erstellt eine Flask-Anwendung mit Standardkonfiguration.
app = create_app()
# Registriert benutzerdefinierte CLI-Befehle bei der Anwendung
cli.register(app)
