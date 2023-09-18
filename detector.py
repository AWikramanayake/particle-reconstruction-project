import numpy as np
from time import time
from particle import Particle
from datawrapper import DataWrapper
from event import Event


class Detector:
    '''
    Class which keeps data for the detector
    '''
    def __init__(self, z, detector_id, size=np.array([20, 20]), pixels=np.array([2000, 2000])):
        self.z = z
        self.detector_id = detector_id
        self.pos = np.array([-size[0]/2, -size[1]/2, z]) # position of top left corner of sensor
        self.size = size
        self.pixels = pixels
        self.hits = [] # hits are given as a tuple (x, y, timestamp)


    def pixel_from_pos(self, pos):
        '''
        Returns the pixel index on a given position (2d array [x,y])
        Pixels start top left
        Pixel index is given by the position - position of top left corner (self.pos) divided by pixel pitch (= size/pixels)
        '''
        pixel_x = np.floor( (pos[0] - self.pos[0]) / (self.size[0] / self.pixels[0]))
        pixel_y = np.floor( (pos[1] - self.pos[1]) / (self.size[1] / self.pixels[1]))

        # If calculated pixel is outside of sensor, raise an error
        #if pixel_x > self.pixels[0] or pixel_y > self.pixels[1]:
            #raise Exception("Position outside of sensor")

        return np.array([pixel_x, pixel_y])

    def detector_hit(self, particle):
        hit_time = particle.time_traveled(self.pos[2])
        hit = particle.trajectory(self.pos[2])
        pixel_id = self.pixel_from_pos(hit)

        event = Event(event_id=hash(hit_time),
                      event_time=hit_time,
                      layer_id=self.layer_id,
                      pixel_hit=pixel_id)

        return event

    def detector_hit_no_event(self, particle):
        hit_time = particle.time_traveled(self.pos[2])
        hit = particle.trajectory(self.pos[2])
        pixel_id = self.pixel_from_pos(hit)

        return pixel_id


class DetectionSetup:
    def __init__(self, detectors: [Detector]):
        """
        Container for all Detectors in setup

        :param detectors:
        """
        self.detectors = detectors
        self.n_detectors = len(detectors)

    def detector_hits(self, particle: Particle):
        """
        calculates the hit of particle with every detector in setup

        :param particle:
        :return: DataWrapper containg all hit events
        """
        data = DataWrapper()

        for detector in self.detectors:
            event = detector.detector_hit(particle)
            data.store_new_events(event)

        return data

    @classmethod
    def from_positions(cls, z_positions: [float], size=np.array([20, 20]), pixels=np.array([2000, 2000])):
        detectors = [Detector(z, detector_id, size, pixels) for z, detector_id in zip(z_positions, range(len(z_positions)))]
        return cls(detectors)

# TODO add detection algorithm
# activated pixels + time when activated (in event time scale) (from simulation class)
# 
# DONE add method position from pixel (index=[])
#
# add algorithm + method pixel from position (from simulation class)