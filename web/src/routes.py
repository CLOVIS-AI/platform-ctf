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

import base64
import datetime
import os

from flask import (Blueprint, Response, abort, current_app, flash, jsonify,
                   redirect, render_template, request, send_from_directory,
                   session, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.sql import desc, func

from .extensions import db
from .forms import (ChangePasswordForm, GenerateVpnConfigurationForm,
                    LoginForm, RegistrationForm, ResetProgressForm)
from .models import (Challenge, ChallengeSection, ChallengeStep,
                     ChallengeValidation, User, Documentation)

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@main_bp.route("/index")
def index():
    logout_if_banned()
    return render_template("index.jinja2", title="Home", page_index=True)


@main_bp.route("/challenges")
def challenges():
    """
    Challenges page.

    .. http:get:: /challenges
       Display all challenges, sorted by category and ordered by number of points, with user progress if logged in

    """
    logout_if_banned()

    data = {}

    challenges_and_points = (
        (db.session.query(Challenge, func.sum(ChallengeStep.points))
         .filter(Challenge.category != "SCENARIO")
         .filter(Challenge.category != "TRAINING")
         .join(ChallengeSection, ChallengeSection.chall_id == Challenge.id)
         .join(ChallengeStep, ChallengeStep.section_id == ChallengeSection.id)
         .group_by(Challenge.id)
         .order_by(func.sum(ChallengeStep.points))
         .all())
    )

    for challenge, points in challenges_and_points:
        if current_user.is_authenticated:
            challenge.current_user_points = current_user.get_points_for_challenge(
                challenge
            )
        if challenge.category not in data:
            data[challenge.category] = []
        data[challenge.category].append(challenge)

    return render_template("challenges.jinja2", data=data, page_challenges=True)


@main_bp.route("/documentation")
def documentation():
    """
    Documentation page.

    .. http:get:: /documentation
       Display all documentation, sorted by category

    """
    logout_if_banned()

    data = {}

    doc_list = (
        db.session.query(Documentation)
        .all()
    )
    for doc in doc_list:
        if doc.category not in data:
            data[doc.category] = []
        data[doc.category].append(doc)

    return render_template("documentation.jinja2", data=data, page_documentation=True)


@main_bp.route("/scenarios", defaults={"category": "SCENARIO"})
@main_bp.route("/trainings", defaults={"category": "TRAINING"})
def scenarios_trainings(category):
    logout_if_banned()
    return render_template(
        "scenarios_trainings.jinja2",
        challenges=Challenge.query.filter(Challenge.category == category),
        category=category,
    )


@main_bp.route("/challenge/<int:challenge_id>", methods=["GET"])
def challenge(challenge_id=None):
    logout_if_banned()
    challenge = Challenge.get_or_404(challenge_id)
    sections = challenge.sections

    if current_user.is_authenticated:
        for section in sections:
            section.completed = True
            for step in section.steps:
                if not step.validated():
                    section.completed = False
                    break

    return render_template(
        "challenge.jinja2",
        challenge=challenge,
        orphan_steps=[],
        sections=sections,
        server_time=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
    )


@main_bp.route("/challenge/<int:challenge_id>", methods=["POST"])
def action_on_challenge(challenge_id=None):
    """
    Start, Stop and status about a challenge.

    :param challenge_id: unique identifier of the challenge in DB
    """
    logout_if_banned()

    if not current_user.is_authenticated:
        return jsonify({"status": "unauthentified"}), 403

    challenge = Challenge.get(challenge_id)
    if not challenge:
        return jsonify({"status": "unknown"}), 404

    action = request.form["action"]

    if action == "start":
        if current_user.instance and current_user.instance.status not in ["stopped", "error"]:
            return jsonify(current_user.instance.status_as_dict()), 200
        try:
            challenge.resource.instantiate(current_user)
            instance = current_user.instance.start()
            if instance["status"] == "started":
                return jsonify(instance)
            return jsonify(instance), 500
        except Exception as e:
            current_app.logger.warning(e)
            return jsonify(current_user.instance.status_as_dict()), 500

    if action == "status":
        if current_user.instance:
            return jsonify(current_user.instance.status_as_dict())
        else:
            return jsonify(
                {
                    "id": None,
                    "status": None,
                    "message": None,
                    "expiration": None,
                    "challenge": None,
                    "server_time": datetime.datetime.now().strftime(
                        "%m/%d/%Y, %H:%M:%S"
                    ),
                }
            )

    if action == "stop":
        answer = jsonify(current_user.instance.stop())
        current_user.instance.delete()
        return answer

    if action == "timeout":
        return current_user.instance.timeout()

    if action == "extend":
        return jsonify(
            {
                "status": "extended"
                if current_user.instance.extend_time()
                else "not_extended"
            }
        )

    return jsonify({"status": "unknown"}), 404


@main_bp.route("/submit/<int:step_id>", methods=["POST"])
def submit_flag(step_id=None):
    try:
        step = ChallengeStep.get(step_id)
        return jsonify(step.validate_submission_if_correct(request.form["flag"]))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"status": "failed"})


