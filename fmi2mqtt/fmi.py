# coding: utf-8
"""
"""
import datetime
import pandas as pd
from os import environ
from lxml import etree
from owslib.wfs import WebFeatureService
from fmi2mqtt.config import config


def tz_local():
    """Local timezone"""
    return datetime.datetime.utcnow().astimezone().tzinfo


def starttime_str(minutes=20, **kws):
    """Start time string using current time with buffer"""
    now = datetime.datetime.utcnow()
    dt = datetime.timedelta(minutes=minutes, **kws)
    t_start = now-dt
    return t_start.isoformat(timespec='minutes')


def fmi_wfs(key=None):
    """FMI WebFeatureService"""
    try:
        key = key or config['fmi']['api_key']
    except KeyError:
        raise KeyError('FMI API key not configured.')
    url_wfs = 'http://data.fmi.fi/fmi-apikey/{}/wfs'.format(key)
    return WebFeatureService(url=url_wfs, version='2.0.0')


def weather_query_simple(t_start=None, **kws):
    """FMI stored query for weather observations in simple format"""
    t_start = t_start or starttime_str()
    storedQueryID = 'fmi::observations::weather::simple'
    storedQueryParams = dict(starttime=t_start, **kws)
    return fmi_wfs().getfeature(storedQueryID=storedQueryID,
                                storedQueryParams=storedQueryParams)


def parse_weather_simple(response):
    """parse FMI stored query for weather observations in simple format"""
    root = etree.fromstring(response.read().encode('utf8'))
    df = pd.DataFrame()
    for result in root.findall('wfs:member/BsWfs:BsWfsElement', root.nsmap):
        time = pd.Timestamp(result.find('BsWfs:Time', root.nsmap).text)
        name = result.find('BsWfs:ParameterName', root.nsmap).text
        value = float(result.find('BsWfs:ParameterValue', root.nsmap).text)
        df.loc[time, name] = value
    return df


def get_weather_simple(**kws):
    """FMI weather observations using stored query in simple format"""
    response = weather_query_simple(**kws)
    return parse_weather_simple(response)


def get_latest(param='t2m', **kws):
    """Get latest timestamp (local time) and weather observation as tuple."""
    latest = get_weather_simple(parameters=param, **kws).iloc[-1]
    timestamp = latest.name.tz_convert(tz_local())
    return timestamp, latest[param]



if __name__ == '__main__':
    #weather = get_weather_simple(place='kumpula', parameters='t2m,p_sea')
    pass


