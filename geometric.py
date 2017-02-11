"""Simple module for playing with geometric optics"""

from cycler import cycler
import numpy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# increase the resolution of figures
matplotlib.rcParams['figure.dpi'] = 200

# add some space around optical system (zoom out)
matplotlib.rcParams['axes.xmargin'] = 0.05
matplotlib.rcParams['axes.ymargin'] = 0.05


class Ray:
    """An optical ray is represented by a 2x1 vector containing its height
and angle w.r.t. the optical axis"""
    def __init__(self, height, angle):
        self.height = height
        self.angle = angle
        self.vector = numpy.array((height, angle), ndmin=2).T

    def __repr__(self):
        return "Ray({}, {})".format(self.height, self.angle)



class OpticalElement:
    """An optical element is represented by a 2x2 matrix called an ABCD matrix"""
    def __init__(self, A, B, C, D):
        self.matrix = numpy.array(((A, B),
                                   (C, D)))

    def apply(self, ray):
        """Apply the transfer matrix to the optical ray"""
        height, angle = self.matrix.dot(ray.vector)
        return Ray(height[0], angle[0])
        

class FreeSpace(OpticalElement):
    """Propagation in free space for a specified distance [mm]"""
    def __init__(self, distance):
        self.distance = distance
        OpticalElement.__init__(self, 1, distance, 0, 1)

        
class Lens(OpticalElement):
    """A thin lens with a given focus [mm]"""
    def __init__(self, focus):
        self.focus = focus
        OpticalElement.__init__(self, 1, 0, -1.0 / focus, 1)



class Scene:
    """Optical rays and elements can be added to a scene and then displayed"""
    def __init__(self):
        # rays and optical elements are stored separately as [(distance, item)]
        self.rays = []
        self.optical_elements = []

        # keeps track of current distance when adding new optical elements
        self.current_distance = 0

        
    def add(self, item):
        """Add an item to the scene"""
        if isinstance(item, Ray):
            self.rays.append((self.current_distance, item))
        
        elif isinstance(item, OpticalElement):
            self.optical_elements.append((self.current_distance, item))
            
            if isinstance(item, FreeSpace):
                # for free space propagation, the current distance is updated
                self.current_distance += item.distance
        
        else:
            raise TypeError("Cannot add object to scene: {}".format(type(item)))

            
    def view(self):
        """Display the scene"""
        # create the figure and axes
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_prop_cycle(cycler('color', ['r', 'g', 'c', 'm']))
        ax.axhline(ls='--', color='k')
        ax.set_xlabel('Distance [mm]')
        ax.set_ylabel('Radius [mm]')
        ax.grid(True)
        
        # display each optical element
        for distance, element in self.optical_elements:
            self._draw_element(ax, distance, element)
        
        # plot rays
        for distance, ray in self.rays:
            path = self._trace(distance, ray)
            plt.plot(*zip(*path), zorder=10)


        plt.savefig('example.png')
        plt.show()
        
  
    def _draw_element(self, ax, distance, element, radius=20):
        """Draw an optical element onto the current axes"""
        if isinstance(element, Lens):
            # draw a lens as a double headed arrow <->
            ax.add_patch(patches.FancyArrowPatch((distance, -radius), (distance, radius),
                                                 arrowstyle='<->', mutation_scale=40,
                                                 lw=2, color='blue'))

            # add a text box above lens displaying the focal length
            t = ax.text(distance, radius+3, 'f = {} mm'.format(element.focus),
                        horizontalalignment='center', verticalalignment='center')
            t.set_bbox(dict(facecolor='white', alpha=1, edgecolor='black'))

            
    def _trace(self, z, ray):
        """Trace a ray through each optical element"""
        # save initial ray height
        path = [(z, ray.height)]
        
        for distance, element in self.optical_elements:
            # update distance for free space propagation
            if isinstance(element, FreeSpace):
                z += element.distance

            ray = element.apply(ray)
            path.append((z, ray.height))

        return path

