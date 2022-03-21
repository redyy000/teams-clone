from werkzeug.exceptions import HTTPException

<<<<<<< HEAD

class AccessError(HTTPException):
    code = 403
    message = 'Access error occurred'


class InputError(HTTPException):
    code = 400
    message = 'Input error occurred'
=======
class AccessError(HTTPException):
    code = 403
    message = 'No message specified'

class InputError(HTTPException):
    code = 400
    message = 'No message specified'
>>>>>>> 6c972cd768d05ea09cbb66b5ac0671c8115f28fd
