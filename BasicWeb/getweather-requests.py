#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :
'''
Get weather from weather underground
Created on 11/22/2014

@author: carlesm
'''

import sys
import requests
import bs4

api_key = None  # If assigned won't read argv[1]

location = 'Lleida'
response_format = 'xml'


class WeatherClient(object):

    """Will access wunderground to gather weather information

    Provides access to wunderground API
    (http://www.wunderground.com/weather/api)

    Provides methods:
        almanac
    """

    url_base = 'http://api.wunderground.com/api/'
    url_services = {
        "almanac": "/almanac/q/CA/"
    }

    def __init__(self, apikey):
        super(WeatherClient, self).__init__()
        self.api_key = api_key

    def almanac(self, location):
        """
        Accesses wunderground almanac information for the given location
        """
        resp_format = "xml"
        url = WeatherClient.url_base + api_key + \
            WeatherClient.url_services[
                "almanac"] + location + "." + resp_format
        r = requests.get(url)

        return_response = {}
        soup = bs4.BeautifulSoup(r.text)
        # We use find (not find_all) as there is only one, if
        # we used find_all the response would be iterable
        temp_high = soup.find("temp_high")
        th_normal = temp_high.find("normal")
        thnc = th_normal.find("c").text
        th_record = temp_high.find("record")
        thrc = th_record.find("c").text
        thry = temp_high.find("recordyear").text

        return_response["high"] = {}
        return_response["high"]["normal"] = thnc
        return_response["high"]["record"] = thrc
        return_response["high"]["year"] = thry

        temp_low = soup.find("temp_low")
        tl_normal = temp_low.find("normal")
        tlnc = tl_normal.find("c").text
        tl_record = temp_low.find("record")
        tlrc = tl_record.find("c").text
        tlry = temp_low.find("recordyear").text
        return_response["low"] = {}
        return_response["low"]["normal"] = tlnc
        return_response["low"]["record"] = tlrc
        return_response["low"]["year"] = tlry

        return return_response


def print_almanac(almanac):
    """
    Prints an almanac received as a dict
    """
    print "High Temperatures:"
    print "Average on this date", almanac["high"]["normal"]
    print "Record on this date %s (%s) " % \
        (almanac["high"]["record"],
            almanac["high"]["year"])
    print "Low Temperatures:"
    print "Average on this date", almanac["low"]["normal"]
    print "Record on this date %s (%s) " % \
        (almanac["low"]["record"],
            almanac["low"]["year"])


if __name__ == "__main__":
    if not api_key:
        try:
            api_key = sys.argv[1]
        except IndexError:
            print "Must provide api key in code or cmdline arg"

    weatherclient = WeatherClient(api_key)
    print_almanac(weatherclient.almanac("Lleida"))
