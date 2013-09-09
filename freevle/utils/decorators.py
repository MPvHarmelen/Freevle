from functools import wraps
from flask import g, request, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('freevle.blueprints.user.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def permalink(function):
    def inner(*args, **kwargs):
        endpoint, values = function(*args, **kwargs)
        return url_for(endpoint, **values)
    return inner
