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

from .utils import DBTestCase, populate_db
from ..extensions import db
from ..models import Challenge, ChallengeStep, ChallengeValidation, User


class TestDatabase(DBTestCase):
    tables = [Challenge, ChallengeStep, ChallengeValidation, User]

    @staticmethod
    def queryAll(typ):
        return db.session.query(typ).all()

    def test_empty_database(self):
        for table in self.tables:
            self.assertListEqual(self.queryAll(table), [], msg=f"The table {table} should be empty.")

    def test_populate_database(self):
        populate_db()

        for table in self.tables:
            self.assertNotEqual(self.queryAll(table), [], msg=f"The table {table} shouldn't be empty.")
