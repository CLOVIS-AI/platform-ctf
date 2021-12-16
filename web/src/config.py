import os

from flask.cli import load_dotenv

config_file = "secret.properties"
if os.path.isfile(config_file):
    load_dotenv(config_file)
else:
    print(f"Could not load the '{config_file}' file. "
          "You should either create it, or create the environment variables.")


class Config(object):
    DEBUG = False
    TESTING = False
    TEMPLATES_AUTO_RELOAD = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("database_url")
    """
    URL of the database used by the flask application.
    By default, we use a SQLite database stored in a volume, to ensure persistence of the data
    when the container is killed.
    """

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASE_INSTANCE_DATA = os.environ.get("server_instances")
    CHALLENGE_DIR = os.environ.get("server_challenges")

    INSTANCE_EXPIRATION_TIME = int(os.environ.get("server_instance_expiration"))
    """
    Instance expiration time (seconds).
    """

    # Range of instance IDs to avoid conflicts between platforms (max excluded))
    MIN_VM_INSTANCE_ID = int(os.environ.get("server_instance_min_id"))
    MAX_VM_INSTANCE_ID = int(os.environ.get("server_instance_max_id"))

    # Number of days before the certificate expires (max 90, default 30)
    VPN_EXPIRATION_TIME_DAYS = 1
    VPN_HOSTNAME = os.environ.get("ssh_vpn_hostname") or ""
    VPN_PORT = os.environ.get("ssh_vpn_port") or ""
    VPN_USER = os.environ.get("ssh_vpn_user") or ""

    SECRET_KEY = os.environ.get("server_secret_key") or ""

    DOCKER_HOSTNAME = os.environ.get("ssh_docker_hostname") or ""
    DOCKER_PORT = os.environ.get("ssh_docker_port") or ""
    DOCKER_USER = os.environ.get("ssh_docker_user") or ""

    ALLOW_REGISTRATION = os.environ.get("server_allows_registration") == "yes"
    ALLOW_LOGIN_THROUGH_LOCAL_FORM = os.environ.get("server_allows_direct_login") == "yes"
    ALLOW_CAS_INTEGRATION = os.environ.get("server_cas_integration") == "yes"

    VCENTER_HOST = os.environ.get("terraform_vcenter_host")
    VCENTER_USER = os.environ.get("terraform_vcenter_user")
    VCENTER_PASSWORD = os.environ.get("terraform_vcenter_password")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    BASE_INSTANCE_DATA = "/tmp/data/instances"
    CHALLENGE_DIR = "web/src/tests/test_data/challenges"
