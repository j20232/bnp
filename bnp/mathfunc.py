import numpy as np


def quaternion2R(q, dtype=np.float32, eps=1e-10):
    # q: (num_of_quaternion, 4) [w, x, y, z]
    if len(q.shape) == 1:
        q = q.reshape(1, -1)
    R = np.zeros((q.shape[0], 4, 4), dtype=dtype)
    for i in range(4):
        R[:, i, i] = 1.0
    q /= (np.sqrt(q[:, 0] ** 2 + q[:, 1] ** 2 +
                  q[:, 2] ** 2 + q[:, 3] ** 2) + eps).reshape(-1, 1)
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
    if len(a.shape) == 1:
        a = a.reshape(1, -1)
    R = np.zeros((a.shape[0], 4, 4), dtype=dtype)
    for i in range(4):
        R[:, i, i] = 1.0
    norm = np.sqrt(a[:, 1] ** 2 + a[:, 2] ** 2 + a[:, 3] ** 2) + eps
    a[:, 1:4] /= norm.reshape(-1, 1)
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
