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

from flask_table import Table, Col, BoolCol, DateCol, ButtonCol, DatetimeCol, LinkCol
from flask_wtf.csrf import generate_csrf


# Flask doesn't declare its metaclasses correctly, so PyCharm doesn't understand the declaration here
# See https://youtrack.jetbrains.com/issue/PY-16132
# noinspection PyAbstractClass
class ChallengeTable(Table):
    name = LinkCol("Name", "main.challenge", attr="name", url_kwargs={"challenge_id": "id"})
    category = Col("Category")
    author = Col("Author")
    points = Col("Points")

    # HTML class (bootstrap)
    classes = ["table", "table-striped", "table-sm"]


def get_user_table():
    """Wrapper function around the UserTable class. It is used to be able to
    call the `generate_csrf` function only after the app context has been
    defined, and not at import time. See
    https://github.com/plumdog/flask_table/pull/118/files"""

    csrf_token = generate_csrf()

    # Flask doesn't declare its metaclasses correctly, so PyCharm doesn't understand the declaration here
    # See https://youtrack.jetbrains.com/issue/PY-16132
    # noinspection PyAbstractClass
    class UserTable(Table):
        username = Col("Username")
        account_creation_date = DateCol("Date de cr??ation", date_format="long")
        is_admin = ButtonCol(
            "Admin",
            'admin.user_toggle_admin_status',
            url_kwargs={"user_id": "id"},
            attr="is_admin",
            form_hidden_fields={"csrf_token": csrf_token}
        )
        is_banned = ButtonCol(
            "Banned",
            'admin.user_toggle_banned_status',
            url_kwargs=dict(user_id="id"),
            attr="is_banned"
        )
        is_connected_to_cas = BoolCol("Int??gration CAS", yes_display="Oui", no_display="Non")

        # HTML class (bootstrap)
        classes = ["table", "table-striped", "table-sm"]

    return UserTable


class StopButtonCol(ButtonCol):
    def td_contents(self, item, attr_list):
        if item.stopped:
            self.button_attrs["disabled"] = "true"
        return super().td_contents(item, attr_list)


def get_instance_table():
    """Wrapper function around the InstanceTable class. It is used to be able to
    call the `generate_csrf` function only after the app context has been
    defined, and not at import time. See
    https://github.com/plumdog/flask_table/pull/118/files"""

    csrf_token = generate_csrf()

    # Flask doesn't declare its metaclasses correctly, so PyCharm doesn't understand the declaration here
    # See https://youtrack.jetbrains.com/issue/PY-16132
    # noinspection PyAbstractClass
    class InstanceTable(Table):
        user = Col("User")
        status = Col("Status")
        name = Col("Challenge", attr="resource.challenge.name")
        expiration = DatetimeCol("Expiration", datetime_format="long")

        started = StopButtonCol(
            "Stop",
            'admin.stop_instance',
            url_kwargs={"instance_id": "id"},
            form_hidden_fields={"csrf_token": csrf_token}
        )

        # HTML class (bootstrap)
        classes = ["table", "table-striped", "table-sm"]

    return InstanceTable
