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


bitbucket_pipelines_success_data = {
    "actor": {
        "type": "user",
        "username": "emmap1",
        "nickname": "emmap1",
        "display_name": "Emma",
        "uuid": "{a54f16da-24e9-4d7f-a3a7-b1ba2cd98aa3}",
        "links": {}
    },
    "repository": {
        "type": "repository",
        "links": {},
        "uuid": "{673a6070-3421-46c9-9d48-90745f7bfe8e}",
        "project": 'Project',
        "full_name": "team_name/repo_name",
        "name": "repo_name",
        "website": "https://mywebsite.com/",
        "owner": 'Owner',
        "scm": "git",
        "is_private": True
    },
    "commit_status": {
        "name": "Unit Tests (Python)",
        "description": "All tests passed",
        "state": "SUCCESSFUL",
        "key": "mybuildtool",
        "url": "https://my-build-tool.com/builds/MY-PROJECT/BUILD-792",
        "type": "build",
        "created_on": "2015-11-19T20:37:35.547563+00:00",
        "updated_on": "2015-11-20T08:01:16.433108+00:00",
        "links": {}
    }
}


def test_cihub__bitbucket_pipelines_ci_status__1(database, client):
    """It can import Bitbucket Pipelines data of a successful test run."""
    url = '/api/bitbucket.json'
    response = client.post(
        url,
        json=bitbucket_pipelines_success_data,
        auth=HTTPBasicAuth('testuser', 'testword'),
    )
    assert response.status_code == 200
    query = select([ci_status.c.id, ci_status.c.status])
    res = database.execute(query).fetchall()
    assert [('repo_name', StatusEnum.Success)] == res
