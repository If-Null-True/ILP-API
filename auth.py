from flask import request, g, current_app
import requests
import os
import jwt

def is_authorized(f):
    def inner(*args, **kwargs):
        public_key = current_app.config["JWT_PUBLIC_KEY"]
        if "Authorization" not in request.headers:
            return "You are unauthorised!", 401
        authorization = request.headers["Authorization"]
        _, token = authorization.split() # Throw this in some regex to make sure it looks libe "Bearer (.*)"
        try:
            claims = jwt.decode(token, public_key, algorithms=["RS256"]) # comes from jwt library RS256
            print(claims)
            g.uid = claims["sub"]
            g.scopes = claims["scope"].split()
            g.authorization = authorization
            return f(*args, **kwargs)
        except Exception as e:
            return ("Unauthorised!\n" + str(e)), 401
    inner.__name__ = f.__name__
    return inner

def need_user_info(f):
    def inner(*args, **kwargs):
        try:
            url = current_app.config["APP_API_URL"]
            url = os.path.join(url, "user", g.uid)
            headers = {'Authorization': g.authorization}
            print(url)
            req = requests.get(url, headers=headers)
            if not req.status_code == 200:
                return ("Failed to get user info!\nStatus Code: " + str(req.status_code))
            json = req.json()
            g.display_name = json["display_name"]
            g.email_address = json["email_address"]
            return f(*args, **kwargs)
        except Exception as e:
            return ("Failed to get user info!\n" + str(e)), 401
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