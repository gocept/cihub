from _cihub.db import ci_status
from _cihub.db import StatusEnum
from requests.auth import HTTPBasicAuth
from sqlalchemy.sql import select

jenkins_success_data = {
    'build':
    {'artifacts': {},
     'full_url': 'https://test.url/job/test_name/2342/',
     'log': '',
     'notes': '',
     'number': 2342,
     'phase': 'COMPLETED',
     'queue_id': 46612,
     'scm': {'changes': [], 'culprits': []},
     'status': 'SUCCESS',
     'timestamp': 1553175595208,
     'url': 'job/test_name/2342/'},
    'display_name': 'test_name',
    'name': 'test_name',
    'url': 'job/test_name/'}


def test_cihub__post_from_jenkins__1(database, client):
    """It can import jenkins data of a successful test run."""
    url = '/api/jenkins.json'
    response = client.post(
        url,
        json=jenkins_success_data,
        auth=HTTPBasicAuth('testuser', 'testword'),
    )
    assert response.status_code == 200
    query = select([ci_status.c.id, ci_status.c.status])
    res = database.execute(query).fetchall()
    assert [('test_name', StatusEnum.Success)] == res
