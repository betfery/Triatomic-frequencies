"""To be added

"""

import os
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D


def parseOutputs(filepath):
    """Reads the file, returns energy and geometry

    """

    file = filepath.split('/')[-1]
    r = file.split('r')[1].split('theta')[0]
    theta = file.split('r')[1].split('theta')[1].split('.out')[0]
    f = open(filepath, 'r')
    energy = 0
    for line in f:
        if 'SCF Done:' in line:
            energy = line.split()[4]
    f.close()

    return (float(r), float(theta), float(energy))


def surfacePlot(xyzPoints):
    """Plots 3D plot given list of xyz points

    """

    ax = plt.axes(projection='3d')
    ax.plot_trisurf(xyzPoints[0],
                    xyzPoints[1],
                    xyzPoints[2])
    plt.show()


def main():
    PATH = './H2Ooutfiles/'
    xyz = ([], [], [])
    for file in os.listdir(PATH):
        filepath = PATH + file
        points = parseOutputs(filepath)
        xyz[0].append(points[0])
        xyz[1].append(points[1])
        xyz[2].append(points[2])
    surfacePlot(xyz)


if __name__ == '__main__':
    main()
