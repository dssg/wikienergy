import pandas as pd
import numpy as np
import sqlalchemy

class Dataset(object):
    def __init__(self):
        self.df = None
        self.source = None
