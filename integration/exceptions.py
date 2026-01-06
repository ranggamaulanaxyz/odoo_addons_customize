from werkzeug.wrappers.response import Response
from werkzeug.exceptions import HTTPException
import json

class IntegrationException(HTTPException):
    data: dict = {}

    def __init__(
        self,
        description: str | None = None,
        data: dict | None = None,
        response: Response | None = None,
    ) -> None:
        super().__init__()
        if description is not None:
            self.description = description
        if data is not None:
            self.response = Response(json.dumps(data), status=self.code, content_type="application/json")
        else:
            self.response = response

class BadRequest(IntegrationException):
    """*400* `Bad Request`

    Raise if the browser sends something to the application the application
    or server cannot handle.
    """

    code = 400
    description = (
        "The browser (or proxy) sent a request that this server could "
        "not understand."
    )