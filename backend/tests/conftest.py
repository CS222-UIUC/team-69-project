import pytest
import secrets

@pytest.fixture(scope="session")
def random_email():
    return  f"cool{secrets.token_hex(8)}@illinois.edu"