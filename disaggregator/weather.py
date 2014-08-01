"""
.. module:: weather
   :platform: Unix
   :synopsis: Contains utilities for obtaining weather data.

.. moduleauthor:: Phil Ngo <ngo.phil@gmail.com>
.. moduleauthor:: Miguel Perez <miguel@invalid.com>
.. moduleauthor:: Stephen Suffian <steve@invalid.com>
.. moduleauthor:: Sabina Tomkins <sabina@invalid.com>

"""
import urllib2
import json

def get_lat_lng_from_zip_code(zip_code,google_apis_key):
    '''
    Return a lat and long given a zip code. (Centroid, see google apis
    documentation)
    '''
    zip_code=zip_code.replace(' ','+')
    zip_code=zip_code.replace(',','%2C')
    f = urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address='+zip_code+'&key=' + google_apis_key)
    json_string = f.read()
    parsed_json_lat_lng = json.loads(json_string)
    lat=parsed_json_lat_lng['results'][0]['geometry']['location']['lat']
    lng=parsed_json_lat_lng['results'][0]['geometry']['location']['lng']
    return lat,lng
