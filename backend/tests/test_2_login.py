import pytest
from flask.testing import FlaskClient


@pytest.mark.order(3)
@pytest.mark.dependency(
    depends=["test_signup_expect_pass"], scope="session", name="test_login_expect_pass"
)
def test_login_expect_pass(random_email, client: FlaskClient):
    r = client.post("/login", json={"email": random_email, "password": "abcdefg1234"})

    assert r.status_code == 200

    with client.session_transaction() as session:
        session["_user_id"] = r.json["id"]
