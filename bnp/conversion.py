import bpy
import mathutils
import numpy as np


def any2np(obj, dtype=np.float32, is_local=False,
           frame=bpy.context.scene.frame_current, change_frame=True,
           as_homogeneous=False):
    if type(obj) == mathutils.Vector:
        return vec2np(obj, dtype=dtype)
    if type(obj) == mathutils.Matrix:
        return mat2np(obj, dtype=dtype)
    elif type(obj) == bpy.types.Object:
        return obj2np(obj, dtype=dtype, is_local=is_local, frame=frame, change_frame=change_frame)
    elif type(obj) == str:
        return objname2np(obj, dtype=dtype, is_local=is_local, frame=frame, change_frame=change_frame)
    elif type(obj) == bpy.types.Mesh:
        return mesh2np(obj, dtype=dtype)
    else:
        raise NotImplementedError(f"{type(obj)} is not supported.")


def vec2np(vec, dtype=np.float32):
    return np.array([v for v in vec], dtype=dtype)


def mat2np(mat, dtype=np.float32):
    return np.array([vec2np(mat[rid]) for rid in range(len(mat.row))], dtype=dtype)


def obj2np(obj, geo_type="position", dtype=np.float32, is_local=False,
           frame=bpy.context.scene.frame_current, change_frame=True,
           as_homogeneous=False):
    # Input: obj(bpy.types.Object), Output: positions or normals
    current_time = bpy.context.scene.frame_current
    bpy.context.scene.frame_set(frame)
    local_verts = mesh2np(obj.data, geo_type, dtype, True)  # (vtx_num, 4)
    world_matrix = get_world_matrix_as_np(obj, dtype=dtype)  # (4, 4)
    if not change_frame:
        bpy.context.scene.frame_set(current_time)
    if is_local or geo_type == "normal":
        return local_verts[:, 0:3]  # (vtx_num, 3)
    vertices = np.array([world_matrix @ v for v in local_verts], dtype=dtype)
    return vertices if as_homogeneous else vertices[:, 0:3]


def objname2np(obj_name, geo_type="position", dtype=np.float32, is_local=False,
               frame=bpy.context.scene.frame_current, change_frame=True,
               as_homogeneous=False):
    obj = bpy.context.scene.objects[obj_name]
    return obj2np(obj, geo_type=geo_type, dtype=dtype, is_local=is_local,
                  frame=frame, change_frame=change_frame, as_homogeneous=as_homogeneous)


def mesh2np(mesh, geo_type="position", dtype=np.float32,
            as_homogeneous=False):
    # Input: mesh(bpy.types.Mesh), Output: positions or normals
    if geo_type not in ["position", "normal"]:
        raise Exception("The type should  be position or normal.")
    vertices = np.array([
        vec2np(v.co if geo_type == "position" else v.normal)
        for v in mesh.vertices], dtype=dtype)  # (vtx_num, 3)
    return np.hstack((vertices, np.ones((len(vertices), 1)))) if as_homogeneous else vertices


def get_world_matrix_as_np(obj, dtype=np.float32,
                           frame=bpy.context.scene.frame_current, change_frame=True):
    current_time = bpy.context.scene.frame_current
    bpy.context.scene.frame_set(frame)
    world_matrix = mat2np(obj.matrix_world, dtype=dtype)  # (4, 4)
    if not change_frame:
        bpy.context.scene.frame_set(current_time)
    return world_matrix


def get_location_as_np(obj, dtype=np.float32,
                       frame=bpy.context.scene.frame_current, change_frame=True):
    current_time = bpy.context.scene.frame_current
    bpy.context.scene.frame_set(frame)
    location = vec2np(obj.location, dtype=dtype)  # (3)
    if not change_frame:
        bpy.context.scene.frame_set(current_time)
    return location


def get_rotation_as_np(obj, dtype=np.float32, mode="DEFAULT",
                       frame=bpy.context.scene.frame_current, change_frame=True):
    current_time = bpy.context.scene.frame_current
    bpy.context.scene.frame_set(frame)
    if mode == "QUATERNION" or (mode == "DEFAULT" and obj.rotation_mode == "QUATERNION"):
        rotation = vec2np(obj.rotation_axis_angle, dtype=dtype)  # (3)
    elif mode == "AXIS_ANGLE" or (mode == "DEFAULT" and obj.rotation_mode == "AXIS_ANGLE"):
        rotation = vec2np(obj.rotation_axis_angle, dtype=dtype)  # (4)
    else:
        rotation = vec2np(obj.rotation_euler, dtype=dtype)  # (3)
    if not change_frame:
        bpy.context.scene.frame_set(current_time)
    return rotation


def get_scale_as_np(obj, dtype=np.float32,
                    frame=bpy.context.scene.frame_current, change_frame=True):
    current_time = bpy.context.scene.frame_current
    bpy.context.scene.frame_set(frame)
    scale = vec2np(obj.scale)  # (3)
    if not change_frame:
        bpy.context.scene.frame_set(current_time)
    return scale
