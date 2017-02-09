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

class Ray:
    """Optical ray handles height and angle"""
    def __init__(self, height, angle):
        self.height = height
        self.angle = angle
        self.v = numpy.array((height, angle), ndmin=2).T

    def __repr__(self):
        return "Ray({}, {})".format(self.height, self.angle)


class RayTransferMatrix:
    """ABCD matrix representation of an optical element"""
    def __init__(self, A, B, C, D):
        self.matrix = numpy.array(((A, B),
                                   (C, D)))

    def dot(self, ray):
        """Apply transfer matrix to ray"""
        v = self.matrix.dot(ray.v)
        return Ray(v[0][0], v[1][0])
        


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
        self.distance = 0

        
    def add(self, item):
        if isinstance(item, Ray):
            self.rays.append((self.distance, item))
        else:
            if isinstance(item, FreeSpace):
                self.elements.append((self.distance, item))
                self.distance += item.distance
            else:
                self.elements.append((self.distance, item))

            
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


        p.xlabel('Distance [mm]')
        p.ylabel('Radius [mm]')
        p.grid('on')
        p.savefig('example.png')
        p.show()
        

        
    def display(self, z, element, radius=20):
        if isinstance(element, Lens):
            self.ax.add_patch(patches.FancyArrowPatch((z, -radius),
                                                      (z, radius),
                                                      arrowstyle='<->',
                                                      mutation_scale=40,
                                                      lw=2,
                                                      color='blue'))
            
            t = self.ax.text(z, radius+3, 'f = {} mm'.format(element.focus),
                             horizontalalignment='center',
                             verticalalignment='center')
            t.set_bbox(dict(facecolor='white', alpha=1, edgecolor='black'))


if __name__ == '__main__':

    # scene will hold the optical rays and elements
    scene = Scene()
    
    # rays are specified by their height [mm] and angle [radians] w.r.t. the optical axis
    ray1 = Ray(height=0, angle=0.1)
    ray2 = Ray(height=5, angle=0)
    
    # each item that we create must be added it to the scene
    scene.add(ray1)
    scene.add(ray2)
    
    # let's add a lens that is 100mm after the rays by using FreeSpace(100)
    scene.add(FreeSpace(100))
    scene.add(Lens(focus=50))
    
    # and add another lens of the same focal length 200mm after the first lens
    scene.add(FreeSpace(200))
    scene.add(Lens(focus=50))
    
    # finally let's allow the rays to propagate 100mm past the second lens
    scene.add(FreeSpace(100))
    
    # let's view what we have made
    scene.view()
