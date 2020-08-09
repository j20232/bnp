import bpy
import numpy as np
from typing import Tuple

from numpy.core.records import ndarray

from bnp.objects.base import world_matrix2np, vec2np

# -------------------------------- Create ------------------------------------


def camera2np(camera: bpy.types.Object, render: bpy.types.RenderSettings = bpy.context.scene.render,
              dtype: type = np.float32, frame: int = bpy.context.scene.frame_current,
              use_cv_coord=False) -> Tuple[np.ndarray]:
    K = get_intrinsic_parameters(camera, render, dtype)
    Rt = get_extrinsic_parameters(camera, dtype, frame, use_cv_coord)
    return K, Rt


def get_intrinsic_parameters(camera: bpy.types.Object, render: bpy.types.RenderSettings = bpy.context.scene.render,
                             dtype: type = np.float32) -> np.ndarray:
    # Reference: https://blender.stackexchange.com/questions/38009/3x4-camera-matrix-from-blender-camera
    if type(camera.data) is bpy.types.Camera:
        camera = camera.data
    f_in_mm = camera.lens
    resolution_x = render.resolution_x
    resolution_y = render.resolution_y
    scale = render.resolution_percentage / 100
    sensor_width = camera.sensor_width
    sensor_height = camera.sensor_height
    pixel_aspect_ratio = render.pixel_aspect_x / render.pixel_aspect_y
    if (camera.sensor_fit == 'VERTICAL'):
        # the sensor height is fixed (sensor fit is horizontal),
        # the sensor width is effectively changed with the pixel aspect ratio
        s_u = resolution_x * scale / sensor_width / pixel_aspect_ratio
        s_v = resolution_y * scale / sensor_height
    else:  # 'HORIZONTAL' and 'AUTO'
        # the sensor width is fixed (sensor fit is horizontal),
        # the sensor height is effectively changed with the pixel aspect ratio
        pixel_aspect_ratio = render.pixel_aspect_x / render.pixel_aspect_y
        s_u = resolution_x * scale / sensor_width
        s_v = resolution_y * scale * pixel_aspect_ratio / sensor_height

    # Parameters of intrinsic calibration matrix K
    alpha_u = f_in_mm * s_u
    alpha_v = f_in_mm * s_v
    u_0 = resolution_x * scale / 2
    v_0 = resolution_y * scale / 2
    skew = 0  # only use rectangular pixels

    K = np.array([[alpha_u, skew, u_0],
                  [0.0, alpha_v, v_0],
                  [0.0, 0.0, 1.0]])
    return K


def get_extrinsic_parameters(camera: bpy.types.Object, dtype: type = np.float32,
                             frame: int = bpy.context.scene.frame_current,
                             use_cv_coord=False) -> np.ndarray:
    if not use_cv_coord:
        return world_matrix2np(camera, dtype=dtype, frame=frame)[0:3, 0:4]
    # There are 3 coordinate systems involved:
    #    1. The World coordinates: "world"
    #       - right-handed
    #    2. The Blender camera coordinates: "bcam"
    #       - x is horizontal
    #       - y is up
    #       - right-handed: negative z look-at direction
    #    3. The desired computer vision camera coordinates: "cv"
    #       - x is horizontal
    #       - y is down (to align to the actual pixel coordinates
    #         used in digital images)
    #       - right-handed: positive z look-at direction
    # bcam stands for blender camera
    R_bcam2cv = np.array([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]], dtype=dtype)
    location, rotation = camera.matrix_world.decompose()[0:2]
    R_world2bcam = rotation.to_matrix().transposed()
    T_world2bcam = -1 * R_world2bcam @ location
    R_world2cv = vec2np(R_bcam2cv @ R_world2bcam)
    T_world2cv = vec2np(R_bcam2cv @ T_world2bcam).reshape(3, 1)
    Rt = np.hstack((R_world2cv, T_world2cv))
    return Rt


def create_camera(name: str = "debug_camera", position: list = [0.0, 0.0, 3.0], rotation: list = [0.0, 0.0, 0.0],
                  align: str = "WORLD", enter_editmode: bool = False) -> bpy.types.Object:
    bpy.ops.object.camera_add(align=align, enter_editmode=enter_editmode, location=position, rotation=rotation)
    camera = bpy.context.active_object
    camera.name = name
    return camera