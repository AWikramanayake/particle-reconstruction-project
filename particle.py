from random import random
from time import time
import numpy as np
from scipy import constants

class Particle:
    '''
    Particle class
    '''
    def __init__(self, phi=None, theta=None, normal_distribution = True, covariance_matrix = np.array([[1.2,0.5],[0.5,1.2]]), speed=constants.c*100, creation_time=0, position=np.zeros(3)):
        '''
        Create timestamp and assign random theta and phi. If angles are given, they will be used. Else, if normal_distribution == True (default), they will be generated from a normal distribution with covariance matrix covariance_matrix (new particle source); if normal_distribution == False they will be sampled from a uniform distribution with theta<=10 (old particle source).
        '''
        self.creation_time = creation_time
        if (phi is not None) and (theta is not None):
            self.phi = np.radians(phi)
            self.theta = np.radians(theta)
        elif normal_distribution:
            normal_sample = np.random.multivariate_normal([0,0],covariance_matrix)
            self.phi = np.arctan2(normal_sample[1],normal_sample[0])
            self.theta = np.arctan2(np.linalg.norm(normal_sample),10)
        else:
            self.phi = np.radians(random()*360)
            self.theta = np.radians(random()*10)
        self.speed = speed
        self.vector = self.vectorize(speed, self.phi, self.theta)
        self.position = position

    def trajectory(self, z: float) -> np.ndarray:
        """
        trajectory function of particle
        starting from specified position in  specified direction
        as a function of z

        :param z:
        :return: x,y vector at postion z
        """

        x_y = (z - self.position[2]) / self.vector[2] * self.vector[0:2] + self.position[0:2]
        return x_y

    def time_traveled(self, z: float) -> np.ndarray:
        """
        computes travel time of particle until reaching specified z value

        :param z:
        :return: time traveled
        """
        time_traveled = (z - self.position[2]) / self.vector[2]
        return time_traveled

    @staticmethod
    def vectorize(length, phi, theta):
        """
        Returns a 3D vector of the particle. Lenght of the vector is defined by
        the distance travelled in one second
        """
        r = length
        x = r * np.cos(phi) * np.sin(theta)
        y = r * np.sin(phi) *np.sin(theta)
        z = r * np.cos(theta)
        return np.array([x,y,z])

