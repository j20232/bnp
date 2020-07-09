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

    vertices = bnp.conversion.obj2np(obj)
    print("Vertex positions: ", vertices)  # (vtx_num, 3)

    location = bnp.conversion.get_location_as_np(obj)
    print("Location: ", location)

    rotation = bnp.conversion.get_rotation_as_np(obj)
    print("Rotation: ", rotation)

    scale = bnp.conversion.get_scale_as_np(obj)
    print("Scale: ", scale)

    bnp.scene.put_cubes(vertices)

    """
    bnp.io.export_geom(str(LIBRARY_ROOT_PATH / "assets" / "box.obj"), obj)
    bnp.io.export_geom(str(LIBRARY_ROOT_PATH / "assets" / "box.fbx"), obj)
    bnp.io.export_geom(str(LIBRARY_ROOT_PATH / "assets" / "box.glb"), obj)
    """
