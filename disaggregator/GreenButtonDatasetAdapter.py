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

from lxml import etree



def get_trace_from_xml(xml_filepath):
    '''
    This function returns a unique set of dates (corresponding to
    individual files) for a single device instance id
    '''
    schema_file = '../assets/schemas/espiDerived.xsd'
    with open(schema_file, 'r') as f:
        schema_root = etree.XML(f.read())
    schema = etree.XMLSchema(schema_root)
    xmlparser = etree.XMLParser(schema=schema)

    with open(xml_filepath,'r') as f:
        xml_string = f.read()

    if not _validate(xml_string):
        raise InvalidXMLError

    pass

def _validate(xml_string):
    try:
        etree.fromstring(xml_string, xmlparser)
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

        return '''Improperly formed XML file. Please make sure the file follows
            the green button specification. '''
