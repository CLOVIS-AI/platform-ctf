#!/usr/bin/env python3

import random
from datetime import datetime, timedelta

import paramiko
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql import func
from sqlalchemy.types import Boolean, DateTime, Integer, String
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db, login


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)

    # Personal data
    username = Column(String(16), index=True, unique=True, nullable=False)
    email = Column(String(120), index=True, unique=True, nullable=False)
    password = Column(String(128))
    team_name = Column(String(16))

    # Personal config
    account_creation_date = Column(DateTime, default=func.now())
    night_mode = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)  # top security
    is_banned = Column(Boolean, default=False)
    is_connected_to_cas = Column(Boolean, default=False)

    # VPN config
    vpn_random_id = Column(String(64))
    vpn_config_file = Column(String(8192))
    vpn_expiration = Column(DateTime)

    instance = relationship("ResourceInstance", uselist=False, back_populates="user")
    validations = relationship("ChallengeValidation", back_populates="user")

    def can_access_logged_content(self):
        return self.is_authenticated and not self.is_banned

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_points_for_challenge(self, challenge):
        points = 0
        for validation in self.validations:
            if validation.step.section.challenge == challenge:
                points += validation.step.points
        return points

    # VPN FUNCTIONS

    def is_vpn_configured(self):
        return self.vpn_random_id and self.vpn_config_file

    def vpn_remaining_time(self):
        if not self.is_vpn_configured():
            return timedelta(0)
        remaining = self.vpn_expiration - datetime.now()
        return remaining if remaining > timedelta(0) else timedelta(0)

    def get_ssh_client(self):
        ssh_key = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")
        ssh_client = paramiko.SSHClient()
        ssh_client.load_host_keys("/root/.ssh/known_hosts")
        ssh_client.load_system_host_keys()
        # Should not be necessary, but sometimes the load_... functions are buggy
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=current_app.config["VPN_HOSTNAME"],
            port=current_app.config["VPN_PORT"],
            username=current_app.config["VPN_USER"],
            pkey=ssh_key,
        )
        return ssh_client

    def revoke_current_vpn_configuration(self):
        if not self.is_vpn_configured():
            return

        ssh_client = self.get_ssh_client()

        command = f"sudo /usr/local/bin/pivpn -r {self.vpn_random_id} -y"
        _, stdout, stderr = ssh_client.exec_command(command)

        # Needed for the revocation to work ?
        stdout.readlines()
        stderr.readlines()

        ssh_client.close()

        self.vpn_random_id = ""
        self.vpn_config_file = ""
        self.vpn_expiration = datetime.now()

        self.save()

    def generate_new_vpn_configuration(self):
        if self.is_vpn_configured():
            current_app.logger.debug(
                "Revoking current certificate before generating a new one"
            )
            self.revoke_current_vpn_configuration()

        new_vpn_id = "".join(
            random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for i in range(32)
        )
        config_expiration = int(current_app.config["VPN_EXPIRATION_TIME_DAYS"])
        new_expiration_days = config_expiration if 0 < config_expiration <= 90 else 30

        ssh_client = self.get_ssh_client()

        command = f"sudo /usr/local/bin/pivpn -a nopass -d {new_expiration_days} -n {new_vpn_id}"
        _, stdout, stderr = ssh_client.exec_command(command)

        if len(stderr.readlines()) > 0:
            ssh_client.close()
            return False

        command = f"cat /home/vpnuser/ovpns/{new_vpn_id}.ovpn | base64"
        _, stdout, stderr = ssh_client.exec_command(command)

        if len(stderr.readlines()) > 0:
            ssh_client.close()
            return False

        config_file = b"".join(stdout.read().splitlines()).decode("utf-8")

        ssh_client.close()

        self.vpn_random_id = new_vpn_id
        self.vpn_config_file = config_file
        self.vpn_expiration = datetime.now() + timedelta(days=new_expiration_days)

        self.save()

        return True

    def __repr__(self):
        return f"{self.username}"


@login.user_loader
def load_user(user_id):
    return User.get(user_id)
