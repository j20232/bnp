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

    vertices = bnp.conversion.objname2np("Cube")
    print(vertices)  # (vtx_num, 3)

    bnp.scene.put_cubes(vertices)
    
    obj = bpy.context.scene.objects["Cube"]
    cone = bpy.context.scene.objects["Cone"]
    bnp.io.export_geom(str(LIBRARY_ROOT_PATH / "assets" / "box.obj"), obj)
    bnp.io.export_geom(str(LIBRARY_ROOT_PATH / "assets" / "box.fbx"), obj)
    bnp.io.export_geom(str(LIBRARY_ROOT_PATH / "assets" / "box.glb"), obj)
    
