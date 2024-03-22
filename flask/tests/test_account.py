import datetime
import pytest
from flask_login import FlaskLoginClient
from app import create_app, db
from app.models import User, rentalvehicle, Reservation
from tests.testconf import TestConfig

@pytest.fixture
def testApp():
    # Erstellt eine Anwendungskonfiguration speziell für Tests.
    app = create_app(TestConfig)
    app.test_client_class = FlaskLoginClient
    with app.app_context():
        db.create_all()
        # Initialisiert Standard-Fahrzeuge für die Tests.
        for x in range(1, 4):
            vehicle = rentalvehicle(id=x, price=1, info=f"vehicles {x}")
            db.session.add(vehicle)
        db.session.commit()

        # Erstellt einen Testbenutzer.
        u = User(username="toby")
        u.set_password("?!4-K4li-L1nux-4?!")
        db.session.add(u)
        db.session.commit()

        # Erstellt eine Reservierung für den Testbenutzer für heute.
        today = datetime.date.today()
        r = Reservation(user_id=u.id, rental_vehicle_id=1, date=today)
        db.session.add(r)
        db.session.commit()

        # Erstellt eine weitere Reservierung für morgen.
        tomorrow = today + datetime.timedelta(days=1)
        r2 = Reservation(user_id=u.id, rental_vehicle_id=2, date=tomorrow)
        db.session.add(r2)
        db.session.commit()

        # Nach Abschluss der Tests werden die Daten bereinigt.
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(testApp):
    # Ermöglicht Tests mit einem authentifizierten Benutzer.
    user = User.query.filter_by(username="toby").first()
    return testApp.test_client(user=user)

@pytest.fixture
def token(client):
    # Holt einen Authentifizierungstoken für den Testbenutzer.
    credentials = ("toby", "?!4-K4li-L1nux-4?!")
    tokenResponse = client.post("api/tokens", auth=credentials)
    token = tokenResponse.json["token"]
    return token

class Testaccount:
    @pytest.mark.dependency()
    def test_token_get(self, token):
        # Überprüft, ob ein Token erfolgreich abgerufen wurde.
        assert token is not None

    @pytest.mark.dependency(depends=["Testaccount::test_token_get"])
    def test_accountint_calc(self, client, token):
        # Testet, ob Account-Informationen korrekt abgerufen werden können.
        with client:
            response = client.get("/api/account", headers={"Authorization": f"Bearer {token}"})
            assert response.status_code == 200

            data = response.json
            assert data["vehicles"] == 3
            assert data["occupied"] == 1
            assert data["occupation"] == 0.33
            assert data["revenue"] == 1
