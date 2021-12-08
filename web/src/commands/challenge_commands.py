from os import listdir, access, X_OK
from os.path import join, isfile
from random import randrange, choice
from subprocess import CalledProcessError, check_call
from .command_utils import safe_open_file, save_new_model, test_model_before_delete
import click
import yaml
from flask import current_app
from flask.cli import AppGroup

from src.models import (
    Challenge,
    ChallengeStep,
    ChallengeSection,
    ChallengeResource,
)

challenge_cli = AppGroup("challenge")


# region Commands related to import

@challenge_cli.command("import")
@click.option("-a", "--all", "_all", is_flag=True)
@click.option("-c", "--challenge", "short_name")
@click.option("-f", "--force", is_flag=True)
def import_challenge_command(_all, short_name, force):
    if _all:
        import_all_challenges(force_reimport=force)
    elif short_name:
        import_challenge(short_name, force_reimport=force)


def import_all_challenges(force_reimport=False):
    """Imports all the challenges present in the challenges folder and absent from the database."""
    for challenge_short_name in listdir(current_app.config["CHALLENGE_DIR"]):
        try:
            import_challenge(challenge_short_name, force_reimport=force_reimport)
        except (Exception,):
            pass


def import_challenge(challenge_short_name, force_reimport=False):
    """Imports the challenge named `short_name` into the database."""
    challenge_yaml_file = join(
        current_app.config["CHALLENGE_DIR"], challenge_short_name, "challenge.yml"
    )
    if not isfile(challenge_yaml_file):
        print(f'File "{challenge_yaml_file}" not found.')
        return

    already_imported = (
        Challenge.query.filter(Challenge.short_name == challenge_short_name).one_or_none()
    )

    if already_imported:
        if force_reimport:
            reload_challenge_from_dir(challenge_short_name, already_imported)
        else:
            print(f"Challenge {challenge_short_name:40s} : already imported")
    else:
        load_challenge_from_dir(challenge_short_name)


def load_challenge_from_dir(challenge_short_name):
    try:
        data = load_challenge_yaml_from_dir(challenge_short_name)
        challenge = load_challenge_from_dict(data)
        load_resource_from_dict(data, challenge)
        load_sections_from_dict(data, challenge)
        challenge.save()
        print(f"Challenge {challenge_short_name:40s}: imported")
    except Exception as e:
        print(f"Challenge {challenge_short_name:40s}: {e}")


def load_challenge_from_dict(data):
    if "challenge" in data:
        return Challenge(**data["challenge"]).save()
    raise FileNotFoundError("No `challenge` key in yaml file.")


def load_resource_from_dict(data, challenge):
    if "resource" in data:
        challenge.resource = ChallengeResource(**data["resource"]).save()
        challenge.save()


def load_sections_from_dict(data, challenge):
    if "sections" in data:
        challenge.sections = [
            load_section_from_dict(order, section_data)
            for order, section_data in enumerate(data["sections"])
        ]
    else:
        section = ChallengeSection(title=None, description=None, order=0)
        challenge.sections = [section]
        section.steps = [
            load_step_from_dict(order, step_data)
            for order, step_data in enumerate(data["steps"])
        ]


def load_section_from_dict(order, section_data):
    section = ChallengeSection(**section_data["section"], order=order)
    if "steps" in section_data:
        section.steps = [
            load_step_from_dict(order, step_data)
            for order, step_data in enumerate(section_data["steps"])
        ]
    else:
        section.steps = [
            ChallengeStep(
                description="Click on the following button to complete this section",
                validation_type="fakevalidation",
                validation_arg="",
                points=0,
            )
        ]
    return section


def load_step_from_dict(order, step_data):
    return ChallengeStep(**step_data, order=order)


def reload_challenge_from_dir(challenge_short_name, challenge):
    data = load_challenge_yaml_from_dir(challenge_short_name)

    challenge.update(**data["challenge"])

    for step, step_data in zip(challenge.steps, data["steps"]):
        step.update(**step_data)

    print(f"Challenge {challenge_short_name:40s}: reimported")


def load_challenge_yaml_from_dir(challenge):
    from src.commands.command_utils import safe_open_file
    description_file = join(
        current_app.config["CHALLENGE_DIR"], challenge, "challenge.yml"
    )
    try:
        return safe_open_file(description_file)
    except Exception as e:
        raise Exception(e)


# endregion
# region List of challenges

@challenge_cli.command("list")
def list_challenges_command():
    for challenge in Challenge.query:
        print(f"- {challenge.short_name}")


# endregion
# region Create challenges

