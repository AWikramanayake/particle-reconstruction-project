# This file will try to run our project

# Import stuff
from particle import Particle
from detector import Detector, DetectionSetup
from reconstruction import reconstruct
from reconstruction import bestFit
import numpy as np
import xlwt

book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")
incr = 1

sheet1.write(0, 0, "Error 1")
sheet1.write(0, 1, "Error 2")
sheet1.write(0, 2, "Error 3")
sheet1.write(0, 3, "Error 4")
sheet1.write(0, 4, "Error 5")

n_hits = 10

for b in range(n_hits):

    # Create a particle 
    p = Particle()
    print("Created a particle with angles phi={} and theta={}".format(np.degrees(p.phi), np.degrees(p.theta)))

    trueVector = np.array([np.sin(p.theta) * np.cos(p.phi),
                           np.sin(p.theta) * np.sin(p.phi),
                           np.cos(p.theta)])

    # Create 5 detectors and pipe them to DetectionSetup
    detectors = []
    for i in range(5):
        z = 30 + 5 * i  # z is 30cm plus 5cm detector spacing
        detectors.append(Detector(z, i))

    # feed the particle to the detection setup and calculate hits
    hits = []
    print("\nDetector hits:")
    for d in detectors:
        print(d.detector_hit_no_event(p))
        hits.append([*d.detector_hit_no_event(p), d.z])

    print("\nParticle vector is:")
    print(trueVector)

    # feed our hits to the reconstruction algorithm
    #
    # right now i used [pixel_x, pixel_y, z_pos], where pixel_x / pixel_y are the indexes of the hit pixels
    # and z_pos is the z_position of the detector (in cm)
    rec = reconstruct(np.array(hits))
    recData = bestFit(rec)

    recHits = np.concatenate(([recData[3:6] - (10 / recData[2]) * (recData[0:3])],
                              [recData[3:6] - (5 / recData[2]) * (recData[0:3])],
                              [recData[3:6]],
                              [recData[3:6] + (5 / recData[2]) * (recData[0:3])],
                              [recData[3:6] + (10 / recData[2]) * (recData[0:3])]))

    trueHits = np.concatenate(([np.zeros(3) + (30 / trueVector[2]) * (trueVector[0:3])],
                               [np.zeros(3) + (35 / trueVector[2]) * (trueVector[0:3])],
                               [np.zeros(3) + (40 / trueVector[2]) * (trueVector[0:3])],
                               [np.zeros(3) + (45 / trueVector[2]) * (trueVector[0:3])],
                               [np.zeros(3) + (50 / trueVector[2]) * (trueVector[0:3])]))

    hitErrors = np.array([np.sqrt(((recHits[0][0] - trueHits[0][0]) ** 2) + (recHits[0][1] - trueHits[0][1]) ** 2),
                          np.sqrt(((recHits[1][0] - trueHits[1][0]) ** 2) + (recHits[1][1] - trueHits[1][1]) ** 2),
                          np.sqrt(((recHits[2][0] - trueHits[2][0]) ** 2) + (recHits[2][1] - trueHits[2][1]) ** 2),
                          np.sqrt(((recHits[3][0] - trueHits[3][0]) ** 2) + (recHits[3][1] - trueHits[3][1]) ** 2),
                          np.sqrt(((recHits[4][0] - trueHits[4][0]) ** 2) + (recHits[4][1] - trueHits[4][1]) ** 2)])

    print("\nThe true hit locations are:")
    print(trueHits)
    print("\nThe reconstructed hit locations are:")
    print(recHits)
    print("\nThe errors in the hits at each detector are:")
    print(hitErrors)
    print("\n \n")

    sheet1.write(incr, 0, hitErrors[0])
    sheet1.write(incr, 1, hitErrors[1])
    sheet1.write(incr, 2, hitErrors[2])
    sheet1.write(incr, 3, hitErrors[3])
    sheet1.write(incr, 4, hitErrors[4])

    incr += 1

book.save("trial.xls")
print("results saved to trial.xls")
