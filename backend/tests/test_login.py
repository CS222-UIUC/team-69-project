import requests
import secrets
import pytest

BASE_URL = "http://127.0.0.1:5000"

@pytest.mark.order(3)
@pytest.mark.dependency(depends=['test_signup_expect_pass'], scope="session")
def test_login_expect_pass(random_email):
    r = requests.post(f"{BASE_URL}/login", json={
        "email": random_email,
        "password": "abcdefg1234"
    })
    print(r.text)

    assert r.status_code == 200