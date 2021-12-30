import os

from flask.cli import load_dotenv

config_file = "secret.properties"
if os.path.isfile(config_file):
    load_dotenv(config_file)
else:
    print(f"Could not load the '{config_file}' file. "
          "You should either create it, or create the environment variables.")


class Config(object):

    def __init__(self):
        self.DEBUG = False
        self.TESTING = False
        self.TEMPLATES_AUTO_RELOAD = True

        self.SQLALCHEMY_DATABASE_URI = os.environ.get("database_url")
        """
        URL of the database used by the flask application.
        By default, we use a SQLite database stored in a volume, to ensure persistence of the data
        when the container is killed.
        """

        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        self.BASE_INSTANCE_DATA = os.environ.get("server_instances")
        self.CHALLENGE_DIR = os.environ.get("server_challenges")

        self.INSTANCE_EXPIRATION_TIME = int(os.environ.get("server_instance_expiration"))
        """
        Instance expiration time (seconds).
        """

        # Range of instance IDs to avoid conflicts between platforms (max excluded))
        self.MIN_VM_INSTANCE_ID = int(os.environ.get("server_instance_min_id"))
        self.MAX_VM_INSTANCE_ID = int(os.environ.get("server_instance_max_id"))

        # Number of days before the certificate expires (max 90, default 30)
        self.VPN_EXPIRATION_TIME_DAYS = 1
        self.VPN_HOSTNAME = os.environ.get("ssh_vpn_hostname") or ""
        self.VPN_PORT = os.environ.get("ssh_vpn_port") or ""
        self.VPN_USER = os.environ.get("ssh_vpn_user") or ""

        self.SECRET_KEY = os.environ.get("server_secret_key") or ""

        self.DOCKER_HOSTNAME = os.environ.get("ssh_docker_hostname") or ""
        self.DOCKER_PORT = os.environ.get("ssh_docker_port") or ""
        self.DOCKER_USER = os.environ.get("ssh_docker_user") or ""

        self.ALLOW_REGISTRATION = os.environ.get("server_allows_registration") == "yes"
        self.ALLOW_LOGIN_THROUGH_LOCAL_FORM = os.environ.get("server_allows_direct_login") == "yes"
        self.ALLOW_CAS_INTEGRATION = os.environ.get("server_cas_integration") == "yes"

        self.VCENTER_HOST = os.environ.get("TF_VAR_vcenter_host")
        self.VCENTER_USER = os.environ.get("TF_VAR_vcenter_user")
        self.VCENTER_PASSWORD = os.environ.get("TF_VAR_vcenter_password")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    def __init__(self):
        super(DevelopmentConfig, self).__init__()
        self.DEBUG = True


class TestingConfig(Config):
    def __init__(self):
        super(TestingConfig, self).__init__()
        self.TESTING = True
        self.WTF_CSRF_ENABLED = False
        self.PRESERVE_CONTEXT_ON_EXCEPTION = False
        self.SQLALCHEMY_DATABASE_URI = "sqlite:///"
        self.BASE_INSTANCE_DATA = "/tmp/data/instances"
        self.CHALLENGE_DIR = "web/src/tests/test_data/challenges"
