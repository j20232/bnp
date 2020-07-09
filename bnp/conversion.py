import bpy
import mathutils
import numpy as np


def any2np(obj, dtype=np.float32, **kwargs):
    if type(obj) == mathutils.Vector:
        return vec2np(obj, dtype=dtype)
    if type(obj) == mathutils.Matrix:
        return mat2np(obj, dtype=dtype)
    elif type(obj) == bpy.types.Object:
        return obj2np(obj, dtype=dtype, **kwargs)
    elif type(obj) == str:
        return objname2np(obj, dtype=dtype, **kwargs)
    elif type(obj) == bpy.types.Mesh:
        return mesh2np(obj, dtype=dtype)
    else:
        raise NotImplementedError(f"{type(obj)} is not supported with any2np.")


def vec2np(vec, dtype=np.float32):
    return np.array([v for v in vec], dtype=dtype)


def mat2np(mat, dtype=np.float32):
    return np.array([vec2np(mat[rid]) for rid in range(len(mat.row))], dtype=dtype)


def obj2np(obj, dtype=np.float32, **kwargs):
    # Input: obj(bpy.types.Object), Output: positions or normals
    if type(obj.data) == bpy.types.Mesh:
        world_matrix = get_world_matrix_as_np(obj, dtype=dtype)  # (4, 4)
        return mesh2np(obj.data, world_matrix=world_matrix, **kwargs)
    elif type(obj.data) == bpy.types.Armature:
        return armature2np(obj, **kwargs)
    else:
        raise NotImplementedError(
            f"{type(obj.data)} is not supported with obj2np")


def objname2np(obj_name, dtype=np.float32, **kwargs):
    return obj2np(bpy.context.scene.objects[obj_name], dtype=dtype, **kwargs)


def mesh2np(mesh, world_matrix=None,
            geo_type="position", dtype=np.float32, is_local=False,
            frame=bpy.context.scene.frame_current, as_homogeneous=False):
    # Input: mesh(bpy.types.Mesh), Output: positions or normals
    bpy.context.scene.frame_set(frame)
    if geo_type not in ["position", "normal"]:
        raise Exception("The type should  be position or normal.")

    # select position or normal
    local_verts = np.array([
        vec2np(v.co if geo_type == "position" else v.normal)
        for v in mesh.vertices], dtype=dtype)

    # whether convert to homogeneous coordinates or not
    local_verts = np.hstack((local_verts, np.ones(
        (len(local_verts), 1)))) if as_homogeneous or world_matrix is not None else local_verts
    if is_local or geo_type == "normal" or world_matrix is None:
        return local_verts if as_homogeneous else local_verts[:, 0:3]

    # Calculate global positions
    global_verts = np.array(
        [world_matrix @ v for v in local_verts], dtype=dtype)
    return global_verts if as_homogeneous else global_verts[:, 0:3]


def armature2np(armature, dtype=np.float32, mode="dynamic",
                frame=bpy.context.scene.frame_current):
    if mode in ["head", "tail", "length", "rest"]:
        return np.array([get_bone_as_np(
            p.bone, dtype=dtype, mode=mode, frame=frame) for p in list(armature.pose.bones)], dtype=dtype)
    elif mode == "dynamic":
        return np.array([get_posebone_as_np(
            p, dtype=dtype, mode=mode, frame=frame) for p in list(armature.pose.bones)], dtype=dtype)
    else:
        raise NotImplementedError(f"Not supported the mode {mode}.")


def get_world_matrix_as_np(obj, dtype=np.float32, frame=bpy.context.scene.frame_current):
    bpy.context.scene.frame_set(frame)
    return mat2np(obj.matrix_world, dtype=dtype)  # (4, 4)


def get_location_as_np(obj, dtype=np.float32, frame=bpy.context.scene.frame_current):
    bpy.context.scene.frame_set(frame)
    return vec2np(obj.location, dtype=dtype)  # (3)


def get_rotation_as_np(obj, dtype=np.float32, mode="DEFAULT",
                       frame=bpy.context.scene.frame_current):
    bpy.context.scene.frame_set(frame)
    if mode == "QUATERNION" or (mode == "DEFAULT" and obj.rotation_mode == "QUATERNION"):
        return vec2np(obj.rotation_axis_angle, dtype=dtype)  # (3)
    elif mode == "AXIS_ANGLE" or (mode == "DEFAULT" and obj.rotation_mode == "AXIS_ANGLE"):
        return vec2np(obj.rotation_axis_angle, dtype=dtype)  # (4)
    else:
        return vec2np(obj.rotation_euler, dtype=dtype)  # (3)


def get_scale_as_np(obj, dtype=np.float32, frame=bpy.context.scene.frame_current):
    bpy.context.scene.frame_set(frame)
    return vec2np(obj.scale)  # (3)


def get_posebone_as_np(posebone, dtype=np.float32, mode="dynamic",
                       frame=bpy.context.scene.frame_current):
    # Get posebon in pose mode
    bpy.context.scene.frame_set(frame)
    if mode == "head":
        return vec2np(posebone.head, dtype=dtype)
    elif mode == "tail":  # local tail position from the origin of the object
        return vec2np(posebone.tail, dtype=dtype)
    elif mode == "length":  # bone length
        return posebone.length
    elif mode == "dynamic":
        # transform matrix relative to the parent (at frame)
        return mat2np(posebone.matrix, dtype=dtype)
    else:
        raise NotImplementedError(f"mode {mode} isn't supported.")


def get_bone_as_np(bone, dtype=np.float32, mode="rest",
                   frame=bpy.context.scene.frame_current):
    # Get bone in edit mode
    bpy.context.scene.frame_set(frame)
    if mode == "head":  # local head position from the origin of the object
        return vec2np(bone.head_local, dtype=dtype)
    elif mode == "tail":  # local tail position from the origin of the object
        return vec2np(bone.tail_local, dtype=dtype)
    elif mode == "length":  # bone length
        return bone.length
    elif mode == "rest":
        # transform matrix relative to the parent (restpose)
        return mat2np(bone.matrix_local, dtype=dtype)
    else:
        raise NotImplementedError(f"mode {mode} isn't supported.")
