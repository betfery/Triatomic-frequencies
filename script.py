"""To be added

"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def parser(filepath):
    """Reads the file, returns energy and geometry

    """

    file = filepath.split('/')[-1]
    r = file.split('r')[1].split('theta')[0]
    theta = file.split('r')[1].split('theta')[1].split('.out')[0]
    f = open(filepath, 'r')
    energy = 0
    for line in f:
        if 'SCF Done:' in line:
            l = line.split()
            energy = l[4]
    f.close()

    return (float(r), float(theta), float(energy))

def surfacePlot(xyzPoints):
    """Plots 3D plot given list of xyz points

    """
    x = xyzPoints[0]
    y = xyzPoints[1]
    z = xyzPoints[2]
    Xi = np.linspace(min(x), max(x), len(set(x)))
    Yi = np.linspace(min(y), max(y), len(set(y)))
    X, Y = np.meshgrid(Xi, Yi)
    Z = np.array(z).reshape(X.shape)
    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1)
    plt.show()

def main():
    PATH = './H2Ooutfiles/'
    xyz=([],[],[])
    for file in os.listdir(PATH):
        filepath = PATH + file
        points = parser(filepath)
        xyz[0].append(points[0])
        xyz[1].append(points[1])
        xyz[2].append(points[2])
    surfacePlot(xyz)

if __name__ == '__main__':
    main()
