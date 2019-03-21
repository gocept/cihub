from sqlalchemy import create_engine
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from starlette.config import Config
import databases
import enum
import sqlalchemy


# Configuration from environment variables or '.env' file.
config = Config('.env')
DATABASE_URL = config('DATABASE_URL')


class StatusEnum(enum.Enum):
    # Status defined for cc.xml:
    Success = 'Success'
    Failure = 'Failure'
    Exception = 'Exception'
    Unknown = 'Unknown'

    # Jenkins status mapping
    SUCCESS = 'Success'
    UNSTABLE = 'Failure'
    FAILURE = 'Exception'
    ABORTED = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return StatusEnum.Unknown


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


database = databases.Database(DATABASE_URL)


def initialize_database():
    url = DATABASE_URL
    engine = create_engine(url)
    assert not database_exists(url)
    create_database(url)
    metadata.create_all(engine)
