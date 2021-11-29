from flask_crontab import Crontab

from .commands import instance_commands

crontab = Crontab()


@crontab.job(minute="*")
def check_expired_instances():
    instance_commands.clean_expired_instances()
