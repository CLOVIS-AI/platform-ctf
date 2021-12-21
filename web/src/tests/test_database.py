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
