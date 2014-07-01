class ApplianceSet(object):

    def __init__(self,instances):
        '''
        Initializes an appliance set given a list of instances.
        '''
        self.instances = instances
        self.make_dataframe()

    def add_instances(self,instances):
        '''
        Adds the list of appliances to the appliance set.
        '''
        self.instances += instances
        self.add_to_dataframe(instances)

    def add_to_dataframe(self,instances):
        '''
        Adds a new list of appliances to the dataframe.
        '''
        pass

    def get_dataframe(self):
        '''
        Returns the dataframe object representing the dataset.
        '''
        return self.df

    def make_dataframe(self):
        '''
        Makes a new dataframe of the appliance instances. Throws an exception if
        if the appliance instances have traces that don't align.
        '''
        pass

    def set_instances(self,instances):
        '''
        Replaces the old instances with the new list. Makes a new dataframe
        using those instances
        '''
        self.instances = instances
        self.make_dataframe()

    def top_k(self):
        '''
        Get top k energy-consuming appliances
        '''
        pass
