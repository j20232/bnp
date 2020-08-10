import bpy
import numpy as np
from typing import Tuple

from numpy.core.records import ndarray
from mathutils import Matrix

from bnp.objects.base import world_matrix2np, vec2np

# -------------------------------- Create ------------------------------------


def camera2np(camera: bpy.types.Object, render: bpy.types.RenderSettings = bpy.context.scene.render,
              dtype: type = np.float32, frame: int = bpy.context.scene.frame_current,
              use_cv_coord: bool = False) -> Tuple[np.ndarray]:
    K = get_intrinsic_parameters(camera, render, dtype)
    Rt = get_extrinsic_parameters(camera, dtype, frame, use_cv_coord)
    return K, Rt


def get_intrinsic_parameters(camera: bpy.types.Object, render: bpy.types.RenderSettings = bpy.context.scene.render,
                             dtype: type = np.float32) -> np.ndarray:
    # Reference: https://blender.stackexchange.com/questions/38009/3x4-camera-matrix-from-blender-camera
    if type(camera.data) is bpy.types.Camera:
        camera = camera.data
    assert render.resolution_percentage == 100
    assert camera.sensor_fit != "VERTICAL"

    f_in_mm = camera.lens
    image_width = render.resolution_x
    image_height = render.resolution_y
    sensor_width = camera.sensor_width
    pixel_aspect_ratio = render.pixel_aspect_y / render.pixel_aspect_x

    # Parameters of intrinsic calibration matrix K
    f_x = f_in_mm / sensor_width * image_width
    f_y = f_x * pixel_aspect_ratio
    c_x = image_width * (0.5 - camera.shift_x)
    c_y = image_height * 0.5 + image_width * camera.shift_y
    skew = 0  # only use rectangular pixels

    K = np.array([[f_x, skew, c_x],
                  [0.0, f_y, c_y],
                  [0.0, 0.0, 1.0]], dtype=dtype)
    return K


def get_extrinsic_parameters(camera: bpy.types.Object, dtype: type = np.float32,
                             frame: int = bpy.context.scene.frame_current,
                             use_cv_coord: bool = False) -> np.ndarray:
    if not use_cv_coord:
        return world_matrix2np(camera, dtype=dtype, frame=frame)[0:3, 0:4]
    # Reference: https://blender.stackexchange.com/questions/38009/3x4-camera-matrix-from-blender-camera
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


def KRt_from_P(P: np.ndarray) -> Tuple[np.ndarray]:
    # Reference: https://gist.github.com/autosquid/8e1cddbc0336a49c6f84591d35371c4d
    # P: [3, 4]
    H = P[:, 0:3]  # [3, 3]
    [K, R] = rf_rq(H)

    K /= K[-1, -1]

    # from http://ksimek.github.io/2012/08/14/decompose/
    # make the diagonal of K positive
    sg = np.diag(np.sign(np.diag(K)))

    K = K @ sg
    R = sg @ R
    # det(R) negative, just invert; the proj equation remains same:
    if (np.linalg.det(R) < 0):
        R = -R
    C = np.linalg.lstsq(-H, P[:, -1])[0]
    T = -R @ C
    return K, R, T


def rf_rq(P):
    # Reference: https://gist.github.com/autosquid/8e1cddbc0336a49c6f84591d35371c4d
    P = P.T
    # numpy only provides qr. Scipy has rq but doesn't ship with blender
    q, r = np.linalg.qr(P[::-1, ::-1], 'complete')
    q = q.T
    q = q[::-1, ::-1]
    r = r.T
    r = r[::-1, ::-1]

    if (np.linalg.det(q) < 0):
        r[:, 0] *= -1
        q[0, :] *= -1
    return r, q


def create_camera(name: str = "debug_camera", position: list = [0.0, 0.0, 3.0], rotation: list = [0.0, 0.0, 0.0],
                  sensor_width: float = 1.0, align: str = "WORLD", enter_editmode: bool = False,
                  render: bpy.types.RenderSettings = bpy.context.scene.render,
                  P: np.ndarray = None, K: np.ndarray = None, Rt: np.ndarray = None, scale: float = 1.0, use_cv_coord: bool = False) -> bpy.types.Object:
    bpy.ops.object.camera_add(align=align, enter_editmode=enter_editmode, location=position, rotation=rotation)
    camera = bpy.context.active_object
    camera.name = name
    if P is None and (K is None or Rt is None):
        return camera
    if P is not None:
        K, R_world2cv, T_world2cv = KRt_from_P(P)
    else:
        R_world2cv = Rt[0:3, 0:3]
        T_world2cv = Rt[0:3, 3]
    # Extrinsic
    # http://blender.stackexchange.com/questions/38009/3x4-camera-matrix-from-blender-camera
    R_bcam2cv = Matrix(((1, 0, 0), (0, -1, 0), (0, 0, -1))) if use_cv_coord else Matrix.Identity(3)
    R_cv2world = R_world2cv.T
    rotation = Matrix(R_cv2world.tolist()) @ R_bcam2cv
    location = -R_cv2world @ T_world2cv
    camera.location = location
    camera.matrix_world = Matrix.Translation(location) @ rotation.to_4x4()

    # Intrinsic
    f_x = K[0, 0]
    f_y = K[1, 1]
    c_x = K[0, 2]
    image_width = c_x * 2  # principal point x assumed at the center
    cam = camera.data
    cam.name = 'CamFrom3x4P'
    cam.type = 'PERSP'
    cam.lens = f_x / image_width * sensor_width
    cam.lens_unit = 'MILLIMETERS'
    cam.sensor_width = sensor_width
    render.pixel_aspect_x = 1.0
    render.pixel_aspect_y = f_y / f_x
    bpy.context.scene.camera = camera
    return camera
