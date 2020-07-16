import bpy
from bpy.types import Depsgraph
from mathutils import Vector, Matrix
from bnp.mathfunc import vec2np, mat2np
import bnp.mathfunc
from bnp.scene import normalize_armature
import numpy as np


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
        return armature2np(obj.data, dtype=dtype, mode=mode, fram=frame)
    else:
        raise NotImplementedError(
            f"{type(obj.data)} is not supported with obj2np")


def objname2np(obj_name: str, dtype=np.float32, apply_modifier=False,
               frame=bpy.context.scene.frame_current, geo_type="position",
               is_local=False, as_homogeneous=False, mode="dynamic") -> np.ndarray:
    return obj2np(bpy.context.scene.objects[obj_name], dtype=dtype,
                  apply_modifier=apply_modifier, frame=frame, geo_type=geo_type,
                  is_local=is_local, as_homogeneous=as_homogeneous, mode=mode)


def mesh2np(mesh: bpy.types.Mesh, world_matrix=None,
            geo_type="position", dtype=np.float32, is_local=False,
            frame=bpy.context.scene.frame_current, as_homogeneous=False) -> np.ndarray:
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


def armature2np(armature: bpy.types.Object, dtype=np.float32, mode="dynamic",
                frame=bpy.context.scene.frame_current) -> np.ndarray:
    normalize_armature(armature)
    kinematic_tree = get_kinematic_tree(armature)
    if mode in ["head", "tail", "length", "rest_from_origin", "rest", "rest_relative"]:
        return np.array([get_bone_as_np(
            p.bone, kinematic_tree=kinematic_tree, armature=armature,
            dtype=dtype, mode=mode, frame=frame) for p in list(armature.pose.bones)], dtype=dtype)
    elif mode in ["dynamic", "dynamic_from_origin", "dynamic_relative"]:
        return np.array([posebone2np(
            p, kinematic_tree=kinematic_tree, armature=armature,
            dtype=dtype, mode=mode, frame=frame) for p in list(armature.pose.bones)], dtype=dtype)
    else:
        raise NotImplementedError(f"Not supported the mode {mode}.")


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
        mat = bnp.mathfunc.quaternion2R(rot, dtype=dtype)
    elif obj.rotation_mode == "AXIS_ANGLE":
        mat = bnp.mathfunc.axis_angle2R(rot, dtype=dtype)
    else:
        mat = bnp.mathfunc.euler2R(rot, obj.rotation_mode, dtype=dtype)
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


def posebone2np(posebone, kinematic_tree=None, armature=None,
                dtype=np.float32, mode="dynamic",
                frame=bpy.context.scene.frame_current) -> np.ndarray:
    # Get posebon in pose mode
    bpy.context.scene.frame_set(frame)
    if mode == "head":
        return vec2np(posebone.head, dtype=dtype)
    elif mode == "tail":  # local tail position from the origin of the object
        return vec2np(posebone.tail, dtype=dtype)
    elif mode == "length":  # bone length
        return posebone.length
    elif mode == "dynamic_from_origin":
        # absolute translation matrix
        # considering bones' rotation at rest pose
        return mat2np(posebone.matrix, dtype=dtype)
    elif mode == "dynamic_relative":
        if kinematic_tree is None or armature is None:
            raise Exception("Kinematic tree and armature should be inputted.")
        dynamic_pose = rotation2np(posebone, dtype=dtype, to_matrix=True, frame=frame)
        bone_id = list(armature.pose.bones).index(posebone)
        parent_id = kinematic_tree[bone_id]
        parent_pos = np.zeros(3, dtype=dtype) if parent_id == -1 else get_bone_as_np(armature.pose.bones[parent_id].bone, dtype=dtype, mode="head", frame=frame)
        current_pos = get_bone_as_np(posebone.bone, dtype=dtype, mode="head", frame=frame)
        dynamic_pose[0:3, 3] = current_pos - parent_pos
        return dynamic_pose
    elif mode == "dynamic":
        if kinematic_tree is None or armature is None:
            raise Exception("Kinematic tree and armature should be inputted.")
        bone_id = list(armature.pose.bones).index(posebone)
        parent_id = kinematic_tree[bone_id]
        current_mat = posebone2np(posebone, kinematic_tree=kinematic_tree, armature=armature, dtype=dtype, mode="dynamic_relative", frame=frame)
        parent_mat = posebone2np(armature.pose.bones[parent_id], kinematic_tree=kinematic_tree,
                                 armature=armature, dtype=dtype, mode="dynamic", frame=frame) if parent_id != -1 else np.eye(4, dtype=dtype)
        return parent_mat @ current_mat
    else:
        raise NotImplementedError(f"mode {mode} isn't supported.")


