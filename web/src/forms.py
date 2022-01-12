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

import re

from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField, StringField, SubmitField
from wtforms.validators import (AnyOf, DataRequired, Email, EqualTo,
                                ValidationError)

from .models import User

# region Custom validators
# These methods are custom validators for form fields.
# They must accept two arguments, the 'form' and the 'field'.

__RESERVED_KEYWORDS = ["system"]


def not_reserved_keyword(_, field):
    if field.data in __RESERVED_KEYWORDS:
        raise ValidationError("Reserved keyword")


def correct_color_format(_, new_color):
    if len(new_color.data) != 6 or not re.match("[a-fA-F0-9]{6}", new_color.data):
        raise ValidationError("Incorrect color format")


def my_length_check(_, field):
    passwd = field.data
    if not passwd or len(passwd) == 0:
        raise ValidationError("Please input a password")


# endregion
# region Forms

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), my_length_check])
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), not_reserved_keyword]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    @staticmethod
    def validate_username(username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    @staticmethod
    def validate_email(email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class GenerateVpnConfigurationForm(FlaskForm):
    a_hidden_field = HiddenField(
        "generate_hidden_field", validators=[DataRequired(), AnyOf(["generate_config"])]
    )
    vpn_config_generate_submit = SubmitField("Generate")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old password", validators=[DataRequired()])
    password = PasswordField("New password", validators=[DataRequired()])
    password_confirm = PasswordField(
        "Confirm new password", validators=[DataRequired(), EqualTo("password")]
    )
    pw_change_submit = SubmitField("Change")


class ResetProgressForm(FlaskForm):
    username = StringField(
        "Please type your username to confirm your wish", validators=[DataRequired()]
    )
    pr_reset_submit = SubmitField("Reset all my progress")


# region Administration

class BanUserForm(FlaskForm):
    ban_username = StringField("Username", validators=[DataRequired()])
    ban_submit = SubmitField("Ban")


class UnbanUserForm(FlaskForm):
    unban_username = StringField("Username", validators=[DataRequired()])
    unban_submit = SubmitField("Unban")


class AdminUserForm(FlaskForm):
    admin_username = StringField("Username", validators=[DataRequired()])
    admin_submit = SubmitField("Submit")


class UnadminUserForm(FlaskForm):
    unadmin_username = StringField("Username", validators=[DataRequired()])
    unadmin_submit = SubmitField("Submit")

# endregion
# endregion
