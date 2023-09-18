class DataWrapper:
    '''
    A simple container class for multiple events of the Event class. Can hold any number of events and any number of reconstructed paths.
    '''
    def __init__(self, list_of_events = [], reconstructed_paths = []):
        '''
        Initiates a container with a given list of events (Event class instances) and reconstructed paths (velocity vectors)
        '''
        self.event_container = list_of_events
        self.reconstructed_paths = reconstructed_paths

    def store_new_events(self,events):
        '''
        Adds new events to a DataWrapper. Can take a single event or a list of events as argument.
        '''
        if type(events) is list:
            self.event_container += events
        else:
            self.event_container.append(events)

    def store_new_paths(self,paths):
        '''
        Adds new reconstructed paths to a DataWrapper. Can take a single path or a list of paths as argument.
        '''
        if type(paths) is list:
            self.reconstructed_paths += paths
        else:
            self.reconstructed_paths.append(paths)

    def get_events_in_layer(self, layer):
        '''
        Returns a list of all events where the layer_id matches the layer argument. 
        '''
        output = []
        for event in self.event_container:
            if event.layer_id == layer:
                output.append(event)
        return output
        
