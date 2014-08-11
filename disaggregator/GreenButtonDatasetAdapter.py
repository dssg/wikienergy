"""
.. module:: GreenButtonDatasetAdapter
   :platform: Unix
   :synopsis: Contains methods for importing data following the green button
     spec.

.. moduleauthor:: Phil Ngo <ngo.phil@gmail.com>
.. moduleauthor:: Miguel Perez <miguel@invalid.com>
.. moduleauthor:: Stephen Suffian <steve@invalid.com>
.. moduleauthor:: Sabina Tomkins <sabina.tomkins@gmail.com>


"""

from appliance import ApplianceTrace
from appliance import ApplianceInstance
from appliance import ApplianceSet
from appliance import ApplianceType
import utils

import sqlalchemy
import pandas as pd
import numpy as np

from xml.parsers.expat import ExpatError
from xml.dom import minidom
from lxml import etree

from datetime import datetime
import warnings
import os.path
import re

def get_trace(xml_string):
    '''
    Returns an ApplianceTrace representing the data in the XML file, which
    must conform to the GreenButtonXML format.
    '''
    # if not _validate(xml_string):
    #     raise InvalidXMLError

    try:
        xmldoc = minidom.parseString(xml_string)
        values = xmldoc.getElementsByTagName('value')
        datetimes = xmldoc.getElementsByTagName('start')
        # TODO - more intelligently handle assumption about duration -> freq
        frequency = int(xmldoc.getElementsByTagName('duration')[1]
                .childNodes[0].nodeValue)
        # remove first extra 'start' time
        datetimes.pop(0)
    except ExpatError:
        print "XML parsing error"

    # extrace values
    values = [v.childNodes[0].nodeValue for v in values]
    datetimes = [datetime.fromtimestamp(int(dt.childNodes[0].nodeValue))
                 for dt in datetimes]

    series = pd.Series(values,index=datetimes)
    metadata = {'source': 'GreenButtonXML'}
    trace = ApplianceTrace(series,metadata)

    # TODO - be more flexible
    # set sample rate
    if frequency == 60 * 60:
        trace = trace.resample('H')
    elif frequency == 60 * 30:
        trace = trace.resample('30T')
    elif frequency == 60 * 15:
        trace = trace.resample('15T')
    elif frequency == 60:
        trace = trace.resample('T')

    return trace

def get_zipcode(xml_string):
    '''
    Returns an ApplianceTrace representing the data in the XML file, which
    must conform to the GreenButtonXML format.
    '''
    try:
        xmldoc = minidom.parseString(xml_string)
        entry=xmldoc.getElementsByTagName('entry')[0]
        address = entry.getElementsByTagName('title')[0].childNodes[0].nodeValue
        # find a zipcode
        try:
            return re.findall(r"\s((\d{5})([-\s]\d{4})?)\s*$", address)[0][1]
        except IndexError:
            warnings.warn("No zipcode found (IndexError), using 60605")
            return "60605"
    except ExpatError:
        warnings.warn("No zipcode found (ExpatError), using 60604")
        return "60604"

def _validate(xml_string):
    '''
    Validates that the XML is in proper GB format
    '''
    # TODO - WARNING this does not actually validate anything right now!!!
    # Actually it would if you uncommented the etree.fromstring call, but it
    # is too strict
    schema_file = os.path.abspath(os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'assets','schemas','espiDerived.xsd'))
    with open(schema_file, 'r') as f:
        schema_root = etree.XML(f.read())
    schema = etree.XMLSchema(schema_root)
    xmlparser = etree.XMLParser(schema=schema)

    try:
        # TODO make the validation work
        # etree.fromstring(xml_string, xmlparser)
        return True
    except:
        return False


class InvalidXMLError(Exception):
    """

    Exception raised for errors in the xml format of the data.

    """
    def __init__(self):
        pass

    def __str__(self):

        return '''Improperly formed GreenButton XML file. Please make sure the
            file follows the green button xsd specification. '''
