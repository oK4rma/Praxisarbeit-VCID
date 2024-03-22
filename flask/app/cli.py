from flask_apidoc.commands import GenerateApiDoc

def register(app):
    @app.cli.group()
     # Definiert eine neue Befehlsgruppe 'docs' im Flask CLI.
    def docs():
        """API documentation commands."""
        # Dient als Platzhalter, da 'docs' als Gruppe für Unterbefehle fungiert.
        pass

    @docs.command()
     # Definiert den 'generate'-Befehl innerhalb der 'docs'-Gruppe.
    def generate():
        """Compile apidoc"""
        # Ruft die Funktion zur Generierung der API-Dokumentation auf, speichert die Ergebnisse im angegebenen Verzeichnis.
        GenerateApiDoc("./app", "app/static/docs").run()
