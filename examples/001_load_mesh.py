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

    vertices = bnp.obj2np(obj)
    print("Vertex positions: ", vertices)  # (vtx_num, 3)

    world_matrix = bnp.world_matrix2np(obj)
    print("world_matrix: ", world_matrix)

    # Location
    location = bnp.location2np(obj)
    print("Location: ", location)
    loc_matrix = bnp.location2np(obj, to_matrix=True)
    print("Location matrix: ", loc_matrix)

    # Rotation
    rotation = bnp.rotation2np(obj)
    print("Rotation: ", rotation)
    rot_matrix = bnp.rotation2np(obj, to_matrix=True)
    print("Rotation matrix: ", rot_matrix)

    # Scale
    scale = bnp.scale2np(obj)
    print("Scale: ", scale)
    scale_matrix = bnp.scale2np(obj, to_matrix=True)
    print("Scale matrix: ", scale_matrix)

    bnp.scene.put_cubes(vertices)

    """
    bnp.scene.export_geom(str(LIBRARY_ROOT_PATH / "assets" / "box.obj"), obj)
    bnp.scene.export_geom(str(LIBRARY_ROOT_PATH / "assets" / "box.fbx"), obj)
    bnp.scene.export_geom(str(LIBRARY_ROOT_PATH / "assets" / "box.glb"), obj)
    """
