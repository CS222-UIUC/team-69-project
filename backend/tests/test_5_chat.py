import pytest
from flask.testing import FlaskClient
import secrets
from helper import login


@pytest.mark.dependency(
    depends=["test_match_user_expect_pass"],
    scope="session",
)
def test_get_chats_expect_pass(random_email, client: FlaskClient):
    client = login(client, random_email)

    r = client.get(
        "/chat/chats",
    )

    assert r.status_code == 200
    assert len(r.json) > 0
