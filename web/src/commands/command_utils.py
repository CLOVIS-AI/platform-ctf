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
