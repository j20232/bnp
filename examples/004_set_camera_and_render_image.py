import bpy
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
    bnp.set_envmap(str(LIBRARY_ROOT_PATH / "assets" / "env_test.png"))
    bnp.scene.import_geom(str(LIBRARY_ROOT_PATH / "assets" / "Suzanne.glb"))
    suzanne = bpy.context.scene.objects["Suzanne"]
    suzanne.name = "debug_monkey"

    use_cv_coord = True
    camera1 = bnp.create_camera(position=[0.0, 0.0, 4.0])
    print("lens1: ", camera1.data.lens)
    vertices = (bnp.objname2np("debug_monkey", as_homogeneous=True)).reshape(-1, 4, 1)
    K, Rt = bnp.camera2np(camera1, use_cv_coord=use_cv_coord)
    print("Intrinsic 1: ", K)
    print("Extrinsic 1: ", Rt)

    KRt = (K @ Rt).reshape(1, 3, 4)
    projected_points = (KRt @ vertices).reshape(-1, 3)
    projected_points = projected_points / projected_points[:, 2].reshape(-1, 1)
    projected_points /= 100  # for visualization
    # bnp.scene.put_cubes(projected_points, size=0.10, sampling_rate=5)
    P = K @ Rt

    camera2 = bnp.create_camera("debug_reconstructed_camera", P=P, scale=1.0, use_cv_coord=use_cv_coord)
    print("lens2: ", camera2.data.lens)
    K, Rt = bnp.camera2np(camera2, use_cv_coord=use_cv_coord)
    # Note: length of sensor height cannot be reconstructed only with intrinsic parameters,
    # so, you can get different intrinsic parameters from camera 1
    print("Intrinsic 2: ", K)
    print("Extrinsic 2: ", Rt)
    print("----------")

    camera3 = bnp.create_camera("debug_reconstructed_camera2", K=K, Rt=Rt, scale=1.0, use_cv_coord=use_cv_coord)
    print("lens3: ", camera3.data.lens)
    K, Rt = bnp.camera2np(camera3, use_cv_coord=use_cv_coord)
    print("Intrinsic 3: ", K)
    print("Extrinsic 3: ", Rt)

    # Render with EEVEE
    # bnp.scene.render(str(LIBRARY_ROOT_PATH / "assets" / "eevee_out"), camera=camera3, render_mode="all")

    # Render with Cycles
    bnp.scene.render(str(LIBRARY_ROOT_PATH / "assets" / "cycles_out"), camera=camera3, engine="CYCLES", render_mode="all")  # Output

    # Export each buffer
    # bnp.scene.render(str(LIBRARY_ROOT_PATH / "assets" / "cycles_out"), camera=camera3, engine="CYCLES", render_mode="Image")  # Output
    # bnp.scene.render(str(LIBRARY_ROOT_PATH / "assets" / "cycles_out"), camera=camera3, engine="CYCLES", render_mode="DiffCol")  # Albedo
    # bnp.scene.render(str(LIBRARY_ROOT_PATH / "assets" / "cycles_out"), camera=camera3, engine="CYCLES", render_mode="Depth")  # Depth
    # bnp.scene.render(str(LIBRARY_ROOT_PATH / "assets" / "cycles_out"), camera=camera3, engine="CYCLES", render_mode="Mist")  # Stencil
    # bnp.scene.render(str(LIBRARY_ROOT_PATH / "assets" / "cycles_out"), camera=camera3, engine="CYCLES", render_mode="Normal")  # Normal
    # bnp.scene.render(str(LIBRARY_ROOT_PATH / "assets" / "cycles_out"), camera=camera3, engine="CYCLES", render_mode="Shadow")  # Roughness
    # bnp.scene.render(str(LIBRARY_ROOT_PATH / "assets" / "cycles_out"), camera=camera3, engine="CYCLES", render_mode="Emit")  # Emission
    # bnp.scene.render(str(LIBRARY_ROOT_PATH / "assets" / "cycles_out"), camera=camera3, engine="CYCLES", render_mode="GlossCol")  # Metalic
    # bnp.scene.render(str(LIBRARY_ROOT_PATH / "assets" / "cycles_out"), camera=camera3, engine="CYCLES", render_mode="AO")  # Ambient Occlusion

    # Export movie
    # bnp.scene.render(str(LIBRARY_ROOT_PATH / "assets" / "eevee_movie"), ext="mp4", camera=camera3, animation=True, frame_start=0, frame_end=3)
