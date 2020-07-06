import bpy
import mathutils
import numpy as np


def any2np(obj, dtype=np.float32, is_local=False):
    if type(obj) == mathutils.Vector:
        return vec2np(obj, dtype=dtype)
    if type(obj) == mathutils.Matrix:
        return mat2np(obj, dtype=dtype)
    elif type(obj) == bpy.types.ObjectType:
        return obj2np(obj, dtype=dtype, is_local=is_local)
    elif type(obj) == bpy.types.Mesh:
        return mesh2np(obj, dtype=dtype, is_local=is_local)
    else:
        raise NotImplementedError(f"{type(obj)} is not supported.")


def vec2np(vec, dtype=np.float32):
    return np.array([v for v in vec], dtype=dtype)


def mat2np(mat, dtype=np.float32):
    return np.array([vec2np(mat[rid]) for rid in range(len(mat.row))], dtype=dtype)


def obj2np(obj, geo_type="position", dtype=np.float32, is_local=False):
    local_vertices = mesh2np(obj.data, geo_type, dtype, is_local)
    if is_local or geo_type == "normal":
        return local_vertices
    world_matrix = mat2np(obj.matrix_world, dtype=dtype)
    homov = np.hstack((local_vertices, np.ones((len(local_vertices), 1))))
    return np.array([world_matrix @ homov[vid]
                     for vid in range(len(local_vertices))], dtype=dtype)[:, 0:3]


def mesh2np(mesh, geo_type="position", dtype=np.float32, is_local=False):
    if geo_type not in ["position", "normal"]:
        raise Exception("The type should  be position or normal.")
    return np.array([
        vec2np(vt.co if geo_type == "position" else vt.normal)
        for vt in mesh.vertices], dtype=dtype)
