class AuthenticationError(Exception):
    pass

class AuthorizationError(Exception):
    pass

class BadInputError(Exception):
    pass

class BadDataError(Exception):
    pass

def handleExceptions(func):
    async def wrapper(*args, **kwargs):
        resp = { 'error': 'other error' }
        try:
            resp = await func(*args, **kwargs)
        except BadDataError as e:
            resp = { 'error': 'bad data error' }
            print(type(e), e)
        except AuthorizationError as e:
            resp = { 'error': 'permission denied' }
            print(type(e), e)
        except AuthenticationError as e:
            resp = { 'error': 'access denied' }
            print(type(e), e)
        except BadInputError as e:
            print(type(e), e)
        except Exception as e:
            print(type(e), e)
        return resp
    return wrapper

def validateData(d, expected_type, keys=[]):
    try:
        if not isinstance(d, expected_type):
            raise BadDataError()
        if expected_type == dict and any(k not in d.keys() for k in keys):
            raise BadDataError()
    except Exception as e:
        raise BadDataError()
    return True
