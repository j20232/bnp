import bpy
import numpy as np


def load_geom(obj_name):
    obj = bpy.context.scene.objects[obj_name]
    print(obj)