@challenge_cli.command("create")
@click.option("-n", "--number", default=1)
def create_challenge_command(number):
    """Create `n` random challenges."""
    for _ in range(number):
        create_random_challenge()
    print(f"Created {number} challenges.")


def create_random_challenge():
    from src.commands.command_utils import save_new_model
    CATEGORIES = ["Reverse", "Crypto", "Web", "Pwn", "Forensic", "SCENARIO"]

    new_challenge = Challenge(
        name="Random chall {}",
        short_name="random_chall_{}",
        description="Ce challenge est un challenge généré aléatoirement.\n",
        category=choice(CATEGORIES),
    )

    new_challenge.sections = [create_random_section() for _ in range(2)]
    # Using the challenge id to uniquify the challenge name and short_name
    save_new_model(new_challenge)


def create_random_section():
    return ChallengeSection(
        title="Title",
        description="Description",
        steps=[create_random_step() for _ in range(3)],
    )


def create_random_step():
    return ChallengeStep(
        description="Quel est le mot de passe de ce challenge ? C'est <b>random_flag</b>",
        validation_type="string",
        validation_arg="random_flag",
        points=randrange(1, 15 * 100),
    )


# endregion
# region Deletion

@challenge_cli.command("delete")
@click.option("-a", "--all", "_all", is_flag=True)
@click.option("-c", "--challenge", "short_name")
def delete_challenge_command(_all, short_name):
    from src.commands.command_utils import test_model_before_delete
    if _all:
        delete_all_challenges()
    elif short_name:
        challenge = test_model_before_delete("Challenge", short_name, Challenge)
        if challenge:
            delete_challenge(challenge)


def delete_all_challenges():
    for challenge in Challenge.query:
        delete_challenge(challenge)


def delete_challenge(challenge):
    challenge.delete()
    print(f"Challenge {challenge.short_name:40s}: deleted")


# endregion
# region Check

@challenge_cli.command("check")
@click.option("-a", "--all", "_all", is_flag=True)
@click.option("-c", "--challenge", "challenge_short_name")
def check_challenge_command(_all, challenge_short_name):
    if _all:
        check_all_challenges()
    elif challenge_short_name:
        check_challenge(challenge_short_name)


def check_all_challenges():
    return all(
        check_challenge(challenge_short_name)
        for challenge_short_name in listdir(current_app.config["CHALLENGE_DIR"])
    )


def check_challenge(challenge_short_name):
    return check_challenge_yaml(challenge_short_name) and check_challenge_build(
        challenge_short_name
    )


def check_challenge_yaml(challenge_short_name):
    yaml_filename = join(
        current_app.config["CHALLENGE_DIR"], challenge_short_name, "challenge.yml"
    )

    return check_challenge_yaml_file(yaml_filename) and check_challenge_yaml_content(
        yaml_filename
    )


def check_challenge_yaml_file(yaml_filename):
    if not isfile(yaml_filename):
        print(f"{yaml_filename:40s}: not found")
        return False

    with open(yaml_filename, "r") as stream:
        try:
            yaml.safe_load(stream)
        except yaml.YAMLError:
            print(f"Exception during the load of {yaml_filename}")
            return False

    return True


def check_challenge_yaml_content(yaml_filename):
    with open(yaml_filename, "r") as stream:
        data = yaml.safe_load(stream)

    try:
        Challenge(**data["challenge"])
    except TypeError as e:
        print("{:40s}: {}".format(yaml_filename, e))
        return False

    return True


def check_challenge_build(challenge_short_name):
    build_filename = join(
        current_app.config["CHALLENGE_DIR"], challenge_short_name, "build", "build.sh"
    )

    if not access(build_filename, X_OK):
        print("{:40s}: is not executable".format(build_filename))
        return False

    return True


# endregion
# region Build

@challenge_cli.command("build")
@click.option("-a", "--all", "_all", is_flag=True)
@click.option("-c", "--challenge", "challenge_short_name")
def build_challenge_command(_all, challenge_short_name):
    if _all:
        build_all_challenges()
    elif challenge_short_name:
        build_challenge(challenge_short_name)


def build_all_challenges():
    for challenge in Challenge.query:
        build_challenge(challenge.short_name)


def build_challenge(challenge_short_name):
    check_challenge(challenge_short_name)

    build_script = join(
        current_app.config["CHALLENGE_DIR"], challenge_short_name, "build", "build.sh"
    )
    try:
        check_call(build_script)
        print(f"Challenge {challenge_short_name:40.40s}: built")
    except FileNotFoundError:
        print(f"Challenge {challenge_short_name:40.40s}: no build script")
    except CalledProcessError:
        print(f"Challenge {challenge_short_name:40.40s}: build failed")
    except Exception as e:
        print(type(e), e)

# endregion
