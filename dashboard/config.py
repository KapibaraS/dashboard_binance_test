import os
from pathlib import Path
from yaml import safe_load
from dashboard.schemas import config_schema

__all__ = ('BASE_DIR', 'config',)

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = (
        os.environ.get('CONFIG_PATH') or
        str(BASE_DIR.parent / 'configs/dev-docker.yml')
)

TEMPLATE_DIR = BASE_DIR / 'templates'


def get_config(path):
    with open(path) as stream:
        data = safe_load(stream)
        config_schema.check(data)
        return data


config = get_config(CONFIG_PATH)
