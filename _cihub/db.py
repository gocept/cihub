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
    url = DATABASE_URL
    engine = create_engine(url)
    assert not database_exists(url)
    create_database(url)
    metadata.create_all(engine)


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
    url = DATABASE_URL
    assert database_exists(url)
    engine = create_engine(url)
    for data in EXAMPLE_DATA:
        query = ci_status.insert().values(**data)
        engine.execute(query)
