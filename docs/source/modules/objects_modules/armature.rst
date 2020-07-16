bnp.objects.armature
=====================


.. py:function:: posebone_basis(dtype=np.float32) -> np.ndarray

    Return Blender's posebone basis (equal to bone.matrix_basis) to adjust a bone's rotation

    :param dtype: dtype
    :return: `np.ndarray` basis


.. py:function:: armature2np(armature, dtype=np.float32, mode="dynamic", frame=bpy.context.scene.frame_current, rotation_mode=None) -> np.ndarray

    Convert a `bpy.types.Object` which has `bpy.types.Armature` to `np.ndarray` at current frame.

    :param bpy.types.Object armature: armature which has `bpy.types.Armature`
    :param dtype: dtype
    :param str mode: "head" or "tail": local head/tail positions (`joint_num`, 3), "length": bone lengths (`joint_num`,), "rest" / "dynamic": absolute translation matrices at rest pose / the frame, "rotation": pose vectors
    :param int frame: frame when you want to read (default: current frame)
    :param str rotation_mode: the type of pose vectors. ("QUATERNION", "AXIS_ANGLE", "XYZ", "XZY", ... "ZYX")
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


.. py:function:: remove_keyframe_from_armature(armature, frame, exception_bone_indices=None)

    Remove a keyframe from an input armature

    :param bpy.types.Object armature: armature
    :param int frame: frame
    :param list exception_bone_indices: bone index list not to remove keyframes (optional)


.. py:function:: normalize_roll(armature: bpy.types.Object)

    Normalize bones' rolls

    :param bpy.types.Object obj: object which has `bpy.types.Armature`
