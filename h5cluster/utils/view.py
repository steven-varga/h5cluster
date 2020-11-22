# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca

class dict_view(object):
        ''' converts dictionary to object with attributes

        Args:
            object (dict): dictionary with parsed program arguments
        '''
        def __init__(self, dictionary: dict):
            self.__dict__ = dictionary
