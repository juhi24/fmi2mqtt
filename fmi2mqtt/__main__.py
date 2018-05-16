# coding: utf-8
"""
"""
import time
from paho.mqtt import publish
import fmi
from fmi2mqtt.config import config, get_place
from j24.server import GracefulKiller


def main():
    killer = GracefulKiller()
    while True:
        topicfmt = 'fmi/{place}/{param}'
        weather = fmi.get_weather_simple(**config['query']).iloc[-1]
        for param, value in weather.iteritems():
            topic = topicfmt.format(place=get_place(), param=param)
            publish.single(topic, value, hostname=config['mqtt']['host'],
                           auth=config['mqtt'])
        if killer.kill_now:
            break
        time.sleep(300)
    print('Stopped gracefully.')


if __name__ == '__main__':
    main()
