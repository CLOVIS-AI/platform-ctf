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

from urllib.request import urlopen

import flask
from flask import current_app
from xmltodict import parse

from .cas_urls import create_cas_login_url
from .cas_urls import create_cas_logout_url
from .cas_urls import create_cas_validate_url

blueprint = flask.Blueprint("cas", __name__)


@blueprint.route("/login/")
def login():
    """
    This route has two purposes. First, it is used by the user
    to login. Second, it is used by the CAS to respond with the
    `ticket` after the user logs in successfully.

    When the user accesses this url, they are redirected to the CAS
    to login. If the login was successful, the CAS will respond to this
    route with the ticket in the url. The ticket is then validated.
    If validation was successful the logged in username is saved in
    the user's session under the key `CAS_USERNAME_SESSION_KEY` and
    the user's attributes are saved under the key
    'CAS_USERNAME_ATTRIBUTE_KEY'
    """

    cas_token_session_key = current_app.config["CAS_TOKEN_SESSION_KEY"]

    redirect_url = create_cas_login_url(
        current_app.config["CAS_SERVER"],
        current_app.config["CAS_LOGIN_ROUTE"],
        flask.url_for(
            ".login",
            origin=flask.session.get("CAS_AFTER_LOGIN_SESSION_URL"),
            _external=True,
        ),
    )

    if "ticket" in flask.request.args:
        flask.session[cas_token_session_key] = flask.request.args["ticket"]

    if cas_token_session_key in flask.session:

        if validate(flask.session[cas_token_session_key]):
            if "CAS_AFTER_LOGIN_SESSION_URL" in flask.session:
                redirect_url = flask.session.pop("CAS_AFTER_LOGIN_SESSION_URL")
            elif flask.request.args.get("origin"):
                redirect_url = flask.request.args["origin"]
            else:
                redirect_url = flask.url_for(current_app.config["CAS_AFTER_LOGIN"])
        else:
            del flask.session[cas_token_session_key]

    current_app.logger.debug("Redirecting to: {0}".format(redirect_url))

    return flask.redirect(redirect_url)


@blueprint.route("/logout/")
def logout():
    """
    When the user accesses this route they are logged out.
    """

    cas_username_session_key = current_app.config["CAS_USERNAME_SESSION_KEY"]
    cas_attributes_session_key = current_app.config["CAS_ATTRIBUTES_SESSION_KEY"]

    if cas_username_session_key in flask.session:
        del flask.session[cas_username_session_key]

    if cas_attributes_session_key in flask.session:
        del flask.session[cas_attributes_session_key]

    if current_app.config["CAS_AFTER_LOGOUT"] is not None:
        redirect_url = create_cas_logout_url(
            current_app.config["CAS_SERVER"],
            current_app.config["CAS_LOGOUT_ROUTE"],
            current_app.config["CAS_AFTER_LOGOUT"],
        )
    else:
        redirect_url = create_cas_logout_url(
            current_app.config["CAS_SERVER"], current_app.config["CAS_LOGOUT_ROUTE"]
        )

    current_app.logger.debug("Redirecting to: {0}".format(redirect_url))
    return flask.redirect(redirect_url)


def validate(ticket):
    """
    Will attempt to validate the ticket. If validation fails, then False
    is returned. If validation is successful, then True is returned
    and the validated username is saved in the session under the
    key `CAS_USERNAME_SESSION_KEY` while tha validated attributes dictionary
    is saved under the key 'CAS_ATTRIBUTES_SESSION_KEY'.
    """

    cas_username_session_key = current_app.config["CAS_USERNAME_SESSION_KEY"]
    cas_attributes_session_key = current_app.config["CAS_ATTRIBUTES_SESSION_KEY"]

    current_app.logger.debug("validating token {0}".format(ticket))

    cas_validate_url = create_cas_validate_url(
        current_app.config["CAS_SERVER"],
        current_app.config["CAS_VALIDATE_ROUTE"],
        flask.url_for(
            ".login",
            origin=flask.session.get("CAS_AFTER_LOGIN_SESSION_URL"),
            _external=True,
        ),
        ticket,
    )

    current_app.logger.debug("Making GET request to {0}".format(cas_validate_url))

    xml_from_dict = {}
    isValid = False

    try:
        xml_dump = urlopen(cas_validate_url).read().strip().decode("utf8", "ignore")
        xml_from_dict = parse(xml_dump)
        isValid = "cas:authenticationSuccess" in xml_from_dict["cas:serviceResponse"]
    except ValueError:
        current_app.logger.error("CAS returned unexpected result")

    if isValid:
        current_app.logger.debug("valid")
        xml_from_dict = xml_from_dict["cas:serviceResponse"][
            "cas:authenticationSuccess"
        ]
        username = xml_from_dict["cas:user"]
        flask.session[cas_username_session_key] = username

        if "cas:attributes" in xml_from_dict:
            attributes = xml_from_dict["cas:attributes"]

            if attributes and "cas:memberOf" in attributes:
                if not isinstance(attributes["cas:memberOf"], list):
                    attributes["cas:memberOf"] = (
                        attributes["cas:memberOf"].lstrip("[").rstrip("]").split(",")
                    )
                    for group_number in range(0, len(attributes["cas:memberOf"])):
                        attributes["cas:memberOf"][group_number] = (
                            attributes["cas:memberOf"][group_number].lstrip(" ").rstrip(" ")
                        )
                else:
                    for index in range(0, len(attributes["cas:memberOf"])):
                        attributes["cas:memberOf"][index] = (
                            attributes["cas:memberOf"][index].lstrip("[").rstrip("]").split(",")
                        )
                        for group_number in range(0, len(attributes["cas:memberOf"][index])):
                            attributes["cas:memberOf"][index][group_number] = (
                                attributes["cas:memberOf"][index][group_number].lstrip(" ").rstrip(" ")
                            )

            flask.session[cas_attributes_session_key] = attributes
    else:
        current_app.logger.debug("invalid")

    return isValid
