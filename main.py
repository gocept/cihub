from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.responses import Response
import datetime
import pytz
import uvicorn


app = Starlette(debug=True)


class XMLResponse(Response):
    media_type = "text/xml"

EXAMPLE_XML = """
<Projects>
    <Project
        name="SvnTest"
        activity="Sleeping"
        lastBuildStatus="Exception"
        lastBuildLabel="8"
        lastBuildTime="2005-09-28T10:30:34.6362160+01:00"
        nextBuildTime="2005-10-04T14:31:52.4509248+01:00"
        webUrl="http://mrtickle/ccnet/"/>

    <Project
        name="HelloWorld"
        activity="Sleeping"
        lastBuildStatus="Success"
        lastBuildLabel="13"
        lastBuildTime="2005-09-15T17:33:07.6447696+01:00"
        nextBuildTime="2005-10-04T14:31:51.7799600+01:00"
        webUrl="http://mrtickle/ccnet/"/>
</Projects>
"""


@app.route('/cc.xml')
async def cc_xml(request):
    """Return the collected data in cc.xml format."""
    return XMLResponse(EXAMPLE_XML)


@app.route('/cc.json')
async def cc_json(request):
    """Return the collected data in JSON format."""
    data = [{
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

    return JSONResponse(data)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
