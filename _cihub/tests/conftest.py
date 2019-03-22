import pytest
from starlette.config import environ
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

# This sets `os.environ`, but provides some additional protection.
# If we placed it below the application import, it would raise an error
# informing us that 'TESTING' had already been read from the environment.
environ['TESTING'] = 'True'
environ['username'] = 'testuser'
environ['password'] = 'testword'

from _cihub.cihub import app  # noqa: E401
from _cihub.config import config  # noqa: E401
from _cihub.db import TEST_DATABASE_URL  # noqa: E401
from _cihub.db import metadata  # noqa: E401


@pytest.fixture(scope="function")
def database():
    """
    Create a clean database on every test case.

    For safety, we should abort if a database already exists.

    We use the `sqlalchemy_utils` package here for a few helpers in
    consistently creating and dropping the database.
    """
    url = str(TEST_DATABASE_URL)
    engine = create_engine(url)
    assert not database_exists(url), \
        'Test database already exists. Aborting tests.'
    create_database(url)
    metadata.create_all(engine)
    yield engine
    drop_database(url)

@pytest.fixture()
def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:
    """
    with TestClient(app) as client:
        yield client
