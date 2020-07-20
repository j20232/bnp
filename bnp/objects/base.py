import bpy
import numpy as np

# ----------------------------------- Conversion -----------------------------------------


def batch_identity(batch_num, size, dtype=np.float32):
    R = np.zeros((batch_num, size, size), dtype=dtype)
    for i in range(size):
        R[:, i, i] = 1.0
    return R


def vec2np(vec, dtype=np.float32) -> np.ndarray:
    return np.array([v for v in vec], dtype=dtype)


def mat2np(mat, dtype=np.float32) -> np.ndarray:
    return np.array([vec2np(mat[rid]) for rid in range(len(mat.row))], dtype=dtype)


def vertices2np(vertices, dtype=np.float32) -> np.ndarray:
    np_verts = np.zeros(len(vertices, 3), dtype=dtype)
    for idx, v in enumerate(vertices):
        np_verts[idx] = np.array([v.co.x, v.co.y, v.co.z], dtype=dtype)
    return np_verts


def collection2np(obj, dtype=np.float32):
    if type(obj[0]) == bpy.types.MeshVertex:
        return vertices2np(obj, dtype)
    raise NotImplementedError(type(obj[0]))


def world_matrix2np(obj: bpy.types.Object, dtype=np.float32, frame=bpy.context.scene.frame_current) -> np.ndarray:
    bpy.context.scene.frame_set(frame)
    return location2np(obj, dtype, True, frame) @ rotation2np(obj, dtype, True, frame) @ scale2np(obj, dtype, True, frame)


def location2np(obj: bpy.types.Object, dtype=np.float32, to_matrix=False,
                frame=bpy.context.scene.frame_current) -> np.ndarray:
    bpy.context.scene.frame_set(frame)
    location = vec2np(obj.location, dtype=dtype)
    if not to_matrix:
        return location  # (3)
    mat = np.eye(4, dtype=dtype)
    mat[0:3, 3] = location
    return mat  # (4, 4)


def rotation2np(obj: bpy.types.Object, dtype=np.float32, to_matrix=False,
                frame=bpy.context.scene.frame_current) -> np.ndarray:
    bpy.context.scene.frame_set(frame)
    if obj.rotation_mode == "QUATERNION":
        rot = vec2np(obj.rotation_quaternion, dtype=dtype)  # (3)
    elif obj.rotation_mode == "AXIS_ANGLE":
        rot = vec2np(obj.rotation_axis_angle, dtype=dtype)  # (4)
    else:
        rot = vec2np(obj.rotation_euler, dtype=dtype)  # (3)
    if not to_matrix:
        return rot
    if obj.rotation_mode == "QUATERNION":
        mat = quaternion2R(rot, dtype=dtype)
    elif obj.rotation_mode == "AXIS_ANGLE":
        mat = axis_angle2R(rot, dtype=dtype)
    else:
        mat = euler2R(rot, obj.rotation_mode, dtype=dtype)
    return mat[0]


def scale2np(obj: bpy.types.Object, dtype=np.float32, to_matrix=False,
             frame=bpy.context.scene.frame_current) -> np.ndarray:
    bpy.context.scene.frame_set(frame)
    scale = vec2np(obj.scale)  # (3)
    if not to_matrix:
        return scale
    mat = np.eye(4, dtype=dtype)
    mat[0:3, 0:3] = np.diag(scale)
    return mat


# ----------------------------------- Rotation -----------------------------------------


def normalize_quaternion(q, eps=1e-10):
    if len(q.shape) == 1:
        q = q.reshape(1, -1)
    q /= (np.sqrt(q[:, 0] ** 2 + q[:, 1] ** 2 +
                  q[:, 2] ** 2 + q[:, 3] ** 2) + eps).reshape(-1, 1)
    return q


def normalize_axis_angle(a, eps=1e-10):
    if len(a.shape) == 1:
        a = a.reshape(1, -1)
    norm = np.sqrt(a[:, 1] ** 2 + a[:, 2] ** 2 + a[:, 3] ** 2) + eps
    a[:, 1:4] /= norm.reshape(-1, 1)
    return a


def axis_angle_4to3(a, eps=1e-10):
    a = normalize_axis_angle(a, eps)
    return a[:, 0].reshape(-1, 1) * a[:, 1:4]  # normalize with norm


def axis_angle_3to4(a):
    norm = np.sqrt(a[:, 0] ** 2 + a[:, 1] ** 2 + a[:, 2] ** 2)
    return np.hstack([norm, a])  # norm as rotation angle


