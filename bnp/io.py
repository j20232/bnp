import bpy
import numpy as np
from bnp.conversion import obj2np


def load_geom(obj_name):
    obj = bpy.context.scene.objects[obj_name]
    positions = obj2np(obj, "position")
    return positions
