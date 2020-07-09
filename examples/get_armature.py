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

    armature = bpy.context.scene.objects["Armature"]
    joints = bnp.conversion.armature2np(armature)
    print(joints)  # (vtx_num, 3)
