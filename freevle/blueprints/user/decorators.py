from functools import wraps
from flask import g, request, redirect

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.user is None:
            return redirect(url_for('user.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@login_required
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ...
