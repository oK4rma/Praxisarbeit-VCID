import datetime
import pytest
from flask_login import FlaskLoginClient

from app import create_app, db
from app.models import User, rentalvehicle, Reservation
from tests.testconf import TestConfig


@pytest.fixture
def testApp():
    app = create_app(TestConfig)
    app.test_client_class = FlaskLoginClient
    with app.app_context():
        db.create_all()
        # Create default rental vehicles
        for x in range(1, 4):
            vehicle = rentalvehicle(id=x, price=1, info=f"vehicles {x}")
            db.session.add(vehicle)
        db.session.commit()

        u = User(username="toby")  # type: ignore
        u.set_password("kali")
        db.session.add(u)
        db.session.commit()

        today = datetime.date.today()
        r = Reservation(user_id=u.id, rental_vehicle_id=1, date=today)
        db.session.add(r)
        db.session.commit()

        tomorrow = today + datetime.timedelta(days=1)
        r2 = Reservation(user_id=u.id, rental_vehicle_id=2, date=tomorrow)
        db.session.add(r2)
        db.session.commit()

        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(testApp):
    user = User.query.filter_by(username="toby").first()
    return testApp.test_client(user=user)


@pytest.fixture
def token(client):
    credentials = ("toby", "kali")
    tokenResponse = client.post(
        "api/tokens",
        auth=credentials,
    )
    token = tokenResponse.json["token"]
    return token


class TestAccounting:
    @pytest.mark.dependency()
    def test_token_get(self, token):  # noqa: F811
        assert token is not None

    @pytest.mark.dependency(depends=["TestAccounting::test_token_get"])
    def test_accountint_calc(self, client, token):  # noqa: F811
        with client:
            response = client.get(
                "/api/accounting", headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200

            data = response.json
            assert data["vehicles"] == 3
            assert data["occupied"] == 1
            assert data["occupation"] == 0.33
            assert data["revenue"] == 1
