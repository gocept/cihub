from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
import datetime
import pytz
import uvicorn


app = Starlette(debug=True)
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

@app.route('/cc.xml')
async def cc_xml(request):
    """Return the collected data in cc.xml format."""
    return templates.TemplateResponse(
        'cc.jj2',
        {'request': request, 'data': EXAMPLE_DATA},
        media_type="text/xml")


@app.route('/cc.json')
async def cc_json(request):
    """Return the collected data in JSON format."""
    return JSONResponse(EXAMPLE_DATA)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
