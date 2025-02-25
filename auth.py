import sys
from flask import g
from flask.sessions import SecureCookieSessionInterface
from flask_login import LoginManager, user_loaded_from_request

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from api.auth.model import User

    return User.get(user_id)

@login_manager.request_loader
def load_user_from_request(request):
    from api.auth.model import User

    api_key = request.headers.get('X-Api-Key')
    if api_key:
        user = User.query.filter(User.token==api_key).first()
        if user:
            return user

    return None


@user_loaded_from_request.connect
def user_loaded_from_request(app, user=None):
    g.login_via_request = True


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_request'):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)
