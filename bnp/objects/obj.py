import bpy
import bmesh
from mathutils import Vector, Matrix
import numpy as np
from bnp.objects.base import vec2np, mat2np, vertices2np, collection2np, world_matrix2np
from bnp.objects.mesh import mesh2np
from bnp.objects.armature import armature2np


def any2np(obj, dtype=np.float32, **kwargs) -> np.ndarray:
    if type(obj) == Vector:
        return vec2np(obj, dtype=dtype)
    if type(obj) == Matrix:
        return mat2np(obj, dtype=dtype)
    elif type(obj) == bpy.types.Object:
        return obj2np(obj, dtype=dtype, **kwargs)
    elif type(obj) == str:
        return objname2np(obj, dtype=dtype, **kwargs)
    elif type(obj) == bpy.types.Mesh:
        return mesh2np(obj, dtype=dtype)
    elif type(obj) == bmesh.types.BMVertSeq:
        return vertices2np(obj, dtype)
    elif type(obj) == bpy.types.bpy_prop_collection:
        return collection2np(obj, dtype)
    else:
        raise NotImplementedError(f"{type(obj)} is not supported with any2np.")


def obj2np(obj: bpy.types.Object, dtype=np.float32, apply_modifier=False,
           frame=bpy.context.scene.frame_current, geo_type="position",
           is_local=False, as_homogeneous=False, mode="dynamic") -> np.ndarray:
    # Input: obj(bpy.types.Object), Output: positions or normals
    bpy.context.scene.frame_set(frame)
    if type(obj.data) == bpy.types.Mesh :
        if apply_modifier:
            depsgraph = bpy.context.evaluated_depsgraph_get()
            obj = obj.evaluated_get(depsgraph)
            mesh = obj.to_mesh()
            return np.array([vec2np(v.co) for v in mesh.vertices], dtype=dtype)
        world_matrix = world_matrix2np(obj, dtype=dtype)  # (4, 4)
        return mesh2np(obj.data, world_matrix=world_matrix, geo_type=geo_type, dtype=dtype,
                       is_local=is_local, frame=frame, as_homogeneous=as_homogeneous)
    elif type(obj.data) == bpy.types.Armature:
        return armature2np(obj.data, dtype=dtype, mode=mode, frame=frame)
    else:
        raise NotImplementedError(
            f"{type(obj.data)} is not supported with obj2np")


def objname2np(obj_name: str, dtype=np.float32, apply_modifier=False,
               frame=bpy.context.scene.frame_current, geo_type="position",
               is_local=False, as_homogeneous=False, mode="dynamic") -> np.ndarray:
    return obj2np(bpy.context.scene.objects[obj_name], dtype=dtype,
                  apply_modifier=apply_modifier, frame=frame, geo_type=geo_type,
                  is_local=is_local, as_homogeneous=as_homogeneous, mode=mode)