def quaternion2R(q, dtype=np.float32, eps=1e-10):
    # q: (num_of_quaternion, 4) [w, x, y, z]
    q = normalize_quaternion(q, eps)
    R = batch_identity(q.shape[0], 4, dtype=dtype)
    R[:, 0, 0] = 1 - 2 * q[:, 2] ** 2 - 2 * q[:, 3] ** 2  # 1 - 2y^2 - 2z^2
    R[:, 0, 1] = 2 * q[:, 1] * q[:, 2] + 2 * q[:, 0] * q[:, 3]  # 2xy + 2wz
    R[:, 0, 2] = 2 * q[:, 1] * q[:, 3] - 2 * q[:, 0] * q[:, 2]  # 2xz - 2wy
    R[:, 1, 0] = 2 * q[:, 1] * q[:, 2] - 2 * q[:, 0] * q[:, 3]  # 2xy - xwz
    R[:, 1, 1] = 1 - 2 * q[:, 1] ** 2 - 2 * q[:, 3] ** 2  # 1 - 2x^2 - 2z^2
    R[:, 1, 2] = 2 * q[:, 2] * q[:, 3] - 2 * q[:, 0] * q[:, 1]  # 2yz - 2wx
    R[:, 2, 0] = 2 * q[:, 1] * q[:, 3] + 2 * q[:, 0] * q[:, 2]  # 2xz + 2wy
    R[:, 2, 1] = 2 * q[:, 2] * q[:, 3] + 2 * q[:, 0] * q[:, 1]  # 2yz + 2wx
    R[:, 2, 2] = 1 - 2 * q[:, 1] ** 2 - 2 * q[:, 2] ** 2  # 1 - 2x^2 - 2y^2
    return R  # (num_of_quaternion, 4, 4)


def axis_angle2R(a, dtype=np.float32, eps=1e-10):
    # a: (num_of_axis_angle, 3) [w, x, y, z]  w is represented as radian
    a = normalize_axis_angle(a, eps=eps)
    R = batch_identity(a.shape[0], 4, dtype=dtype)
    cos = np.cos(a[:, 0])
    sin = np.sin(a[:, 0])
    R[:, 0, 0] = a[:, 1] ** 2 * (1 - cos) + cos            # n_1^2(1 - cos) + cos
    R[:, 0, 1] = a[:, 1] * a[:, 2] * (1 - cos) - a[:, 3] * sin   # n_1n_2(1 - cos) - n_3sin
    R[:, 0, 2] = a[:, 1] * a[:, 3] * (1 - cos) + a[:, 2] * sin   # n_1n_3(1 - cos) + n_2sin
    R[:, 1, 0] = a[:, 1] * a[:, 2] * (1 - cos) + a[:, 3] * sin   # n_1n_2(1 - cos) + n_3sin
    R[:, 1, 1] = a[:, 2] ** 2 * (1 - cos) + cos            # n_2^2(1 - cos) + cos
    R[:, 1, 2] = a[:, 2] * a[:, 3] * (1 - cos) - a[:, 1] * sin   # n_2n_3(1 - cos) - n_1sin
    R[:, 2, 0] = a[:, 1] * a[:, 3] * (1 - cos) - a[:, 2] * sin   # n_1n_3(1 - cos) - n_2sin
    R[:, 2, 1] = a[:, 2] * a[:, 3] * (1 - cos) + a[:, 1] * sin   # n_2n_3(1 - cos) + n_1sin
    R[:, 2, 2] = a[:, 3] ** 2 * (1 - cos) + cos            # n_3^2(1 - cos) + cos
    return R  # (num_of_axis_angle, 4, 4)


