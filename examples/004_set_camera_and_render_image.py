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
    print(sys.path)
    bnp.scene.remove_objects("debug")
    bnp.scene.put_cubes([[0, 0, 0]], size=1.0)

    bnp.create_lights(0, 0)
