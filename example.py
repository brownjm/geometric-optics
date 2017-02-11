"""Example usage of the geometric module"""
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
