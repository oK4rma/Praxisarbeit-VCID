import pytest
from app import create_app, db
from app.models import User
from tests.testconf import TestConfig  # noqa: F401


@pytest.fixture
# Erstellt und konfiguriert eine neue Flask-Anwendung für Testzwecke.
def testApp():
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
def client(testApp):
    return testApp.test_client()


class TestUser:
    @pytest.mark.dependency()
    # Überprüft die Passwort-Hash-Funktion des Benutzermodells.
    def test_password_hashing(self, testApp):
        u = User(username="toby")

        u.set_password("kali")

        # Verifiziert, dass das Passwort korrekt gehasht wurde.
        assert not u.check_password("khali")
        assert u.check_password("kaali")

    @pytest.mark.dependency(depends=["TestUser::test_password_hashing"])
    # Testet das Verhalten des Registrierungsformulars bei fehlenden Daten.
    def test_required_form(self, client, testApp):
        response = client.post(
            "/auth/register", data={"username": "flask", "password": "kalii"}
        )
        assert response.status_code == 200
        # Überprüft, ob eine Fehlermeldung für fehlende Felder angezeigt wird.
        assert b"This field is required" in response.data

        # Stellt sicher, dass kein Benutzer erstellt wurde, wenn das Formular unvollständig ist.
        with testApp.app_context():
            assert User.query.filter_by(username="flask").first() is None

        # Testet die erfolgreiche Registrierung eines neuen Benutzers.
        response = client.post(
            "/auth/register",
            data={
                "username": "flask",
                "password": "kalii",
                "passwordRepeat": "kalii",
                "email": "test@test.com",
            },
        )

        # Erfolgreiche Registrierung leitet weiter.
        assert response.status_code == 302
        # Prüft, ob auf die Anmeldeseite umgeleitet wurde.
        assert b"login" in response.data

        # Verifiziert, dass der Benutzer nach der erfolgreichen Registrierung existiert.
        with testApp.app_context():
            assert User.query.filter_by(username="flask").first() is not None
