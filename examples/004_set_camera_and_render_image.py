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
    camera1 = bnp.create_camera(position=[0.0, 0.0, 4.0])
    vertices = (bnp.objname2np("Suzanne", as_homogeneous=True)).reshape(-1, 4, 1)
    K, Rt = bnp.camera2np(camera1, use_cv_coord=True)
    print("Intrinsic: ", K)
    print("Extrinsic: ", Rt)

    KRt = (K @ Rt).reshape(1, 3, 4)
    projected_points = (KRt @ vertices).reshape(-1, 3)
    projected_points = projected_points / projected_points[:, 2].reshape(-1, 1)
    projected_points /= 100  # forvisualization
    bnp.scene.put_cubes(projected_points, size=0.10, sampling_rate=3)
    P = K @ Rt

    camera2 = bnp.create_camera("debug_reconstructed_camera", P=P, scale=1.0, use_cv_coord=True)
    camera3 = bnp.create_camera("debug_reconstructed_camera2", K=K, Rt=Rt, scale=1.0, use_cv_coord=True)

    bnp.scene.render(str(LIBRARY_ROOT_PATH / "assets" / "render_out.png"), camera3)
