#  CTF Platform by RSR, educational platform to try cyber-security challenges
#  Copyright (C) 2022 ENSEIRB-MATMECA, Bordeaux-INP, RSR formation since 2018
#  Supervised by Toufik Ahmed, tad@labri.fr
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from functools import wraps

import flask
from flask import _request_ctx_stack as stack  # TODO: cleanup in #30
from flask import current_app

from . import routing


class CAS(object):
    """
    Required Configs:

    |Key             |
    |----------------|
    |CAS_SERVER      |
    |CAS_AFTER_LOGIN |

    Optional Configs:

    |Key                        | Default               |
    |---------------------------|-----------------------|
    |CAS_TOKEN_SESSION_KEY      | _CAS_TOKEN            |
    |CAS_USERNAME_SESSION_KEY   | CAS_USERNAME          |
    |CAS_ATTRIBUTES_SESSION_KEY | CAS_ATTRIBUTES        |
    |CAS_LOGIN_ROUTE            | '/cas'                |
    |CAS_LOGOUT_ROUTE           | '/cas/logout'         |
    |CAS_VALIDATE_ROUTE         | '/cas/serviceValidate'|
    |CAS_AFTER_LOGOUT           | None                  |
    """

    def __init__(self, app=None, url_prefix=None):
        self._app = app
        if app is not None:
            self.init_app(app, url_prefix)

    def init_app(self, app, url_prefix=None):
        # Configuration defaults
        app.config.setdefault("CAS_TOKEN_SESSION_KEY", "_CAS_TOKEN")
        app.config.setdefault("CAS_USERNAME_SESSION_KEY", "CAS_USERNAME")
        app.config.setdefault("CAS_ATTRIBUTES_SESSION_KEY", "CAS_ATTRIBUTES")
        app.config.setdefault("CAS_LOGIN_ROUTE", "/cas")
        app.config.setdefault("CAS_LOGOUT_ROUTE", "/cas/logout")
        app.config.setdefault("CAS_VALIDATE_ROUTE", "/cas/serviceValidate")
        # Requires CAS 2.0
        app.config.setdefault("CAS_AFTER_LOGOUT", None)
        # Register Blueprint
        app.register_blueprint(routing.blueprint, url_prefix=url_prefix)

        # Use the new style teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, "teardown_appcontext"):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        stack.top

    @property
    def app(self):
        return self._app or current_app

    @property
    def username(self):
        return flask.session.get(self.app.config["CAS_USERNAME_SESSION_KEY"], None)

    @property
    def attributes(self):
        return flask.session.get(self.app.config["CAS_ATTRIBUTES_SESSION_KEY"], None)

    @property
    def token(self):
        return flask.session.get(self.app.config["CAS_TOKEN_SESSION_KEY"], None)


def login():
    return flask.redirect(flask.url_for("cas.login", _external=True))


def logout():
    return flask.redirect(flask.url_for("cas.logout", _external=True))


def login_required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        if "CAS_USERNAME" not in flask.session:
            flask.session["CAS_AFTER_LOGIN_SESSION_URL"] = (
                    flask.request.script_root + flask.request.full_path
            )
            return login()
        else:
            return function(*args, **kwargs)

    return wrap
