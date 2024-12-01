import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from functools import reduce

#fig = plt.figure()
#ax = fig.gca(projection='3d')
#ax.set_aspect("equal")


def x_y_edge(x_range, y_range, z_range, color):
    xx, yy = np.meshgrid(x_range, y_range)

    for value in [0, 1]:
        zz = np.zeros([len(xx), len(xx[0])], int) + z_range[value]
        ax.plot_wireframe(xx, yy, zz, color = color)
        ax.plot_surface(xx, yy, zz, color = color, alpha=0.2)
        #ax.plot_wireframe(xx, yy, z_range[value], color = color)
        #ax.plot_surface(xx, yy, z_range[value], color = color, alpha=0.2)


def y_z_edge(x_range, y_range, z_range, color):
    yy, zz = np.meshgrid(y_range, z_range)

    for value in [0, 1]:
        ax.plot_wireframe(x_range[value], yy, zz, color = color)
        ax.plot_surface(x_range[value], yy, zz, color = color, alpha=0.2)


def x_z_edge(x_range, y_range, z_range, color):
    xx, zz = np.meshgrid(x_range, z_range)

    for value in [0, 1]:
        ax.plot_wireframe(xx, y_range[value], zz, color = color)
        ax.plot_surface(xx, y_range[value], zz, color = color, alpha=0.2)


def rect_prism(x_range, y_range, z_range, color):
    x_y_edge(x_range, y_range, z_range, color)
    y_z_edge(x_range, y_range, z_range, color)
    x_z_edge(x_range, y_range, z_range, color)


def getVolume(cube):
    return reduce(lambda a,b: a*b, (abs(c2 - c1) + 1 for c1,c2 in cube), 1)

def drawCube(cube, color):
    rect_prism(*(np.array((t[0], t[1]+1)) for t in cube), color)




def main():
    otherCube = ((-5, 47), (-31, 22), (-19, 33))
    intersection = ((-5, 5), (-27, 21), (-14, 33))
    cube = ((-44, 5), (-27, 21), (-14, 35))


    #drawCube(otherCube, "g")
    #drawCube(cube, "y")
    drawCube(intersection, "c")

    print(f"Total volume before = {getVolume(otherCube) - getVolume(intersection)}")


    cubes = [((5, 47), (-31, 22), (-19, 33)), ((-5, 5), (-31, -27), (-19, 33)), ((-5, 5), (21, 22), (-19, 33)), ((-5, 5), (-27, 21), (-19, -14))]
    cubes = [((6, 47), (-31, 22), (-19, 33)), ((-5, 5), (-31, -28), (-19, 33)), ((-5, 5), (22, 22), (-19, 33)), ((-5, 5), (-27, 21), (-19, -15))]

    for cube in cubes:
        drawCube(cube, "r")
        


    print(f"Total volume decomposed = {sum(getVolume(cube) for cube in cubes)}")

    #drawCube(((1,2), (3,4), (5,6)))
    #drawCube(((5,6), (3,4), (1,2)))
    plt.show()


if __name__ == "__main__":
    main()
