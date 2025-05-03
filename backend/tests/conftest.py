import pytest
import secrets
import sys
import os

sys.path.append(os.getcwd())  # hack to load server.py

from server import app as flask_app


@pytest.fixture(scope="session")
def random_email():
    return f"cool{secrets.token_hex(8)}@illinois.edu"


@pytest.fixture()
def app():
    flask_app.testing = True

    return flask_app


@pytest.fixture()
def client(app):
    return flask_app.test_client()
