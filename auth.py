import datetime
from flask import request, g, current_app
import jwt

def is_authorized(f):
    def inner(*args, **kwargs):
        public_key = current_app.config["JWT_SECRET"]
        if "Authorization" not in request.headers:
            return "You are unauthorised!", 401
        authorization = request.headers["Authorization"]
        _, token = authorization.split() # Throw this in some regex to make sure it looks libe "Bearer (.*)"
        try:
            claims = jwt.decode(token, public_key, algorithms=["HS256"]) # comes from jwt library RS256
            g.uid = claims["sub"]
            g.scopes = claims["scope"].split()
            return f(*args, **kwargs)
        except Exception as e:
            return ("Unauthorised!\n" + str(e)), 401
    inner.__name__ = f.__name__
    return inner


def is_teacher(f):
    def inner(*args, **kwargs):
        if ("nbscmanlys-h:teacher" not in g.scopes and g.uid not in current_app.config["ADMINS"]):
            return "You are not a teacher!", 401
        return f(*args, **kwargs)
    inner.__name__ = f.__name__
    return inner

def is_cool(f):
    def inner(*args, **kwargs):
        if g.uid not in current_app.config["ADMINS"]:
            return "You are not a cool!", 401
        return f(*args, **kwargs)
    inner.__name__ = f.__name__
    return inner