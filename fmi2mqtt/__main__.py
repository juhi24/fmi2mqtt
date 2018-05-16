# coding: utf-8
"""
"""
import time
from paho.mqtt import publish
from fmi2mqtt import fmi
from fmi2mqtt.config import config, get_place
from j24.server import GracefulKiller


def main():
    killer = GracefulKiller()
    while True:
        topicfmt = 'fmi/{place}/{param}'
        weather = fmi.get_weather_simple(**config['query']).iloc[-1]
        for param, value in weather.iteritems():
            topic = topicfmt.format(place=get_place(), param=param)
            print('published {}: {}'.format(topic, value))
            publish.single(topic, value, hostname=config['mqtt']['host'],
                           auth=config['mqtt'], retain=True)
        # check every 5 sec if process needs to be killed
        for i in range(60):
            if killer.kill_now:
                break
            time.sleep(5)
        else:
            continue
        break
    print('Stopped gracefully.')


if __name__ == '__main__':
    main()
