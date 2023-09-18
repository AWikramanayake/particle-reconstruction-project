import detector
import particle
import matplotlib.pyplot as plt
import numpy as np
from random import random

particle_num = 1000
covariance_matrix = np.array([[1.2, 0.5], [0.5, 1.2]])

particles = []
for i in range(particle_num):
    phi = np.random.random() * 360
    theta = np.random.random() * 10
    particles.append(particle.Particle(phi=phi, theta=theta))

d = detector.Detector(30, 0)

pixel_hits = []

for p in particles:
    pixel_hits.append(d.detector_hit_no_event(p))

ph = np.array(pixel_hits)

# Plot particles
plt.plot(ph.T[0], ph.T[1], marker=".", linestyle="None")

# Plot detector
plt.vlines([0, 2000], 0, 2000)
plt.hlines([0, 2000], 0, 2000)

plt.xlim(-250, 2250)
plt.ylim(-250, 2250)
plt.gca().set_aspect('equal', adjustable='box')

plt.show()
