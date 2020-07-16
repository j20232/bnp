import bpy
import sys
from pathlib import Path
import importlib

# Please change LIBRARY_ROOT_PATH according to your environment
LIBRARY_ROOT_PATH = Path(".").resolve().parent
sys.path.append(str(LIBRARY_ROOT_PATH))


if __name__ == '__main__':
    import bnp
    importlib.reload(bnp)
    bnp.scene.remove_objects("debug")

    obj = bpy.context.scene.objects["Cube"]

    bnp.objects.mesh.remove_shape_keys(obj)

    bnp.objects.mesh.add_shape_key(obj, "root")
    vertices = bnp.any2np(obj)
    print("vertices: ", vertices.shape)

    small_vertices = 0.5 * vertices
    bnp.objects.mesh.add_shape_key(obj, "small", vertices=small_vertices)

    big_vertices = 1.5 * vertices
    bnp.objects.mesh.add_shape_key(obj, "big", vertices=big_vertices)

    blend_weights = {
        # key: frame, dict: blend weights
        "0": {
            "root": 1.0,
            "small": 0.0,
            "big": 0.0,
        },
        "20": {
            "root": 0.0,
            "small": 1.0,
            "big": 0.0,
        },
        "50": {
            "root": 0.0,
            "small": 0.0,
            "big": 1.0,
        }
    }
    bnp.objects.mesh.insert_keyframes_to_shape_keys(obj, blend_weights)

    keyframes = bnp.objects.mesh.get_keyframe_of_shapekeys(obj)
    print("keyframes: ", keyframes)
