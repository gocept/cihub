from _cihub.db import ci_status
from _cihub.db import wipe_older_than
from datetime import datetime
from datetime import timedelta
from sqlalchemy.sql import select
import pytz


def test_db__wipe_older_than__1(database):
    """It removes older entries and returns the number of deletes ones."""
    now = pytz.UTC.localize(datetime.now())
    for title, age in (('oldest', 14), ('older', 7), ('old', 3), ('now', 0)):
        ins = ci_status.insert().values(
            id=title, timestamp=now - timedelta(days=age))
        ins.bind = database
        ins.execute()

    query = select([ci_status.c.id])
    res = database.execute(query).fetchall()
    assert len(res) == 4

    assert wipe_older_than(2) == 3

    res = database.execute(query).fetchall()
    assert res == [('now',)]
