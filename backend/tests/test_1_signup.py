import requests
import secrets
import pytest
from flask.testing import FlaskClient


@pytest.mark.dependency(name="test_signup_expect_pass", scope="session")
@pytest.mark.order(1)
def test_signup_expect_pass(random_email, client: FlaskClient):
    r = client.post(
        "/signup",
        json={
            "display_name": "my_cool_username"
            + secrets.token_hex(8),  # prevents duplicates
            "email": random_email,
            "password": "abcdefg1234",
        },
    )
    assert r.status_code == 200

    response_json = r.json

    assert "password" not in response_json
    assert random_email in response_json["email"]


@pytest.mark.order(2)
def test_signup_expect_fail(client: FlaskClient):
    try:
        r = client.post(
            "/signup",
            json={"display_name": "my_cooler_username2", "password": "abcdefg1234"},
        )
        assert r.status_code != 200
    except Exception:
        assert True
