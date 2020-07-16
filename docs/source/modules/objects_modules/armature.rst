bnp.conversion
=====================


.. py:function:: armature2np(armature, dtype=np.float32, mode="dynamic", frame=bpy.context.scene.frame_current)

    Convert a `bpy.types.Armature` to `np.ndarray` at current frame.

    :param bpy.types.Armature armature: armature
    :param dtype: dtype
    :param str mode: "head" or "tail": local head/tail positions (`joint_num`, 3), "length": bone lengths (`joint_num`,), "rest_from_origin" or "dynamic_from_origin": absolute translation matrices at rest pose / the frame considering bones' initial translation (joint_num, 4, 4), "rest_relative" / "dynamic_relative": translation matices relative to parents not considering intiial translation (joint_num, 4, 4), "rest" / "dynamic": absolute translation matrices at rest pose / the frame not considering bones' initial translation
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray`


.. py:function:: get_posebone_as_np(posebone, dtype=np.float32, mode="dynamic", frame=bpy.context.scene.frame_current)

    Get posebone as `np.ndarray`.

    :param bpy.types.PoseBone posebone: posebone
    :param dtype: dtype
    :param str mode: "head" or "tail": local head/tail positions (`joint_num`, 3), "length": bone lengths (`joint_num`,), "dynamic_from_origin": absolute translation matrices at the frame considering bones' initial translation (joint_num, 4, 4), "dynamic_relative": translation matices relative to parents not considering intiial translation (joint_num, 4, 4), "dynamic": absolute translation matrices at the frame not considering bones' initial translation
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray`


.. py:function:: get_bone_as_np(bone, dtype=np.float32, mode="rest", frame=bpy.context.scene.frame_current)

    Get bone as `np.ndarray`.

    :param bpy.types.Bone bone: bone
    :param dtype: dtype
    :param str mode: "head" or "tail": local head/tail positions (`joint_num`, 3), "length": bone lengths (`joint_num`,), "rest_from_origin": absolute translation matrices at rest pose considering bones' initial translation (joint_num, 4, 4), "rest_relative": translation matices relative to parents not considering intiial translation (joint_num, 4, 4), "rest": absolute translation matrices at rest pose not considering bones' initial translation
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray`


.. py:function:: normalize_armature(armature: bpy.types.Object)

    Normalize bones' rolls

    :param bpy.types.Object obj: object which has `bpy.types.Armature`