@main_bp.route("/challenge/<int:challenge_id>/static/<static_file>", methods=["GET"])
def challenge_static_file(challenge_id=None, static_file=None):
    """
    A static file included into the "static" subfolder of the challenge.

    :param challenge_id: identifier of the challenge, default to None
    :param static_file: name of the file
    """
    logout_if_banned()

    if not challenge_id or not static_file:
        abort(404)

    challenge = Challenge.query.filter(Challenge.id == challenge_id).first()

    if not challenge:
        abort(404)

    challenge_static_dir = os.path.join(
        current_app.config["CHALLENGE_DIR"], challenge.short_name, "static/"
    )

    if not os.path.isfile(os.path.join(challenge_static_dir, static_file)):
        abort(404)

    return send_from_directory(directory=challenge_static_dir, path=static_file)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Login page

    .. http:get:: /login
       Display login form + link to register

    .. http:post:: /login
       Verify login form submission and load user session

    """
    logout_if_banned()
    if current_user.is_authenticated:
        return redirect("/")

    if (
            not current_app.config["ALLOW_LOGIN_THROUGH_LOCAL_FORM"]
            and current_app.config["ALLOW_CAS_INTEGRATION"]
    ):
        return redirect(url_for("cas.login"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and user.is_connected_to_cas:
            flash(
                'This user is linked to the CAS. Log in using the "Log in with CAS" button.',
                category="danger",
            )
            return redirect(url_for("main.login"))

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", category="danger")
            return redirect(url_for("main.login"))
        if user.is_banned:
            flash(
                "You were banned and can no longer connect to our website",
                category="danger",
            )
            return redirect("index")
        login_user(user)
        return redirect("index")

    return render_template(
        "login.jinja2",
        title="Sign In",
        form=form,
        allow_cas=current_app.config["ALLOW_CAS_INTEGRATION"],
        allow_register=current_app.config["ALLOW_REGISTRATION"],
    )


@main_bp.route("/cas/after_login")
def after_cas_login():
    """
    CAS login management page.
      - If the user does not exist in the local database, it is created and linked to CAS.
      - If the user already exists and is connected to CAS, he is logged in.
      - If the user already exists but is not connected to CAS, the user is connected to CAS and then logged in.
    """
    if not current_app.config["ALLOW_CAS_INTEGRATION"]:
        return redirect(url_for("main.index"))

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if not current_app.config["CAS_USERNAME_SESSION_KEY"] in session:
        return redirect(url_for("cas.login"))

    username = session[current_app.config["CAS_USERNAME_SESSION_KEY"]]

    user = User.query.filter_by(username=username).first()

    if user is None:
        user = User(username=username, email=f"{username}@enseirb-matmeca.fr")
        user.set_password("USER_FROM_CAS")
        user.is_connected_to_cas = True
        user.save()

    elif not user.is_connected_to_cas:
        user.set_password("USER_FROM_CAS")
        user.is_connected_to_cas = True
        user.email = f"{username}@enseirb-matmeca.fr"
        user.save()
        flash(
            f"The user {username} has been linked to the CAS. "
            f"It is no longer possible to login using the standard form.",
            category="warning",
        )

    if user.is_banned:
        flash(
            "You were banned and can no longer connect to our website",
            category="danger",
        )
        return redirect(url_for("main.index"))

    login_user(user)
    return redirect(url_for("main.index"))


@main_bp.route("/cas/after_logout")
def after_cas_logout():
    return redirect(url_for("main.index"))


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    logout_if_banned()

    if not current_app.config["ALLOW_REGISTRATION"]:
        flash(
            "Registration is disabled",
            category="danger",
        )
        return redirect(url_for("main.index"))

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.is_connected_to_cas = False
        user.save()
        flash("Welcome on board, sergeant!", category="success")
        return redirect(url_for("main.login"))
    return render_template("register.jinja2", title="Register", form=form)


@main_bp.route("/logout")
@login_required
def logout_page():
    """Logout page.
    Directly acts with the flask-login plugin to clear the session"""
    logout_from_cas = current_user.is_connected_to_cas
    logout_user()
    if logout_from_cas:
        if current_app.config["CAS_USERNAME_SESSION_KEY"] in session:
            session.pop(current_app.config["CAS_USERNAME_SESSION_KEY"])
    return redirect("/")


@main_bp.route("/user/settings", methods=["GET", "POST"])
@login_required
def settings():
    """
    Settings modification page

    .. http:get:: /user/settings
       Display form for changing password, handle the VPN and resetting all progress

    .. http:post:: /user/settings
       Process forms
    """
    logout_if_banned()
    change_pass_form = ChangePasswordForm()
    reset_progress_form = ResetProgressForm()
    generate_vpn_configuration_form = GenerateVpnConfigurationForm(
        a_hidden_field="generate_config"
    )
    if change_pass_form.validate_on_submit():
        if change_pass(
                current_user.username,
                change_pass_form.old_password.data,
                change_pass_form.password.data,
        ):
            flash("Your password was successfully changed !", category="success")
        else:
            flash("Your password has not been changed", category="danger")
    elif reset_progress_form.validate_on_submit():
        if reset_progress(current_user.username, reset_progress_form.username.data):
            flash("Your progress has been reset", "success")
        else:
            flash("The submitted username is not valid", "danger")
    elif generate_vpn_configuration_form.validate_on_submit():
        created = current_user.generate_new_vpn_configuration()
        if created:
            flash("Your connection pack have been successfully generated !", "success")
        else:
            flash("Error while generating your VPN connection pack", "danger")

    vpn_info = {
        "is_configured": current_user.is_vpn_configured(),
        "expires_in": None,
    }

    if vpn_info["is_configured"]:
        vpn_remaining_time = current_user.vpn_remaining_time()
        if vpn_remaining_time.days > 0:
            vpn_info["expires_in"] = f"{vpn_remaining_time.days} days"
        else:
            vpn_info[
                "expires_in"
            ] = f"{vpn_remaining_time.seconds // 3600} hours {(vpn_remaining_time.seconds // 60) % 60} minutes"

    return render_template(
        "settings.jinja2",
        title="Settings",
        pw_change_form=change_pass_form,
        reset_progress_form=reset_progress_form,
        generate_vpn_configuration_form=generate_vpn_configuration_form,
        vpn=vpn_info,
        settings=True,
    )


@main_bp.route("/ranking")
def ranking():
    """
    Display scores of top users, system-wide (different from /status which shows information about specific user)

    Currently shows the users with the most points.
    """
    logout_if_banned()

    hall_of_fame = (
        (User.query.outerjoin(ChallengeValidation)
         .outerjoin(ChallengeStep)
         .with_entities(
            User.id,
            User.username,
            func.sum(ChallengeStep.points).label("points_sum"),
        )
         .group_by(User.id)
         .order_by(desc("points_sum"))
         .limit(100)
         .all())
    )

    users_to_display = False
    for challenger in hall_of_fame:
        if challenger.points_sum and challenger.points_sum > 0:
            users_to_display = True
            break

    return render_template(
        "ranking.jinja2",
        title="Hall of fame",
        hall_of_fame=hall_of_fame,
        page_ranking=True,
        users_to_display=users_to_display,
    )


@main_bp.route("/user/vpn/download")
@login_required
def download_vpn_file():
    logout_if_banned()

    if not current_user.is_vpn_configured():
        flash(
            "You must generate your connection pack before downloading it.",
            category="warning",
        )
        return redirect(url_for("main.settings"))

    configuration_file = base64.b64decode(
        current_user.vpn_config_file).decode("utf-8")

    return Response(
        configuration_file,
        mimetype="text/plain",
        headers={
            "Content-Disposition": "attachment;filename=vpn_connection_pack.ovpn"},
    )


# region Miscellaneous, helper functions

@main_bp.route("/user/nightmode")
@login_required
def toggle_night_mode():
    """
    Switch CSS theme based on toggle existing in DB for every user
    """
    logout_if_banned()
    current_user.night_mode = not current_user.night_mode
    current_user.save()
    return redirect(url_for("main.index"))


@main_bp.errorhandler(404)
def page_not_found(e):
    """
    Custom error page for 404 HTTP errors
    """
    return render_template("404.jinja2"), 404


def logout_if_banned():
    if current_user.is_authenticated and current_user.is_banned:
        logout_user()


def change_pass(username, old_pass, new_pass):
    """
    Helper function to change password of a user

    :param username: Name of the user querying a pass change
    :param old_pass: Current password of the user, as submitted in the form (for double checking)
    :param new_pass: Wished new password
    :param username: str
    :type old_pass: str
    :type new_pass: str
    """
    user = User.query.filter_by(username=username).first()
    if user is None or user.is_connected_to_cas or not user.check_password(old_pass):
        return False
    user.set_password(new_pass)
    user.save()
    return True


def reset_progress(username, submitted_username):
    """
    Helper function to reset full progress of user

    All the challenges progress will be forgotten

    All the steps completed in various scenarios will be forgotten

    :param username: Name of the user asking for a progress reset
    :param submitted_username: Username submitted by the user, so as to double check and avoid hasty click on form
    :type username: str
    :type submitted_username: str
    """
    if username != submitted_username:
        return False
    for step in ChallengeValidation.query.filter(
            ChallengeValidation.user_id == current_user.id
    ).all():
        step.delete()
    return True

# endregion
