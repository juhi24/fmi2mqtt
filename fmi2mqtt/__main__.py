# coding: utf-8
"""
"""
from paho.mqtt import publish
import fmi
from config import config

if __name__ == '__main__':
    topicfmt = 'fmi/{place}/{param}'
    weather = fmi.get_weather_simple(**config['query']).iloc[-1]
    for param, value in weather.iteritems():
        topic = topicfmt.format(place=config['query']['place'], param=param)
        publish.single('fmi/{place}/{param}', value,
                       hostname=config['mqtt']['host'], auth=config['mqtt'])