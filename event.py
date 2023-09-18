from time import time
import numpy as np

class Event:
    '''
    Encapsulates the data of a single pixel hit, specified by a set of two coordinates, a time coordinate, an Event ID, as well as status information, a layer ID and the number of total layers for verification of completeness of the data. 
    '''
    
    def __init__(self, event_id = None, layer_id = 0, total_layers = 1,  event_time=None, pixel_hit=None):
        '''
        Creates an event with all class members initialized to None if no arguments are given.
        The pixel hit is to be specified with a set of x- and y-coordinate. 
        An Event ID will be generated when not given.
        '''
        self.pixel_hit = pixel_hit
        try:
            if layer_id >= total_layers:
                raise ValueError
            self.layer_id = layer_id
            self.total_layers = total_layers
        except ValueError:
            print("Warning: Layer ID is larger than total number of layers.")
        if time is None:
            self.time = time()
        else:
            self.time = event_time
        
        if event_id is None:
            self.event_id = hash(time)
        else:
            self.event_id = event_id

        if pixel_hit is None:
            self.status = "no_hits"
        else:
            self.status = "pixel_hit"

    def __eq__(self, other):
        '''
        Method to determine whether two events are equal.
        '''
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
