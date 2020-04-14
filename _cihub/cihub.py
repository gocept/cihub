from _cihub.auth import BasicAuthBackend
from _cihub.auth import on_auth_error
from _cihub.db import StatusEnum
from _cihub.db import ci_status
from _cihub.db import database
from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
import datetime
import json
import pytz


app = Starlette()
app.add_middleware(AuthenticationMiddleware,
                   backend=BasicAuthBackend(),
                   on_error=on_auth_error)
templates = Jinja2Templates(directory='templates')


EXAMPLE_DATA = [{
    'name': 'dgb.internet',
    'url': 'https://jenkins.verdi4you.de/job/dgb.internet/3433/',
    'buildnumber': 3433,
    'status': 'Success',
    'timestamp': str(datetime.datetime.now(pytz.UTC)),
}, {
    'name': 'dgb.content',
    'url': 'https://jenkins.verdi4you.de/job/dgb.content/1234/',
    'buildnumber': 1234,
    'status': 'Failure',
    'timestamp': str(datetime.datetime.now(pytz.UTC)),
}, {
    'name': 'uc.https',
    'url': 'https://jenkins.verdi4you.de/job/uc.https/321/',
    'buildnumber': 321,
    'status': 'Unknown',
    'timestamp': '2005-09-28 10:30:34.6362160+01:00',
}]

async def fetch_ci_status():
    """Fetch all stored ci status."""
    query = ci_status.select().order_by(ci_status.c.id)
    async for row in database.iterate(query):
        yield {
            'name': row['id'],
            'url': row['url'],
            'buildnumber': row['buildnumber'],
            'status': row['status'].value,
            'timestamp': row['timestamp'].isoformat(),
        }


async def store(name, *, url, buildnumber, status):
    """Store job date int the database."""
    query = ci_status.select().where(ci_status.c.id == name)
    existing = await database.fetch_all(query)

    status_data = dict(
        url=url,
        buildnumber=buildnumber,
        status=StatusEnum[status],
        timestamp=datetime.datetime.now(pytz.UTC),
    )

    if len(existing):
        query = (
            ci_status.update()
            .where(ci_status.c.id == name)
            .values(status_data))
    else:
        status_data['id'] = name
        query = ci_status.insert().values(status_data)

    await database.execute(query)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.route('/cc.xml')
@requires('authenticated')
async def cc_xml(request):
    """Return the collected data in cc.xml format."""
    data = [x async for x in fetch_ci_status()]
    return templates.TemplateResponse(
        'cc.jj2',
        {'request': request, 'data': data},
        media_type="text/xml")


@app.route('/cc.json')
@requires('authenticated')
async def cc_json(request):
    """Return the collected data in JSON format."""
    data = [x async for x in fetch_ci_status()]
    return JSONResponse(data)


@app.route("/api/jenkins.json", methods=["POST"])
@requires('authenticated')
async def post_from_jenkins(request):
    """Store data posted by Jenkins."""
    data = await request.json()
    name = data['display_name']
    build = data['build']
    await store(
        name,
        url=build['full_url'],
        buildnumber=build['number'],
        status=build['status'])
    return JSONResponse("ok")


@app.route("/api/bitbucket.json", methods=["POST"])
@requires('authenticated')
async def bitbucket_pipelines_ci_status(request):
    """Store data posted by Bitbucket pipelines."""
    data = await request.json()

    name = data['repository']['name']
    commit_status = data['commit_status']
    await store(
        name,
        url=commit_status['url'],
        buildnumber=0,
        status=commit_status['state'])
    return JSONResponse("ok")


@app.route("/api/travis.json", methods=["POST"])
@requires('authenticated')
async def travis_ci_status(request):
    """Store data posted by TravisCI."""
    form = await request.form()
    data = json.loads(form['payload'])

    if data['branch'] != 'master':
        return JSONResponse("ok")

    if data['pull_request']:
        return JSONResponse("ok")

    name = data['repository']['name']
    await store(
        name,
        url=data['build_url'],
        buildnumber=data['number'],
        status=data['status_message'].replace(' ', ''))
    return JSONResponse("ok")


@app.route("/api/github.json", methods=["POST"])
@requires('authenticated')
async def github_actions_status(request):
    """Store data posted by Github for `check_suite` events."""
    data = await request.json()
    result = JSONResponse("ok")

    if data["action"] != "completed":
        return result

    master_branch_name = data["repository"]["default_branch"]
    if data["check_suite"]["head_branch"] != master_branch_name:
        return result

    html_url = data["repository"]["html_url"]
    commit_id = data["check_suite"]["head_sha"]
    suite_id = data["check_suite"]["id"]
    await store(
        name=data['repository']['name'],
        url=f'{html_url}/commit/{commit_id}/checks?check_suite_id={suite_id}',
        buildnumber=0,
        status=data['check_suite']['conclusion'])
    return result


@app.route("/api/gitlab.json", methods=["POST"])
@requires('authenticated')
async def gitlab_ci_status(request):
    """Store data posted by Gitlab CI for job events."""
    data = await request.json()
    result = JSONResponse("ok")

    if data['ref'] != 'master':
        return result

    status = data['build_status']
    if getattr(StatusEnum, status, None) is None:
        return result

    homepage_url = data['repository']['homepage']
    build_id = data['build_id']
    await store(
        name=data['repository']['name'],
        url=f'{homepage_url}/-/jobs/{build_id}',
        buildnumber=0,
        status=data['build_status'])

    return result
