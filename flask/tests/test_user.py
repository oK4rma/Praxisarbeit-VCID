import pytest

from app import create_app, db
from app.models import User
from tests.testconf import TestConfig  # noqa: F401


@pytest.fixture
def testApp():
    # Start setup, create new app and database
    app = create_app(TestConfig)
    with app.app_context():
        # Create all tables
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(testApp):
    return testApp.test_client()


class TestUser:
    @pytest.mark.dependency()
    def test_password_hashing(self, testApp):
        u = User(username="toby")

        u.set_password("kali")

        assert not u.check_password("khali")
        assert u.check_password("kaali")

    @pytest.mark.dependency(depends=["TestUser::test_password_hashing"])
    def test_required_form(self, client, testApp):
        response = client.post(
            "/auth/register", data={"username": "flask", "password": "kalii"}
        )
        assert response.status_code == 200
        assert b"This field is required" in response.data

        with testApp.app_context():
            assert User.query.filter_by(username="flask").first() is None

        response = client.post(
            "/auth/register",
            data={
                "username": "flask",
                "password": "kalii",
                "passwordRepeat": "kalii",
                "email": "test@test.com",
            },
        )

        assert response.status_code == 302
        assert b"login" in response.data

        with testApp.app_context():
            assert User.query.filter_by(username="flask").first() is not None
