import pytest
from app import create_app, db
from config import Config

# Konfigurationsklasse für Testumgebungen, erbt von der Basiskonfiguration.
class TestConfig(Config):
    # Aktiviert den Testmodus.
    TESTING = True
    # Nutzt eine In-Memory SQLite-Datenbank für Tests.
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    # Deaktiviert CSRF-Schutz in Formularen für Tests.
    WTF_CSRF_ENABLED = False


@pytest.fixture
# Erstellt eine Flask-Anwendung für Testzwecke mit der Testkonfiguration.
def fixture():
    app = create_app(TestConfig)
    with app.app_context():
        # Erstellt alle Datenbanktabellen.
        db.create_all()
        # Macht die App für Tests verfügbar.
        yield app
        # Bereinigt die Session nach dem Test.
        db.session.remove()
        # Löscht alle Datenbanktabellen.
        db.drop_all()


@pytest.fixture
# Stellt einen Test-Client für die Flask-Anwendung bereit.
def client(app):
    return app.test_client()