def get_bone_as_np(bone, kinematic_tree=None, armature=None,
                   dtype=np.float32, mode="rest",
                   frame=bpy.context.scene.frame_current) -> np.ndarray:
    # Get bone in edit mode
    bpy.context.scene.frame_set(frame)
    if mode == "head":  # local head position from the origin of the object
        return vec2np(bone.head_local, dtype=dtype)
    elif mode == "tail":  # local tail position from the origin of the object
        return vec2np(bone.tail_local, dtype=dtype)
    elif mode == "length":  # bone length
        return bone.length
    elif mode == "rest_from_origin":
        # absolute translation matrix
        # considering bones' rotation at rest pose
        return mat2np(bone.matrix_local, dtype=dtype)
    elif mode == "rest_relative":
        # translation matrix relative to the parent (restpose)
        # not considering bones' rotation at rest pose
        if kinematic_tree is None or armature is None:
            raise Exception("Kinematic tree and armature should be inputted.")
        rest_pose = np.eye(4, dtype=dtype)
        bone_id = list(armature.data.bones).index(bone)
        parent_id = kinematic_tree[bone_id]
        parent_pos = np.zeros(3, dtype=dtype) if parent_id == -1 else get_bone_as_np(armature.pose.bones[parent_id].bone, dtype=dtype, mode="head", frame=frame)
        current_pos = get_bone_as_np(bone, dtype=dtype, mode="head", frame=frame)
        rest_pose[0:3, 3] = current_pos - parent_pos
        return rest_pose
    elif mode == "rest":
        # absolute translation matrix
        # not considering bones' rotation at rest pose
        if kinematic_tree is None or armature is None:
            raise Exception("Kinematic tree and armature should be inputted.")
        bone_id = list(armature.data.bones).index(bone)
        parent_id = kinematic_tree[bone_id]
        current_mat = get_bone_as_np(bone, kinematic_tree=kinematic_tree, armature=armature, dtype=dtype, mode="rest_relative", frame=frame)
        parent_mat = get_bone_as_np(armature.pose.bones[parent_id].bone, kinematic_tree=kinematic_tree,
                                    armature=armature, dtype=dtype, mode="rest", frame=frame) if parent_id != -1 else np.eye(4, dtype=dtype)
        return parent_mat @ current_mat
    else:
        raise NotImplementedError(f"mode {mode} isn't supported.")


def get_skinning_weights_as_np(obj: bpy.types.Object, dtype=np.float32) -> np.ndarray:
    # skining weights are equal to vertex weights in Blender
    mesh = obj.data
    vertices = mesh.vertices
    skinning_weights = np.zeros((len(vertices), len(obj.vertex_groups)))
    for vid, v in enumerate(mesh.vertices):
        for vg in v.groups:
            skinning_weights[vid, vg.group] = vg.weight
        skinning_weights[vid] /= sum(skinning_weights[vid])
    return skinning_weights  # (vtx_num, joint_num)


def get_kinematic_tree(armature: bpy.types.Object):
    # Bone's parent index list (root node's parent idx: -1)
    return [-1 if bone.parent is None else list(armature.data.bones).index(bone.parent)
            for bone in armature.data.bones]
