bnp.objects.armature
=====================


.. py:function:: posebone_basis(dtype=np.float32) -> np.ndarray

    Return Blender's posebone basis (equal to bone.matrix_basis) to adjust a bone's rotation

    :param dtype: dtype
    :return: `np.ndarray` basis


.. py:function:: armature2np(armature, dtype=np.float32, mode="dynamic", frame=bpy.context.scene.frame_current) -> np.ndarray

    Convert a `bpy.types.Object` which has `bpy.types.Armature` to `np.ndarray` at current frame.

    :param bpy.types.Object armature: armature which has `bpy.types.Armature`
    :param dtype: dtype
    :param str mode: "head" or "tail": local head/tail positions (`joint_num`, 3), "length": bone lengths (`joint_num`,), "offset": bone offset translation matices (`joint_num`, 4, 4),"rest" / "dynamic": absolute translation matrices at rest pose / the frame, "rotation": pose vectors
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray`


.. py:function:: posebone2np(posebone, dtype=np.float32, mode="dynamic", frame=bpy.context.scene.frame_current) -> np.ndarray

    Get posebone as `np.ndarray`.

    :param bpy.types.PoseBone posebone: posebone
    :param dtype: dtype
    :param str mode: "head" or "tail": local head/tail positions (`joint_num`, 3), "length": bone lengths (`joint_num`,), "offset": offset matrix from the parent (4, 4), "dynamic": absolute translation matrices at the frame
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray`


.. py:function:: bone2np(bone, dtype=np.float32, mode="rest", frame=bpy.context.scene.frame_current) -> np.ndarray

    Get bone as `np.ndarray`.

    :param bpy.types.Bone bone: bone
    :param dtype: dtype
    :param str mode: "head" or "tail": local head/tail positions (`joint_num`, 3), "length": bone lengths (`joint_num`,), "offset": offset matrix from the parent (4, 4), "rest": absolute translation matrices at rest pose
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray`


.. py:function:: get_kinematic_tree(armature: bpy.types.Object) -> list

    Get a kinematic tree as a list (index: bone index, value: parent index)

    :param armature: `bpy.types.Object` or `bpy.types.Armature`


.. py:function:: insert_keyframe_to_posebone(posebone, pose, translation=None, frame=bpy.context.scene.frame_current, rotation_mode="rotation_axis_angle")

    Insert a keyframe to a posebone

    :param bpy.types.PoseBone posebone: posebone
    :param np.ndarray pose: pose (3) or (4)
    :param np.ndarray translation: translation (3), (4) or None
    :param int frame: keyframe
    :param str rotation_mode: "rotation_axis_angle" (equal to "AXIS_ANGLE"), "rotation_quaternion" (equal to "QUATERNION") or "rotation_euler" (equal to "XYZ")


.. py:function:: insert_keyframe_to_armature(armature, poses, translations=None, frame=bpy.context.scene.frame_current, rotation_mode="rotation_axis_angle", exception_bone_indices=None, only_root_translation=True)

    Insert a keyframe to an harmature

    :param bpy.types.Object armature: armature which has `bpy.types.Armature`
    :param np.ndarray poses: poses (num_of_joints, 3) or (num_of_joints, 4)
    :param np.ndarray translations: translations (num_of_joints, 3), (1, 3) or None
    :param int frame: keyframe
    :param str rotation_mode: "rotation_axis_angle" (equal to "AXIS_ANGLE"), "rotation_quaternion" (equal to "QUATERNION") or "rotation_euler" (equal to "XYZ")
    :param list exception_bone_indices: bone indices not to insert keyframes
    :param bool only_root_translation: whether to insert only root translation or not


.. py:function:: remove_keyframe_from_posebone(posebone, frame, exception_bone_indices=None)

    Remove a keyframe from an input posebone

    :param bpy.types.PoseBone posebone: posebone
    :param int frame: frame


.. py:function:: remove_keyframe_from_armature(armature, frame, exception_bone_indices=None)

    Remove a keyframe from an input armature

    :param bpy.types.Object armature: armature which has `bpy.types.Armature`
    :param int frame: frame
    :param list exception_bone_indices: bone index list not to remove keyframes (optional)


.. py:function:: remove_keyframes_from_armature(armature, frames, exception_bone_indices=None)

    Remove a keyframe from an input armature

    :param bpy.types.Object armature: armature which has `bpy.types.Armature`
    :param list frames: frame list
    :param list exception_bone_indices: bone index list not to remove keyframes (optional)


.. py:function:: change_rotation_modes_of_armature(armature, rotation_mode, normalized=True)

    Change rotation modes of an input armature and posebones in the armature

    :param bpy.types.Object armature: armature which has `bpy.types.Armature`
    :param str rotation_mode: "rotation_axis_angle" (equal to "AXIS_ANGLE"), "rotation_quaternion" (equal to "QUATERNION") or "rotation_euler" (equal to "XYZ")
    :param bool normalized: whether to normalize axis_angle or quaternion


.. py:function:: normalize_roll(armature: bpy.types.Object)

    Normalize bones' rolls

    :param bpy.types.Object obj: object which has `bpy.types.Armature`
