"""Simple module for playing with geometric optics"""

import numpy
from matplotlib import pyplot as p
import matplotlib.patches as patches
from matplotlib import rcParams
from cycler import cycler

# higher resolution figures
rcParams['figure.dpi'] = 200
rcParams['axes.xmargin'] = 0.05
rcParams['axes.ymargin'] = 0.05

class LightRay:
    """Optical ray handles height and angle"""
    def __init__(self, height, angle):
        self.height = height
        self.angle = angle
        self.v = numpy.array((height, angle), ndmin=2).T

    def __repr__(self):
        return "({}, {})".format(self.height, self.angle)


class RayTransferMatrix:
    """ABCD matrix representation of an optical element"""
    def __init__(self, A, B, C, D):
        self.matrix = numpy.array(((A, B),
                                   (C, D)))

    def dot(self, ray):
        """Apply transfer matrix to ray"""
        v = self.matrix.dot(ray.v)
        return LightRay(v[0][0], v[1][0])
        


class FreeSpace:
    def __init__(self, distance):
        self.distance = distance
        self.m = RayTransferMatrix(1, distance, 0, 1)

        
class Lens:
    def __init__(self, focus):
        self.focus = focus
        self.m = RayTransferMatrix(1, 0, -1.0 / focus, 1)


class FlatMirror:
    def __init__(self):
        self.m = RayTransferMatrix(1, 0, 0, 1)




class Scene:
    def __init__(self):
        self.rays = []
        self.elements = []

        
    def add(self, distance, item):
        if isinstance(item, LightRay):
            self.rays.append((distance, item))
        else:
            self.elements.append((distance, item))

            
    def view(self):
        self.fig = p.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_prop_cycle(cycler('color', ['r', 'g', 'c', 'm']))

        self.ax.axhline(ls='--', color='k')
        
        # plot elements
        for z, element in self.elements:
            self.display(z, element)
        
        # plot rays
        for distance, ray in self.rays:
            path = [(0, ray.height)]
            for z, element in self.elements:
                if isinstance(element, FreeSpace):
                    z += element.distance

                    
                ray = element.m.dot(ray)
                path.append((z, ray.height))
                # print(path)


            p.plot(*zip(*path), zorder=10)


        p.xlabel('Distance [cm]')
        p.ylabel('Radius [cm]')
        p.grid('on')
        p.savefig('example.png')
        p.show()
        

        
    def display(self, z, element, radius=2):
        if isinstance(element, Lens):
            self.ax.add_patch(patches.FancyArrowPatch((z, -radius),
                                                      (z, radius),
                                                      arrowstyle='<->',
                                                      mutation_scale=40,
                                                      lw=2,
                                                      color='blue'))
            
            t = self.ax.text(z, radius+0.15, 'f = {} cm'.format(element.focus),
                             horizontalalignment='center',
                             verticalalignment='center')
            t.set_bbox(dict(facecolor='white', alpha=1, edgecolor='black'))


if __name__ == '__main__':
    scene = Scene()

    scene.add(0, LightRay(0, 0.1))
    scene.add(0, LightRay(0.5, 0))
    scene.add(0, FreeSpace(10))
    scene.add(10, Lens(5))
    scene.add(10, FreeSpace(20))
    scene.add(30, Lens(5))
    scene.add(30, FreeSpace(10))
    
    scene.view()
