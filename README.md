# geometric-optics

A simple Python module for tracing rays through a series of geometric
optical elements. Rays and lenses can be added to a scene sequentially
and the resulting ray paths can be viewed. It is intended as a
teaching illustration to help students visualize how rays propagate
through simple optical system.

Internally, rays are traced through optical elements using [ray
transfer matrix
analysis](https://en.wikipedia.org/wiki/Ray_transfer_matrix_analysis),
where each optical element is represented by a 2x2 matrix operating on
a 2x1 vector representing the ray's height and angle. This general
formalism allows for new optical elements to be added to the program
easily, and the same classes of optical elements used for propagating
gaussian beams.


# example code
```python
from geometric import Scene, Ray, Lens, FreeSpace

# The scene object holds the optical rays and elements
scene = Scene()

# Optical rays are specified by their height [mm] and angle [radians] from the optical axis
ray1 = Ray(height=0, angle=0.1)
ray2 = Ray(height=5, angle=0)

# Each item that is created must be added to the scene
scene.add(ray1)
scene.add(ray2)

# To add a lens that is located 100mm after the rays use FreeSpace(100)
scene.add(FreeSpace(distance=100))
scene.add(Lens(focus=50))

# Add another lens of the same focal length 200mm after the first lens
scene.add(FreeSpace(200))
scene.add(Lens(focus=50))

# Finally, allow the rays to propagate 100mm after the second lens
scene.add(FreeSpace(100))

# View the scene that has been created
scene.view()
```
![example.png](./example.png)