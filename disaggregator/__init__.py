"""
.. module:: disaggregator
   :platform: Unix
   :synopsis: A package for performing disaggregation on smart meter data.

.. moduleauthor:: Phil Ngo <ngo.phil@gmail.com>
.. moduleauthor:: Miguel Perez <miguel.a.perez4@gmail.com>
.. moduleauthor:: Stephen Suffian <stephen.suffian@gmail.com>
.. moduleauthor:: Sabina Tomkins <sabina.tomkins@gmail.com>
"""

# TODO remove these
from appliance import *
from utils import *

import evaluation_metrics
import PecanStreetDatasetAdapter
import OakParkDatasetAdapter
from TracebaseDatasetAdapter import TracebaseDatasetAdapter
import GreenButtonDatasetAdapter
import utils
import appliance
import fhmm
import generate
import weather
