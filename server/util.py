import datetime
import os

import yaml


def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_config(env, config_resource):
    config_dict = yaml.load(config_resource, Loader=yaml.Loader)
    try:
        config_dict = config_dict[env]
    except KeyError:
        raise KeyError(f"Invalid ENV value '{env}' should be in {list(config_dict.keys())}")
    for key, value in os.environ.items():
        if key.startswith('FLASK_'):
            config_dict[key[6:]] = value
    for key, value in config_dict.items():
        if isinstance(value, str) and value.startswith('env:'):
            config_dict[key] = os.environ[value[4:]]
    return config_dict


def date_to_ordinal(dt):
    if dt is None:
        return None
    elif isinstance(dt, datetime.datetime):
        return dt.toordinal()
    else:
        return 'unknown'
