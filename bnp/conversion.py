import bpy
import mathutils
import numpy as np


def any2np(obj, dtype=np.float32, is_local=False):
    if type(obj) == mathutils.Matrix:
        return mat2np(obj, dtype=dtype)
    elif type(obj) == bpy.types.ObjectType:
        return obj2np(obj, dtype=dtype, is_local=is_local)
    elif type(obj) == bpy.types.Mesh:
        return mesh2np(obj, dtype=dtype, is_local=is_local)
    else:
        raise NotImplementedError(f"{type(obj)} is not supported.")


def mat2np(mat, dtype=np.float32):
    out = np.zeros((len(mat.row), len(mat.col)), dtype=dtype)
    for rid in range(len(mat.row)):
        out[rid] = mat[rid]
    return out


def obj2np(obj, geo_type="position", dtype=np.float32, is_local=False):
    local_vertices = mesh2np(obj.data, geo_type, dtype, is_local)
    if is_local:
        return local_vertices
    world_matrix = mat2np(obj.matrix_world)
    homo_vertices = np.ones((len(local_vertices), 4))
    homo_vertices[:, 0:3] = local_vertices
    for vid in range(len(local_vertices)):
        homo_vertices[vid] = world_matrix @ homo_vertices[vid]
    return homo_vertices[:, 0:3]


def mesh2np(mesh, geo_type="position", dtype=np.float32, is_local=False):
    if geo_type not in ["position", "normal"]:
        raise Exception("The type should  be position or normal.")
    vnum = len(mesh.vertices[0].co)
    out = np.zeros((len(mesh.vertices), vnum))
    for idx, vt in enumerate(mesh.vertices):
        val = vt.co if geo_type == "position" else vt.normal
        out[idx] = np.array([val[0], val[1], val[2]])
    return out