def euler2R(e, mode, dtype=np.float32):
    # e: (num_of_euler_angles, 3) [x, y, z]
    if len(e.shape) == 1:
        e = e.reshape(1, -1)
    one = np.ones(e.shape[0], dtype=dtype)
    zero = np.zeros(e.shape[0], dtype=dtype)
    Rx = np.array([one, zero, zero, zero,
                   zero, np.cos(e[:, 0]), -np.sin(e[:, 0]), zero,
                   zero, np.sin(e[:, 0]), np.cos(e[:, 0]), zero,
                   zero, zero, zero, one], dtype=dtype).reshape(-1, 4, 4)
    Ry = np.array([np.cos(e[:, 1]), zero, np.sin(e[:, 1]), zero,
                   zero, one, zero, zero,
                   -np.sin(e[:, 1]), zero, np.cos(e[:, 1]), zero,
                   zero, zero, zero, one], dtype=dtype).reshape(-1, 4, 4)
    Rz = np.array([np.cos(e[:, 2]), -np.sin(e[:, 2]), zero, zero,
                   np.sin(e[:, 2]), np.cos(e[:, 2]), zero, zero,
                   zero, zero, one, zero,
                   zero, zero, zero, one], dtype=dtype).reshape(-1, 4, 4)
    # shape to return: (num_of_euler_angles, 4, 4)
    if mode == "XYZ":
        return Rz @ Ry @ Rx
    elif mode == "XZY":
        return Ry @ Rz @ Rx
    elif mode == "YXZ":
        return Rz @ Rx @ Ry
    elif mode == "YZX":
        return Rx @ Rz @ Ry
    elif mode == "ZYX":
        return Rx @ Ry @ Rz
    elif mode == "ZXY":
        return Ry @ Rx @ Rz
    else:
        NotImplementedError(f"mode {mode} is not supported.")


def change_rotation_mode(obj, rotation_mode, normalized=True):
    if rotation_mode == "rotation_axis_angle":
        rotation_mode = "AXIS_ANGLE"
    elif rotation_mode == "rotation_quaternion":
        rotation_mode = "QUATERNION"
    elif rotation_mode == "rotation_euler":
        rotation_mode = "XYZ"
    obj.rotation_mode = rotation_mode
    if normalized and obj.rotation_mode == "AXIS_ANGLE":
        axis_angle = normalize_axis_angle(vec2np(obj.rotation_axis_angle))[0]
        obj.rotation_axis_angle = (axis_angle[0], axis_angle[1], axis_angle[2], axis_angle[3])
    elif normalized and obj.rotation_mode == "QUATERNION":
        quat = normalize_quaternion(vec2np(obj.rotation_quaternion))[0]
        obj.rotation_quaternion = (quat[0], quat[1], quat[2], quat[3])

# ----------------------------------- Keyframe -----------------------------------------


def get_keyframe_list(obj):
    if obj.animation_data.action is None:
        return []
    keyframes = []
    for fcurve in obj.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            # keyframe: Vector(keyframe, value)
            keyframes.append(int(keyframe.co[0]))
    return list(sorted(set(keyframes)))


def insert_keyframe(obj, vec: np.ndarray, datapath: str, frame=bpy.context.scene.frame_current) -> np.ndarray:
    bpy.context.scene.frame_set(frame)
    if datapath == "rotation":
        if obj.rotation_mode == "AXIS_ANGLE":
            datapath = "rotation_axis_angle"
        elif obj.rotation_mode == "QUATERNION":
            datapath = "rotation_quaternion"
        else:
            datapath = "rotation_euler"

    if datapath == "location":
        obj.location = (vec[0], vec[1], vec[2])
    elif datapath == "rotation_euler":
        obj.rotation_mode = "XYZ"
        obj.rotation_euler = (vec[0], vec[1], vec[2])
    elif datapath == "rotation_quaternion":
        obj.rotation_mode = "QUATERNION"
        obj.rotation_quaternion = (vec[0], vec[1], vec[2], vec[3])
    elif datapath == "rotation_axis_angle":
        obj.rotation_mode = "AXIS_ANGLE"
        obj.rotation_axis_angle = (vec[0], vec[1], vec[2], vec[3])
    elif datapath == "scale":
        obj.scale = (vec[0], vec[1], vec[2])
    else:
        raise NotImplementedError("Illegal datapath!")
    obj.keyframe_insert(data_path=datapath, frame=frame)


def remove_keyframe(obj, frame):
    if obj.rotation_mode == "QUATERNION":
        obj.keyframe_insert(data_path="rotation_quaternion", frame=frame)
        obj.keyframe_delete(data_path="rotation_quaternion", frame=frame)
    elif obj.rotation_mode == "AXIS_ANGLE":
        obj.keyframe_insert(data_path="rotation_axis_angle", frame=frame)
        obj.keyframe_delete(data_path="rotation_axis_angle", frame=frame)
    else:
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)
        obj.keyframe_delete(data_path="rotation_euler", frame=frame)
    obj.keyframe_insert(data_path="location", frame=frame)
    obj.keyframe_delete(data_path="location", frame=frame)
    obj.keyframe_insert(data_path="scale", frame=frame)
    obj.keyframe_delete(data_path="scale", frame=frame)


def remove_keyframes(obj, frames):
    for frame in frames:
        remove_keyframe(obj, frame)
