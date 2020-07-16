import bpy
import numpy as np
from bnp.objects.base import vec2np, mat2np, location2np, rotation2np
from bnp.objects.base import normalize_axis_angle
from bnp.objects.base import remove_keyframe

# ----------------------------------- Conversion -----------------------------------------


def posebone_basis(dtype=np.float32):
    return np.array([1.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, -1.0, 0.0,
                     0.0, 1.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 1.0], dtype=dtype).reshape(4, 4)


def armature2np(armature: bpy.types.Object, dtype=np.float32, mode="dynamic",
                frame=bpy.context.scene.frame_current, rotation_mode=None) -> np.ndarray:
    normalize_roll(armature)
    if mode in ["head", "tail", "length", "rest"]:
        return np.array([bone2np(
            p.bone, dtype=dtype, mode=mode, frame=frame) for p in list(armature.pose.bones)], dtype=dtype)
    elif mode in ["dynamic"]:
        return np.array([posebone2np(
            p, dtype=dtype, mode=mode, frame=frame) for p in list(armature.pose.bones)], dtype=dtype)
    elif mode in ["rotation"]:
        return np.array([rotation2np(p, rotation_mode=rotation_mode, dtype=dtype, frame=frame) for p in list(armature.pose.bones)], dtype=dtype)
    else:
        raise NotImplementedError(f"Not supported the mode {mode}.")


def posebone2np(posebone,
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
    elif mode == "offset":  # offset matrix from the parent
        return bone2np(posebone.bone, dtype=dtype, mode=mode, frame=frame)
    elif mode == "dynamic":
        dynamic_pose = rotation2np(posebone, dtype=dtype, to_matrix=True, frame=frame)
        basis = posebone_basis(dtype=dtype)
        rot_scale = basis if posebone.parent is None else posebone2np(
            posebone.parent, dtype=dtype, mode=mode) @ posebone2np(posebone, dtype=dtype, mode="offset")
        dynamic_pose = rot_scale @ dynamic_pose
        if posebone.parent is None:  # root node
            dynamic_pose[0:3, 3] = (basis @ location2np(posebone, dtype=dtype, to_matrix=True, frame=frame))[0:3, 3]
        return dynamic_pose  # equal to mat2np(posebone.matrix, dtype=dtype)
    else:
        raise NotImplementedError(f"mode {mode} isn't supported.")


def bone2np(bone,
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
    elif mode == "offset":  # offset matrix from the parent
        offset = bone.matrix.to_4x4()
        offset.translation = bone.head
        if bone.parent is not None:
            offset.translation.y += bone.parent.length
        return mat2np(offset, dtype=dtype)
    elif mode == "rest":
        # absolute translation matrix
        # not considering bones' rotation at rest pose
        # equal to mat2np(bone.matrix_local, dtype=dtype)
        return posebone_basis(dtype) if bone.parent is None else bone2np(bone.parent, dtype=dtype, mode="rest", frame=frame) @ bone2np(bone, dtype=dtype, mode="offset", frame=frame)
    else:
        raise NotImplementedError(f"mode {mode} isn't supported.")


# --------------------------- Kinematic tree -------------------------------

def get_kinematic_tree(armature):
    if type(armature.data) is bpy.types.Armature:
        armature = armature.data
    # Bone's parent index list (root node's parent idx: -1)
    return [-1 if bone.parent is None else list(armature.bones).index(bone.parent)
            for bone in armature.bones]

# -------------------------- Remove keyframes ------------------------------


def remove_keyframe_from_armature(armature, frame, exception_bone_indices=None):
    exception_bone_indices = [] if exception_bone_indices is None else exception_bone_indices
    for idx, bone in enumerate(armature.pose.bones):
        if idx in exception_bone_indices:
            continue
        remove_keyframe(bone, frame)

# --------------------------- Normalization ------------------------------


def change_bone_rotation_mode(armature, mode, normalized=True):
    armature.rotation_mode = mode
    for bone in armature.pose.bones:
        q = normalize_axis_angle(bone.rotation_axis_angle)
        print(q)
        assert False
        bone.rotation_mode = mode


def normalize_roll(armature: bpy.types.Object):
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    for bone in armature.data.edit_bones:
        bone.roll = 0.0
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
