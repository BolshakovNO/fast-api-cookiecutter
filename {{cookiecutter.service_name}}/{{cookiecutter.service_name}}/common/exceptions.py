

class ServiceBaseException(Exception):
    status_code = NotImplemented

    def __init__(self, msg: str = None):
        if msg is not None:
            self.msg = msg


class NotFound(ServiceBaseException):
    status_code = 404
    msg = 'Not found'


class Conflict(ServiceBaseException):
    status_code = 409
    msg = 'Conflict'
