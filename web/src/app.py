from flask import Flask
from flask_wtf.csrf import CSRFProtect

from .cas import CAS
from .commands import challenge_cli, instance_cli, user_cli
from .config import ProductionConfig
from .cronjobs import crontab
from .extensions import db, login, migrate
from .routes import main_bp
from .routes_admin import admin_bp


def create_app(config_object=ProductionConfig()):
    app = Flask(__name__)

    app.config.from_object(config_object)  # config["VAR"]
    app.configuration = config_object      # configuration.VAR

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_crontabs(app)
    register_CSRFs(app)
    register_cas(app)

    return app


def register_CSRFs(app):
    csrf = CSRFProtect()
    csrf.init_app(app)


def register_crontabs(app):
    crontab.init_app(app)


def register_extensions(app):
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)


def register_commands(app):
    app.cli.add_command(challenge_cli)
    app.cli.add_command(instance_cli)
    app.cli.add_command(user_cli)


def register_cas(app):
    if app.config["ALLOW_CAS_INTEGRATION"]:
        CAS(app, "/cas")
        app.config["CAS_TOKEN_SESSION_KEY"] = "_CAS_TOKEN"
        app.config["CAS_USERNAME_SESSION_KEY"] = "CAS_USERNAME"
        app.config["CAS_ATTRIBUTES_SESSION_KEY"] = "CAS_ATTRIBUTES"
        app.config["CAS_SERVER"] = "https://cas.bordeaux-inp.fr:443"
        app.config["CAS_AFTER_LOGIN"] = "main.after_cas_login"
        app.config["CAS_AFTER_LOGOUT"] = "https://ctf.rsr.enseirb-matmeca.fr/cas/after_logout"
        app.config["CAS_LOGIN_ROUTE"] = "/login"
        app.config["CAS_LOGOUT_ROUTE"] = "/logout"
        app.config["CAS_VALIDATE_ROUTE"] = "/serviceValidate"
