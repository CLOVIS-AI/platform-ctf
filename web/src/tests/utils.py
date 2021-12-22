from flask import Flask
from flask_testing import TestCase

from ..app import create_app
from ..config import TestingConfig
from ..extensions import db
from ..models import ChallengeValidation, User, Challenge, ChallengeStep
from ..models.challenge_section import ChallengeSection


def populate_db():
    user1 = User(username="user1", email="user1@email.com").save()
    User(username="user2", email="user2@email.com").save()

    logged_user = User(username="logged_user", email="logged@user.com")
    logged_user.set_password("logged_password")
    logged_user.save()

    admin_user = User(username="admin_user", email="admin@user.com")
    admin_user.set_password("admin_password")
    admin_user.is_admin = True
    admin_user.save()

    chall1 = Challenge(
        name="Challenge 1",
        short_name="challenge_1",
        description="Le premier challenge",
    ).save()

    chall2 = Challenge(
        name="Scenario 2",
        short_name="scenario_2",
        description="Le premier scenario",
        category="scenario",
    ).save()

    step1 = ChallengeStep(points=30).save()
    step2 = ChallengeStep(points=10).save()

    ChallengeSection(title="Section 1", description="Description", challenge=chall1, order=0, steps=[step1]).save()
    ChallengeSection(title="Section 1", description="Description", challenge=chall2, order=0, steps=[step2]).save()

    ChallengeValidation(step=step1, user=user1).save()
    ChallengeValidation(step=step2, user=logged_user).save()


class DBTestCase(TestCase):
    def create_app(self):
        app = create_app(TestingConfig())

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class PopulatedDBTestCase(DBTestCase):
    def setUp(self):
        super().setUp()
        populate_db()


class CliTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config.from_object(TestingConfig())
        db.init_app(app)
        self.runner = app.test_cli_runner()
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
