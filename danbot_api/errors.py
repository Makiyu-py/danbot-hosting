class DBHException(Exception):
    """ Base exception class for this module

    So all of the errors/exceptions below/after this would be a subclass of this
    """
    pass


class NotAllowed(DBHException):
    """ Error when you give an invalid dbh API key
    """
    pass


class HTTPException(DBHException):
    """ The exception for the http errors
    """
    pass


class ServerError(HTTPException):
    """ Gives you this error when the response status is higher than 500
    """

    def __init__(self, status_code: int):
        super().__init__(f"DanBot Hosting Server Error. Status Code: {status_code}")


class APIError(HTTPException):
    """Given when the API itself gives out an error
    """
    def __init__(self, msg):
        super().__init__(f"The API has given you an error: {msg}")
