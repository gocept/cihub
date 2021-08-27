from _cihub.config import config
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
import databases
import datetime
import enum
import pytz
import sqlalchemy


DATABASE_URL = config('DATABASE_URL', cast=databases.DatabaseURL)
TESTING = config('TESTING', cast=bool, default=False)
TEST_DATABASE_URL = DATABASE_URL.replace(
    database='test_' + DATABASE_URL.database)

if TESTING:
    database = databases.Database(TEST_DATABASE_URL)
else:
    database = databases.Database(DATABASE_URL)


class StatusEnum(enum.Enum):
    """Enum mapping status texts to internal representations."""

    # Status defined for cc.xml:
    Success = 'Success'
    Failure = 'Failure'
    Exception = 'Exception'
    Unknown = 'Unknown'

    # Jenkins status mapping
    SUCCESS = 'Success'
    UNSTABLE = 'Failure'
    FAILURE = 'Failure'
    ABORTED = 'Unknown'

    # Bitbucket Pipelines status mapping
    SUCCESSFUL = 'Success'
    FAILED = 'Failure'
    INPROGRESS = 'Unknown'
    STOPPED = 'Unknown'

    # TravisCI status mapping
    Pending = 'Unknown'
    Passed = 'Success'
    Fixed = 'Success'
    Broken = 'Failure'
    Failed = 'Failure'
    StillFailing = 'Failure'
    Canceled = 'Unknown'
    Errored = 'Failure'

    # Github actions status mapping
    success = 'Success'
    failure = 'Failure'
    neutral = 'Unknown'
    cancelled = 'Failure'
    timed_out = 'Failure'
    action_required = 'Unknown'

    # GitLab CI status mapping
    # success = 'Success'  # Same as in Github
    canceled = 'Unknown'
    failed = 'Failure'


# Database table definitions.
metadata = sqlalchemy.MetaData()

ci_status = sqlalchemy.Table(
    "ci_status",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("url", sqlalchemy.String),
    sqlalchemy.Column("buildnumber", sqlalchemy.Integer),
    sqlalchemy.Column("status", sqlalchemy.Enum(StatusEnum)),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime(timezone=True)),
)


def initialize_database():
    url = str(DATABASE_URL)
    engine = create_engine(url)
    assert not database_exists(url)
    create_database(url)
    metadata.create_all(engine)


def _get_db_engine():
    """Get an engine object for the currently defined database."""
    if TESTING:
        url = TEST_DATABASE_URL
    else:
        url = DATABASE_URL
    url = str(url)
    assert database_exists(url)
    return create_engine(url)


def install_example_data():
    EXAMPLE_DATA = [{
        'id': 'dgb.internet',
        'url': 'https://jenkins.verdi4you.de/job/dgb.internet/3433/',
        'buildnumber': 3433,
        'status': StatusEnum.Success,
        'timestamp': datetime.datetime.now(pytz.UTC),
    }, {
        'id': 'dgb.content',
        'url': 'https://jenkins.verdi4you.de/job/dgb.content/1234/',
        'buildnumber': 1234,
        'status': StatusEnum.Failure,
        'timestamp': datetime.datetime.now(pytz.UTC),
    }, {
        'id': 'uc.https',
        'url': 'https://jenkins.verdi4you.de/job/uc.https/321/',
        'buildnumber': 321,
        'status': StatusEnum.Unknown,
        'timestamp': datetime.datetime.now(pytz.UTC) - datetime.timedelta(20),
    }]
    engine = _get_db_engine()
    for data in EXAMPLE_DATA:
        query = ci_status.insert().values(**data)
        engine.execute(query)


def wipe_older_than(days):
    """Wipe entries which are older than the given number of days.

    Returns the number of deleted entries.
    """
    assert days > 0
    engine = _get_db_engine()

    borderline = (pytz.UTC.localize(datetime.datetime.now())
                  - datetime.timedelta(days=days))
    query = ci_status.delete().where(ci_status.c.timestamp < borderline)
    return engine.execute(query).rowcount
