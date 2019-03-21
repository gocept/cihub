from db import StatusEnum
from db import ci_status
from db import database
from db import initialize_database
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
import argparse
import datetime
import pytz
import sys
import uvicorn


app = Starlette()
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


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.route('/cc.xml')
async def cc_xml(request):
    """Return the collected data in cc.xml format."""
    data = [x async for x in fetch_ci_status()]
    return templates.TemplateResponse(
        'cc.jj2',
        {'request': request, 'data': data},
        media_type="text/xml")


@app.route('/cc.json')
async def cc_json(request):
    """Return the collected data in JSON format."""
    data = [x async for x in fetch_ci_status()]
    return JSONResponse(data)


@app.route("/api/jenkins.json", methods=["POST"])
async def post_from_jenkins(request):
    """Store data posted by Jenkins."""
    data = await request.json()
    name = data['display_name']
    query = ci_status.select().where(ci_status.c.id == name)
    existing = await database.fetch_all(query)

    build = data['build']
    status_data = dict(
        url=build['full_url'],
        buildnumber=build['number'],
        status=StatusEnum(build['status']),
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
    return JSONResponse("ok")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="CIHub - aggregates status of CI systems")
    parser.add_argument(
        '--init-db', help='Initialize the database and quit.',
        action='store_true')
    parser.add_argument(
        '--debug', help='Start in debug mode - do not use in production.',
        action='store_true')
    args = parser.parse_args()

    if args.init_db:
        print('Initializing database')
        initialize_database()
        print('Done.')
        sys.exit(0)
    if args.debug:
        app.debug = True

    uvicorn.run(app, host='0.0.0.0', port=8000)
