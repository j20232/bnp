import bpy
import numpy as np


# -------------------------------- Create ------------------------------------

def create_light(name: str = "debug_light", position: list = [0.0, 0.0, 3.0], rotation: list = [0.0, 0.0, 0.0],
                 light_type: str = "POINT", radius: float = 1.0, align: str = "WORLD") -> bpy.types.Light:
    # light_type: "POINT", "SUN", "SPOT" or "AREA"
    # You can see the specification from https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.light_add
    location = [position[0], position[1], position[2]]
    rotation = [rotation[0], rotation[1], rotation[2]]
    bpy.ops.object.light_add(type=light_type, radius=radius, align=align, location=location, rotation=rotation)
    light = bpy.context.active_object
    light.name = name
    return light
