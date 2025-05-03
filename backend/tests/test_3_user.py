import pytest
from flask.testing import FlaskClient
import secrets
from helper import login


@pytest.mark.dependency(
    depends=["test_signup_expect_pass", "test_login_expect_pass"],
    scope="session",
    name="test_modify_user_expect_pass",
)
def test_modify_user_expect_pass(random_email, client: FlaskClient):
    client = login(client, random_email)

    r = client.patch(
        "/user",
        json={
            "display_name": "my_cool_username" + secrets.token_hex(8),
            "major": "Computer Science",
            "year": "Sophomore",
            "classes_can_tutor": ["CS 225"],
            "classes_needed": ["CHEM 332"],
        },
    )

    assert r.status_code == 200


@pytest.mark.dependency(
    depends=["test_signup_expect_pass", "test_login_expect_pass"], scope="session"
)
def test_get_self(random_email, client: FlaskClient):
    client = login(client, random_email)

    r = client.get(
        "/user/@me",
    )

    assert r.status_code == 200
    assert "display_name" in r.json


@pytest.mark.dependency(
    depends=["test_signup_expect_pass", "test_login_expect_pass"], scope="session"
)
def test_search(random_email, client: FlaskClient):
    client = login(client, random_email)

    r = client.get(
        f"/search?name=my_cool_username",
    )

    assert r.status_code == 200
    assert len(r.json) > 0
