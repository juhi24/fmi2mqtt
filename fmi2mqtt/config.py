# coding: utf-8
"""
"""
import configparser


global_file = '/etc/fmi2mqtt.conf'
config = configparser.ConfigParser()
config.read(global_file)


def get_place(config=config):
    keys = [k for k in config['query'].keys()]
    keys.remove('parameters')
    return config['query'][keys[0]]
