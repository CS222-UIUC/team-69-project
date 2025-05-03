import pytest
from flask.testing import FlaskClient
import secrets
from helper import login


@pytest.mark.dependency(
    depends=["test_modify_user_expect_pass"],
    scope="session",
    name="test_match_user_expect_pass",
)
def test_match_user_expect_pass(random_email, client: FlaskClient):
    client = login(client, random_email)

    r = client.post(
        "/match/new_user",
    )

    assert r.status_code == 200


@pytest.mark.dependency(
    depends=["test_match_user_expect_pass"],
    scope="session",
)
def test_get_matches_expect_pass(random_email, client: FlaskClient):
    client = login(client, random_email)

    r = client.get(
        "/match/matches",
    )

    assert r.status_code == 200
    assert len(r.json) > 0
