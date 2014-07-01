class ApplianceType(object):

    def __init__(self, instances):
        '''
        Initialize a type object with a list of instances. (Check for
        uniqueness?)
        '''
        # TODO Check for uniqueness?
        self.instances = instances

    def add_instances(self,instances):
        '''
        Add instances to the list of instances. (Check for uniqueness?)
        '''
        # TODO Check for uniqueness?
        self.instances += instances

    def get_instances(self):
        '''
        Returns the list of appliance instances which are members of this type.
        '''
        return self.instances

    def set_instances(self,instances):
        '''
        Replaces the old list of instances with the new set of instances.
        (Check for uniqueness?)
        '''
        # TODO Check for uniqueness?
        self.instances = instances

