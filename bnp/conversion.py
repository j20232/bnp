import bpy
import mathutils
import numpy as np


def any2np(obj, dtype=np.float32, is_local=False):
    if type(obj) == mathutils.Vector:
        return vec2np(obj, dtype=dtype)
    if type(obj) == mathutils.Matrix:
        return mat2np(obj, dtype=dtype)
    elif type(obj) == bpy.types.Object:
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
    # Input: obj(bpy.types.Object), Output: positions or normals
    local_verts = mesh2np(obj.data, geo_type, dtype, is_local)  # (vtx_num, 3)
    if is_local or geo_type == "normal":
        return local_verts  # (vtx_num, 3)
    world_matrix = mat2np(obj.matrix_world, dtype=dtype)  # (4, 4)
    homov = np.hstack((local_verts, np.ones(
        (len(local_verts), 1))))  # (vtx_num, 4)
    return np.array([world_matrix @ v for v in homov], dtype=dtype)[:, 0:3]


def mesh2np(mesh, geo_type="position", dtype=np.float32):
    # Input: mesh(bpy.types.Mesh), Output: positions or normals
    if geo_type not in ["position", "normal"]:
        raise Exception("The type should  be position or normal.")
    return np.array([
        vec2np(v.co if geo_type == "position" else v.normal)
        for v in mesh.vertices], dtype=dtype)  # (vtx_num, 3)
