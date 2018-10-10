"""To be added

"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D


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


def surfacePlot(X, Y, Z):
    """Plots 3D plot given list of xyz points

    Adds lines to show the potential well along r and theta.

    """
    tx, ty, tz, rx, ry, rz = fitQuadratic(X, Y, Z)

    ax = plt.axes(projection='3d')
    ax.plot(tx, ty, tz)
    ax.plot(rx, ry, rz)

    ax.set_xlabel('r / Angstroms')
    ax.set_ylabel('Theta / degrees')
    ax.set_zlabel('Energy / Hartree')
    ax.set_title('Potential Energy Surface')
    plt.tight_layout()

    ax.plot_trisurf(X, Y, Z,
                    cmap=cm.viridis)

#    plt.axis([tx[0]-0.15, tx[-1]+0.15,
#           ty[0], ty[-1]])

    plt.show()


def fitQuadratic(X, Y, Z):
    """Fits a quadratic potential well around minima of given data


    """
    n = 0
    while X[n] == X[0]: n = n + 1

    minZ, minPos = min(Z), np.argmin(Z)
    minX, minY = X[minPos], Y[minPos]
    print(f'The optimized geometry is at ({minX},{minY}) with E={minZ:.3e}')

    xr = X[minPos - n::n]
    xr = xr[:3]
    xr[:] = [x - minX for x in xr]
    zr = Z[minPos - n::n]
    zr = zr[:3]
    d = np.polynomial.polynomial.polyfit(xr, zr, np.arange(0, 2, 1))


    yt = Y[minPos-5:minPos+5]
    yt[:] = [y - minY for y in yt]
    zt = Z[minPos-5:minPos+5]
    ax = plt.axes()
    p = np.polynomial.polynomial.polyfit(yt, zt, np.arange(0, 2, 1))
    p[1] = -p[1]

    xR = np.linspace(xr[0], xr[-1], 100) + minX
    yR = minY * np.ones(100)
    zR = d[1]*(xR-minX)*(xR-minX) + d[0]

    xT = minX * np.ones(100)
    yT = np.linspace(yt[0], yt[-1], 100) + minY
    zT = p[1]*(yT-minY)*(yT-minY) + p[0]
    ax.plot(yt, zt)
    ax.plot(yT-minY, zT)

    plt.show()

    print('Potential for constant theta is '
          f'E = {d[1] :+.3e}(t-t0)^2 {d[0] :+.3e} ')
    print('Potential for constant r is '
          f'E = {p[1] :+.3e}(r-r0)^2 {p[0] :+.3e} ')

    return xT, yT, zT, xR, yR, zR


def main():
    PATH = './H2Ooutfiles/'
    xyz = ([], [], [])
    for file in os.listdir(PATH):
        filepath = PATH + file
        points = parseOutputs(filepath)
        xyz[0].append(points[0])
        xyz[1].append(points[1])
        xyz[2].append(points[2])
    surfacePlot(*xyz)

if __name__ == '__main__':
    main()
