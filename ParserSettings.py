import configparser
import os


def create_config(path):
    config = configparser.ConfigParser()
    config.add_section('Settings')
    config.set('Settings', 'length_base', '80')
    config.set('Settings', 'punctuation', '(".", "!", "?")')

    with open(path, 'w') as config_file:
        config.write(config_file)


def get_config(path):
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_setting(path, section, setting):
    config = get_config(path)
    value = config.get(section, setting)
    return value

