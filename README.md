# geometric-optics
A simple Python script for tracing rays through geometric optical elements

# example code
```python
from geometric import Scene, Ray, Lens, FreeSpace

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
```
![example.png](./example.png)