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

from flask import Blueprint, abort, render_template, current_app, redirect, url_for
from flask_login import current_user

from .models import (Challenge, ResourceInstance, User)
from .tables import ChallengeTable, get_instance_table, get_user_table

main_domain = "platform.local"
admin_bp = Blueprint("admin", __name__)


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_admin:
            return abort(403)
        return func(*args, **kwargs)

    return decorated_view


@admin_bp.route("/admin")
@admin_required
def index():
    return render_template("admin/index.jinja2")


# region Challenges

@admin_bp.route("/admin/challenges", methods=["GET"])
@admin_required
def challenges():
    table = ChallengeTable(Challenge.query)
    return render_template("admin/list.jinja2", table=table, title="Challenges")


# endregion
# region Users

@admin_bp.route("/admin/users", methods=["GET", "POST"])
@admin_required
def user_administration():
    users = User.query.order_by(User.username)
    user_table = get_user_table()(users)
    return render_template("admin/list.jinja2", table=user_table, title="Users")


@admin_bp.route("/admin/user/<int:user_id>/toggle_admin", methods=["POST"])
@admin_required
def user_toggle_admin_status(user_id):
    user = User.get(user_id)

    if current_user != user:
        user.is_admin = not user.is_admin
        user.save()
    return redirect(url_for("admin.users"))


@admin_bp.route("/admin/user/<int:user_id>/toggle_banned", methods=["POST"])
@admin_required
def user_toggle_banned_status(user_id):
    user = User.get(user_id)

    if current_user != user:
        user.is_banned = not user.is_banned
        user.save()
    return redirect(url_for("admin.users"))


# endregion
# region Instances

@admin_bp.route("/admin/instances")
@admin_required
def instances():
    table = get_instance_table()(ResourceInstance.query)
    return render_template("admin/list.jinja2", table=table, title="Instances")


@admin_bp.route("/admin/instances/<int:instance_id>/stop", methods=["POST"])
@admin_required
def stop_instance(instance_id=None):
    instance = ResourceInstance.get_or_404(instance_id)
    instance.stop()
    instance.message = "Your instance has been stopped by an administrator."
    instance.save()

    return redirect(url_for("admin.instances"))


# endregion
# region Error handlers

@admin_bp.errorhandler(404)
def page_not_found(_):
    return render_template("404.jinja2"), 404


@admin_bp.errorhandler(403)
def unauthorized_access(_):
    return render_template("403.jinja2"), 403

# endregion
