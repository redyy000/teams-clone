from werkzeug.exceptions import HTTPException


class AccessError(HTTPException):
    code = 403
    message = 'Access error occurred'


class InputError(HTTPException):
    code = 400
    message = 'Input error occurred'
