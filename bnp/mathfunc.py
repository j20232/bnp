import numpy as np


def vec2np(vec, dtype=np.float32) -> np.ndarray:
    return np.array([v for v in vec], dtype=dtype)


def mat2np(mat, dtype=np.float32) -> np.ndarray:
    return np.array([vec2np(mat[rid]) for rid in range(len(mat.row))], dtype=dtype)


def batch_identity(batch_num, size, dtype=np.float32):
    R = np.zeros((batch_num, size, size), dtype=dtype)
    for i in range(size):
        R[:, i, i] = 1.0


def normalize_quaternion(q, eps=1e-10):
    if len(q.shape) == 1:
        q = q.reshape(1, -1)
    q /= (np.sqrt(q[:, 0] ** 2 + q[:, 1] ** 2 +
                  q[:, 2] ** 2 + q[:, 3] ** 2) + eps).reshape(-1, 1)
    return q


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


def normalize_axis_angle(a, eps=1e-10):
    if len(a.shape) == 1:
        a = a.reshape(1, -1)
    norm = np.sqrt(a[:, 1] ** 2 + a[:, 2] ** 2 + a[:, 3] ** 2) + eps
    a[:, 1:4] /= norm.reshape(-1, 1)
    return a


def axis_angle2R(a, dtype=np.float32, eps=1e-10):
    # a: (num_of_axis_angle, 3) [w, x, y, z]  w is represented as radian
    a = normalize_axis_angle(a, eps=eps)
    R = batch_identity(q.shape[0], 4, dtype=dtype)
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


def linear_blend_skinning(vertices, rest_pose, dynamic_pose, skinning_weights):
    """Calculate new vertex positions

    Args:
        vertices (np.ndarray): homogeneous vertex positions (vtx_num, 4)
        rest_pose (np.ndarray): translation matices at rest pose (joint_num, 4, 4)
        dynamic_pose (np.ndarray): translation matrices at a specified frame (joint_num, 4, 4)
        skinning_weights (np.ndarray): skinning weights (equal to vertex weights) (vtx_num, joint_num)

    Returns:
        np.ndarray: new vertex positions at homogeneous coordinates (vtx_num, 4)
    """
    vertices = vertices.reshape(-1, 1, 4)
    inv_rest_pose = np.linalg.inv(rest_pose).transpose(0, 2, 1)
    dynamic_pose = dynamic_pose.transpose(0, 2, 1)
    skinning_weights = skinning_weights.reshape(len(vertices), -1, 1, 1)
    lbs_matrices = np.sum(skinning_weights * inv_rest_pose @ dynamic_pose, axis=1)
    return (vertices @ lbs_matrices)[:, 0]  # (vtx_num, 4)
