from flask.testing import FlaskClient


def login(client: FlaskClient, random_email):
    r = client.post("/login", json={"email": random_email, "password": "abcdefg1234"})

    assert r.status_code == 200

    with client.session_transaction() as session:
        session["_user_id"] = r.json["id"]

    return client
