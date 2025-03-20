import jwt
from functools import wraps
from datetime import datetime
from flask import redirect, url_for, flash, session, current_app

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get("jwt_token")
        if not token:
            flash("You must be logged in to access this page.", "danger")
            return redirect(url_for("main.login"))
        try:
            jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            flash("Session expired. Please log in again.", "danger")
            return redirect(url_for("main.login"))
        except jwt.InvalidTokenError:
            flash("Invalid session. Please log in.", "danger")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorated_function
