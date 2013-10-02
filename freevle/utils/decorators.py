from functools import wraps
from flask import url_for

def permalink(function):
    @wraps(function)
    def inner(*args, **kwargs):
        endpoint, values = function(*args, **kwargs)
        return url_for(endpoint, **values)
    return inner
