import numpy as np


def quaternion2R(q, dtype=np.float32, eps=1e-10):
    # q: [w, x, y, z]
    R = np.eye((4), dtype=dtype)
    q /= np.sqrt(q[0] ** 2 + q[1] ** 2 + q[2] ** 2 + q[3] ** 2) + eps
    R[0, 0] = 1 - 2 * q[2] ** 2 - 2 * q[3] ** 2  # 1 - 2y^2 - 2z^2
    R[0, 1] = 2 * q[1] * q[2] + 2 * q[0] * q[3]  # 2xy + 2wz
    R[0, 2] = 2 * q[1] * q[3] - 2 * q[0] * q[2]  # 2xz - 2wy
    R[1, 0] = 2 * q[1] * q[2] - 2 * q[0] * q[3]  # 2xy - xwz
    R[1, 1] = 1 - 2 * q[1] ** 2 - 2 * q[3] ** 2  # 1 - 2x^2 - 2z^2
    R[1, 2] = 2 * q[2] * q[3] - 2 * q[0] * q[1]  # 2yz - 2wx
    R[2, 0] = 2 * q[1] * q[3] + 2 * q[0] * q[2]  # 2xz + 2wy
    R[2, 1] = 2 * q[2] * q[3] + 2 * q[0] * q[1]  # 2yz + 2wx
    R[2, 2] = 1 - 2 * q[1] ** 2 - 2 * q[2] ** 2  # 1 - 2x^2 - 2y^2
    return R  # (4, 4)


def axis_angle2R(a, dtype=np.float32, eps=1e-10):
    # a: [w, x, y, z]  w is represented as radian
    R = np.eye((4), dtype=dtype)
    norm = np.sqrt(a[1] ** 2 + a[2] ** 2 + a[3] ** 2)
    a[1:4] /= norm + eps
    cos = np.cos(a[0])
    sin = np.sin(a[0])
    R[0, 0] = a[1] ** 2 * (1 - cos) + cos            # n_1^2(1 - cos) + cos
    R[0, 1] = a[1] * a[2] * (1 - cos) - a[3] * sin   # n_1n_2(1 - cos) - n_3sin
    R[0, 2] = a[1] * a[3] * (1 - cos) + a[2] * sin   # n_1n_3(1 - cos) + n_2sin
    R[1, 0] = a[1] * a[2] * (1 - cos) + a[3] * sin   # n_1n_2(1 - cos) + n_3sin
    R[1, 1] = a[2] ** 2 * (1 - cos) + cos            # n_2^2(1 - cos) + cos
    R[1, 2] = a[2] * a[3] * (1 - cos) - a[1] * sin   # n_2n_3(1 - cos) - n_1sin
    R[2, 0] = a[1] * a[3] * (1 - cos) - a[2] * sin   # n_1n_3(1 - cos) - n_2sin
    R[2, 1] = a[2] * a[3] * (1 - cos) + a[1] * sin   # n_2n_3(1 - cos) + n_1sin
    R[2, 2] = a[3] ** 2 * (1 - cos) + cos            # n_3^2(1 - cos) + cos
    return R


def euler2R(e, mode, dtype=np.float32):
    # e: [x, y, z]
    Rx = np.array([1.0, 0.0, 0.0, 0.0,
                   0.0, np.cos(e[0]), -np.sin(e[0]), 0.0,
                   0.0, np.sin(e[0]), np.cos(e[0]), 0.0,
                   0.0, 0.0, 0.0, 1.0], dtype=dtype).reshape(-1, 4, 4)
    Ry = np.array([np.cos(e[1]), 0.0, np.sin(e[1]), 0.0,
                   0.0, 1.0, 0.0, 0.0,
                   -np.sin(e[1]), 0.0, np.cos(e[1]), 0.0,
                   0.0, 0.0, 0.0, 1.0], dtype=dtype).reshape(-1, 4, 4)
    Rz = np.array([np.cos(e[2]), -np.sin(e[2]), 0.0, 0.0,
                   np.sin(e[2]), np.cos(e[2]), 0.0, 0.0,
                   0.0, 0.0, 1.0, 0.0,
                   0.0, 0.0, 0.0, 1.0], dtype=dtype).reshape(-1, 4, 4)
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
