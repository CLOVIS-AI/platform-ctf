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

import yaml
from os.path import isfile


def save_new_model(new_model):
    new_model.save()
    new_model.name = new_model.name.format(new_model.id)
    new_model.short_name = new_model.short_name.format(new_model.id)
    new_model.save()


def safe_open_file(file_name):
    if not isfile(file_name):
        raise Exception(f"File {file_name} does not exist.")

    with open(file_name, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise Exception(exc)


def test_model_before_delete(title, model_short_name, model_class):
    model_exist = (
        model_class.query
        .filter(model_class.short_name == model_short_name)
        .one_or_none()
    )
    if not model_exist:
        print(f"{title:40s} {model_short_name:40s} : not found")
        return
    return model_exist
