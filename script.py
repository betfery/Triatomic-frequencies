"""To be added

"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
# from mpl_toolkits.mplot3d import Axes3D

Const = {'m_u': 1.66054e-27,
         'Hartree': 4.35974e-18}
validate = True


def parseOutputs(filepath):
    """Reads the file, returns energy from file and geometry from name.

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

    return float(r), float(theta), float(energy)


def surfacePlot(X, Y, Z):
    """Plots 3D plot given list of xyz points

    Adds lines to show the potential well along r and theta.
    """

    tx, ty, tz, rx, ry, rz = fitQuadratic(X, Y, Z, validate)

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

    plt.show()


def fitQuadratic(X, Y, Z, validate=True):
    """Fits a quadratic potential well around minima of given data

    Produces two graphs, along each axis, to validate the fit.
    """
    n = 0  # determines the offset for r's
    while X[n] == X[0]:
        n = n + 1

    minZ, minPos = min(Z), np.argmin(Z)
    minX, minY = X[minPos], Y[minPos]

    xr = X[minPos - 3*n::n]
    xr = xr[:7]
    zr = Z[minPos - 3*n::n]
    zr = zr[:7]
    d = np.polyfit(xr, zr, 2)

    yt = Y[minPos-5:minPos+5]
    zt = Z[minPos-5:minPos+5]
    p = np.polyfit(yt, zt, 2)

    xR = np.linspace(xr[0], xr[-1], 100)
    yR = minY * np.ones(100)
    zR = d[0]*xR*xR + d[1]*xR + d[2]

    xT = minX * np.ones(100)
    yT = np.linspace(yt[0], yt[-1], 100)
    zT = p[0]*yT*yT + p[1]*yT + p[2]

    if validate:
        plt.subplot(2, 1, 1)
        plt.plot(xr, zr, 'o-')
        plt.plot(xR, zR)
        plt.title('Potential wells along axis')
        plt.ylabel('Along theta axis')
        plt.xlabel('r')
        plt.tight_layout()

        plt.subplot(2, 1, 2)
        plt.plot(yt, zt, 'o-')
        plt.plot(yT, zT)
        plt.ylabel('Along r axis')
        plt.xlabel('theta')

        plt.show()

    freqR = math.sqrt(d[0]*Const['Hartree']*1e20/(2*Const['m_u']))\
        / (2*math.pi*3e10)
    freqT = math.sqrt(p[0]*Const['Hartree']/(0.5e-20*minX*minX*Const['m_u']))\
        / (2*math.pi*3e10)

    print(f'The optimized geometry is at ({minX},{minY}) with E={minZ:.3e}')
    print('Potential for constant theta (around Emin) is '
          f'E = {d[0]:+.3e}r^2{d[1]:+.3e}r{d[2]:+.3e} '
          f'with stretching frequency: {freqR:.1f} 1/cm ')
    print('Potential for constant r (around Emin) is '
          f'E = {p[0]:+.3e}t^2{p[1]:+.3e}t{p[2]:+.3e} '
          f'with bending frequency: {freqT:.1f} 1/cm')

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
