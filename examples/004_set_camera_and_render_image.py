import numpy as np
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
    point_light = bnp.create_light()
    camera = bnp.create_camera()
    vertices = (bnp.objname2np("Suzanne", as_homogeneous=True)).reshape(-1, 4, 1)
    K, Rt = bnp.camera2np(camera, use_cv_coord=True)
    KRt = (K @ Rt).reshape(1, 3, 4)
    projected_points = (KRt @ vertices).reshape(-1, 3)
    projected_points = projected_points / projected_points[:, 2].reshape(-1, 1)
    projected_points /= 100  # for visualization
    bnp.scene.put_cubes(projected_points, size=0.10, sampling_rate=3)
