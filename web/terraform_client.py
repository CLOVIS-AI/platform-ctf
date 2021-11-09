import os
import re
from subprocess import run, PIPE, check_output

from flask import current_app


class TerraformClient:
    """Terraform client class that allows to apply, plan and destroy"""

    def __init__(self, instance_id, variables=None):
        if variables is None:
            variables = {}
        self.terraform_binary = check_output(["which", "terraform"]).decode().strip()
        self.instance_id = instance_id
        self.output = {}
        self.variables = variables
        self.variables["instance_id"] = instance_id
        self.planned = False
        self.working_directory = os.path.join(
            os.getcwd(), f"{current_app.config['BASE_INSTANCE_DATA']}/{instance_id}/"
        )

        self.run_command([self.terraform_binary, "init", "-no-color"])

    def plan(self):
        command = [self.terraform_binary, "plan", "--out", "planpython.out", "-no-color"]
        result = self.run_command(command, with_vars=True)
        self.check_created_names_are_correct(result.stdout)
        self.planned = True

    def check_created_names_are_correct(self, plan_output):
        names = re.findall(r'\+ name[ ]+= "(?P<name>.*)"', plan_output)
        for name in names:
            if "vCenter" in name or not (
                    name.startswith("clonevm_" + str(self.instance_id) + "_")
                    or name.startswith("clonesw_" + str(self.instance_id) + "_")
                    or name.startswith("clonepg_" + str(self.instance_id) + "_")
                    or name.startswith("docker_" + str(self.instance_id) + "_")
            ):
                raise TerraformError("Resource name are not valid")

    def apply(self):
        if not self.planned:
            raise TerraformError("Plan must be run before apply")

        command = [self.terraform_binary, "apply", "planpython.out", "-no-color"]
        result = self.run_command(command)
        self.parse_apply_output(result.stdout)

    def parse_apply_output(self, apply_output):
        if "Outputs" in apply_output:
            outputs_before_parse = apply_output.split("Outputs")[1]
            found = re.findall(r"([^=\n]+) = ([^\n]+)", outputs_before_parse)
            for key, value in found:
                self.output[key] = value

    def destroy(self):
        command = [self.terraform_binary, "destroy", "-auto-approve", "-no-color"]
        self.run_command(command, with_vars=True)
        self.remove_temporary_files()

    def remove_temporary_files(self):
        for f in ["terraform.tfstate", "terraform.tfstate.backup"]:
            file_path = os.path.join(self.working_directory, f)
            if os.path.exists(file_path):
                os.remove(file_path)

    def format_variables(self, variables):
        variable_array = []
        for variable in [
            str(key) + "=" + str(value) for key, value in variables.items()
        ]:
            variable_array.append("-var")
            variable_array.append(variable)
        return variable_array

    def run_command(self, command, with_vars=False):
        if with_vars:
            formatted_variables = self.format_variables(self.variables)
            command.extend(formatted_variables)
        return run(
            command,
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf-8",
            cwd=self.working_directory,
            check=True,
        )


class TerraformError(Exception):
    pass
