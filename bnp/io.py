import bpy
import numpy as np
from bnp.conversion import obj2np


def load_geom(obj_name, geo_type="position", dtype=np.float32, is_local=False):
    obj = bpy.context.scene.objects[obj_name]
    return obj2np(obj, geo_type=geo_type, dtype=dtype, is_local=is_local)
