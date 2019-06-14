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


travis_success_data = {
    "id": 545671425,
    "number": "566",
    "config": {
        "os": "linux",
        "dist": "trusty",
        "sudo": False,
        "cache": {
            "pip": True,
            "directories": [
                "vendor/bundle",
                "node_modules"
            ]
        },
        "group": "stable",
        "deploy": {
            "app": "docs-travis-ci-com",
            "true": {
                "branch": ["master"]
            },
            "api_key": {"secure": "hylw..."},
            "provider": "heroku",
            "skip_cleanup": True
        },
        "python": ["3.5.2"],
        "script": ["bundle exec rake test"],
        ".result": "configured",
        "install": [
            "rvm use 2.3.1 --install",
            "bundle install --deployment"
        ],
        "branches": {
            "only": ["master"]
        },
        "language": "python",
        "global_env": ["PATH=$HOME/.local/user/bin:$PATH"],
        "notifications": {
            "slack": {
                "rooms": {"secure": "LPN..."},
                "on_success": "never"
            },
            "webhooks": "https://docs.travis-ci.com/update_webhook_payload_doc"
        }
    },
    "type": "cron",
    "state": "failed",
    "status": 1,
    "result": 1,
    "status_message": "Still Failing",
    "result_message": "Still Failing",
    "started_at": "2019-06-14T10:06:51Z",
    "finished_at": "2019-06-14T10:07:51Z",
    "duration": 60,
    "build_url": "https://travis-ci.org/lapolinar/docs/builds/545671425",
    "commit_id": 164949783,
    "commit": "14e8e737d1054b1776bb7b9c2ddfa793f2f85cfa",
    "base_commit": None,
    "head_commit": None,
    "branch": "master",
    "message": "Update deployments.yml",
    "compare_url": "https://github.com/lapolinar/docs-travis-ci-com/...",
    "committed_at": "2019-01-06T02:01:09Z",
    "author_name": "apolinar",
    "author_email": "lapolinar2368@gmail.com",
    "committer_name": "GitHub",
    "committer_email": "noreply@github.com",
    "pull_request": False,
    "pull_request_number": None,
    "pull_request_title": None,
    "tag": None,
    "repository": {
        "id": 15948437,
        "name": "docs-travis-ci-com",
        "owner_name": "lapolinar",
        "url": None
    },
    "matrix": [{
        "id": 545671426,
        "repository_id": 15948437,
        "parent_id": 545671425,
        "number": "566.1",
        "state": "failed",
        "config": {
            "os": "linux",
            "dist": "trusty",
            "sudo": False,
            "cache": {
                "pip": True,
                "directories": [
                    "vendor/bundle",
                    "node_modules"
                ]
            },
            "group": "stable",
            "addons": {
                "deploy": {
                    "app": "docs-travis-ci-com",
                    "true": {"branch": ["master"]},
                    "api_key": {"secure": "hyl..."},
                    "provider": "heroku",
                    "skip_cleanup": True
                }
            },
            "python": "3.5.2",
            "script": ["bundle exec rake test"],
            ".result": "configured",
            "install": [
                "rvm use 2.3.1 --install",
                "bundle install --deployment"
            ],
            "branches": {"only": ["master"]},
            "language": "python",
            "global_env": ["PATH=$HOME/.local/user/bin:$PATH"],
            "notifications": {
                "slack": {
                    "rooms": {"secure": "LPN..."},
                    "on_success": "never"
                },
                "webhooks": "https://docs.travis-ci.com/..."
            }
        },
        "status": 1,
        "result": 1,
        "commit": "14e8e737d1054b1776bb7b9c2ddfa793f2f85cfa",
        "branch": "master",
        "message": "Update deployments.yml",
        "compare_url": "https://github.com/lapolinar/...",
        "started_at": "2019-06-14T10:06:51Z",
        "finished_at": "2019-06-14T10:07:51Z",
        "committed_at": "2019-01-06T02:01:09Z",
        "author_name": "apolinar",
        "author_email": "lapolinar2368@gmail.com",
        "committer_name": "GitHub",
        "committer_email": "noreply@github.com",
        "allow_failure": False
    }]
}


def test_cihub__travis_ci_status__1(database, client):
    """It can import TravisCI data of a failed test run."""
    url = '/api/travis.json'
    response = client.post(
        url,
        json=travis_success_data,
        auth=HTTPBasicAuth('testuser', 'testword'),
    )
    assert response.status_code == 200
    query = select([
        ci_status.c.id,
        ci_status.c.url,
        ci_status.c.buildnumber,
        ci_status.c.status,
    ])
    res = database.execute(query).fetchall()
    assert [(
        'docs-travis-ci-com',
        'https://travis-ci.org/lapolinar/docs/builds/545671425',
        566,
        StatusEnum.Failure)] == res
