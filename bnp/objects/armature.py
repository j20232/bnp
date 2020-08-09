import bpy
import numpy as np
from bnp.objects.base import vec2np, mat2np, location2np, rotation2np
from bnp.objects.base import normalize_axis_angle, normalize_quaternion, change_rotation_mode
from bnp.objects.base import remove_keyframe, insert_keyframe

# ----------------------------------- Conversion -----------------------------------------


def posebone_basis(dtype: type = np.float32):
    return np.array([1.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, -1.0, 0.0,
                     0.0, 1.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 1.0], dtype=dtype).reshape(4, 4)


def armature2np(armature: bpy.types.Object, dtype: type = np.float32, mode: str = "dynamic",
                frame: int = bpy.context.scene.frame_current) -> np.ndarray:
    normalize_roll(armature)
    if mode in ["head", "tail", "length", "offset", "rest"]:
        return np.array([bone2np(
            p.bone, dtype=dtype, mode=mode, frame=frame) for p in list(armature.pose.bones)], dtype=dtype)
    elif mode in ["dynamic"]:
        return np.array([posebone2np(
            p, dtype=dtype, mode=mode, frame=frame) for p in list(armature.pose.bones)], dtype=dtype)
    elif mode in ["rotation"]:
        return np.array([rotation2np(p, dtype=dtype, frame=frame) for p in list(armature.pose.bones)], dtype=dtype)
    else:
        raise NotImplementedError(f"Not supported the mode {mode}.")


def posebone2np(posebone: bpy.types.PoseBone,
                dtype: type = np.float32, mode: str = "dynamic",
                frame: int = bpy.context.scene.frame_current) -> np.ndarray:
    # Get posebon in pose mode
    bpy.context.scene.frame_set(frame)
    if mode == "head":
        return vec2np(posebone.head, dtype=dtype)
    elif mode == "tail":  # local tail position from the origin of the object
        return vec2np(posebone.tail, dtype=dtype)
    elif mode == "length":  # bone length
        return posebone.length
    elif mode == "offset":  # offset matrix from the parent
        return bone2np(posebone.bone, dtype=dtype, mode=mode, frame=frame)
    elif mode == "dynamic":
        dynamic_pose = rotation2np(posebone, dtype=dtype, to_matrix=True, frame=frame)
        basis = bone2np(posebone.bone, dtype=dtype, mode="rest")
        rot_scale = basis @ dynamic_pose if posebone.parent is None else posebone2np(
            posebone.parent, dtype=dtype, mode=mode) @ posebone2np(posebone, dtype=dtype, mode="offset")
        dynamic_pose = rot_scale @ dynamic_pose
        if posebone.parent is None:  # root node
            dynamic_pose[0:3, 3] = (basis @ location2np(posebone, dtype=dtype, to_matrix=True, frame=frame))[0:3, 3]
        return dynamic_pose  # equal to mat2np(posebone.matrix, dtype=dtype)
    else:
        raise NotImplementedError(f"mode {mode} isn't supported.")


def bone2np(bone: bpy.types.Bone,
            dtype: type = np.float32, mode: str = "rest",
            frame: int = bpy.context.scene.frame_current) -> np.ndarray:
    # Get bone in edit mode
    bpy.context.scene.frame_set(frame)
    if mode == "head":  # local head position from the origin of the object
        return vec2np(bone.head_local, dtype=dtype)
    elif mode == "tail":  # local tail position from the origin of the object
        return vec2np(bone.tail_local, dtype=dtype)
    elif mode == "length":  # bone length
        return bone.length
    elif mode == "offset":  # offset matrix from the parent
        offset = bone.matrix.to_4x4()
        offset.translation = bone.head
        if bone.parent is not None:
            offset.translation.y += bone.parent.length
        return mat2np(offset, dtype=dtype)
    elif mode == "rest":
        # absolute translation matrix not considering bones' rotation at rest pose
        return mat2np(bone.matrix_local, dtype=dtype)
    else:
        raise NotImplementedError(f"mode {mode} isn't supported.")


# --------------------------- Kinematic tree -------------------------------

def get_kinematic_tree(armature: bpy.types.Object):
    if type(armature.data) is bpy.types.Armature:
        armature = armature.data
    # Bone's parent index list (root node's parent idx: -1)
    return [-1 if bone.parent is None else list(armature.bones).index(bone.parent)
            for bone in armature.bones]


# -------------------------- Insert keyframes ------------------------------

def insert_keyframe_to_posebone(posebone: bpy.types.PoseBone, pose: np.ndarray, translation: np.ndarray = None,
                                frame: int = bpy.context.scene.frame_current,
                                rotation_mode: str = "rotation_axis_angle"):
    change_rotation_mode(posebone, rotation_mode, normalized=True)
    if translation is not None:
        insert_keyframe(posebone, translation, datapath="location", frame=frame)
    insert_keyframe(posebone, pose, datapath=rotation_mode, frame=frame)


def insert_keyframe_to_armature(armature: bpy.types.Object, poses: np.ndarray, translations: np.ndarray = None, frame: int = bpy.context.scene.frame_current,
                                rotation_mode: str = "rotation_axis_angle", exception_bone_indices: list = None,
                                only_root_translation: bool = True):
    change_rotation_modes_of_armature(armature, rotation_mode, normalized=True)
    exception_bone_indices = [] if exception_bone_indices is None else exception_bone_indices
    for idx, posebone in enumerate(armature.pose.bones):
        if idx in exception_bone_indices:
            continue
        translation = None if only_root_translation or translations is None else translations[idx]
        insert_keyframe_to_posebone(posebone, poses[idx], translation, frame=frame, rotation_mode=rotation_mode)


# -------------------------- Remove keyframes ------------------------------

def remove_keyframe_from_posebone(posebone: bpy.types.PoseBone, frame: int):
    remove_keyframe(posebone, frame)


def remove_keyframe_from_armature(armature: bpy.types.Object, frame: int, exception_bone_indices: list = None):
    exception_bone_indices = [] if exception_bone_indices is None else exception_bone_indices
    for idx, bone in enumerate(armature.pose.bones):
        if idx in exception_bone_indices:
            continue
        remove_keyframe_from_posebone(bone, frame)


def remove_keyframes_from_armature(armature: bpy.types.Armature, frames: int, exception_bone_indices: list = None):
    for frame in frames:
        remove_keyframe_from_armature(armature, frame, exception_bone_indices)


# --------------------------- Normalization ------------------------------


def change_rotation_modes_of_armature(armature: bpy.types.Object, rotation_mode: str, normalized: bool = True):
    change_rotation_mode(armature, rotation_mode, normalized)
    for posebone in armature.pose.bones:
        change_rotation_mode(posebone, rotation_mode, normalized)


def normalize_roll(armature: bpy.types.Object):
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    for bone in armature.data.edit_bones:
        bone.roll = 0.0
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
