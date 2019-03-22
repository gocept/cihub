from _cihub.config import config
from starlette.authentication import AuthCredentials
from starlette.authentication import AuthenticationBackend
from starlette.authentication import AuthenticationError
from starlette.authentication import SimpleUser
from starlette.responses import PlainTextResponse
import base64
import binascii


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            raise AuthenticationError('You have to authenticate.')

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        if username == config('username') and password == config('password'):
            return AuthCredentials(["authenticated"]), SimpleUser(username)


def on_auth_error(request, exc):
    return PlainTextResponse(
        str(exc),
        headers={'WWW-Authenticate': 'Basic realm=cihub'},
        status_code=401)
