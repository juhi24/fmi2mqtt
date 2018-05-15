# coding: utf-8
"""
"""
import configparser


global_file = '/etc/fmi2mqtt.conf'
config = configparser.ConfigParser()
config.read(global_file)
