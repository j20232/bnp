import bpy
import numpy as np


# -------------------------------- Create ------------------------------------

def create_lights(positions, rotations, dtype: type = np.float32):
    print(type(dtype))
