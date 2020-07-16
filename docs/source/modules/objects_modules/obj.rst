bnp.objects.obj
=====================

.. py:function:: any2np(obj, dtype=np.float32, **kwargs) -> np.ndarray

    Convert any objects in Blender to `np.ndarray` at current frame.

    :param obj: any object such as `mathutils.Vector`, `mathutils.Matrix`, `bpy.types.Object`, `bpy.types.Mesh` or str (name of an object in the Scene)
    :param dtype: dtype
    :param kwargs: other attrs
    :return: `np.ndarray`


.. py:function:: obj2np(obj: bpy.types.Object, dtype=np.float32, apply_modifier=False, frame=bpy.context.scene.frame_current, geo_type="position", is_local=False, as_homogeneous=False, mode="dynamic") -> np.ndarray

    Convert a `bpy.types.Object` which have a mesh to `np.ndarray` at current frame.
    If obj.data == bpy.types.Mesh, this method calls `mesh2np` or `armature2np`.

    :param bpy.types.Object obj: object which have a mesh
    :param dtype: dtype
    :param bool apply_modifier: whether to apply modifiers
    :param int frame: frame when you want to get matrices
    :param str geo_type: "position" or "normal". This is used when `obj.data == bpy.types.Mesh`.
    :param bool is_local: whether to get positions as local coordinates. This is used when `obj.data == bpy.types.Mesh`.
    :param bool as_homogeneous: whether to get positions as homogeneous or not. This is used when `obj.data == bpy.types.Mesh`.
    :param str mode: "head", "tail", "length", "rest", "dynamic".  This is used when `obj.data == bpy.types.Armature`.
    :return: `np.ndarray`


.. py:function:: objname2np(obj_name: str, dtype=np.float32, apply_modifier=False, frame=bpy.context.scene.frame_current, geo_type="position", is_local=False, as_homogeneous=False, mode="dynamic") -> np.ndarray

    Get `bpy.types.Object` in the Scene which have a mesh and convert it to `np.ndarray` at current frame.
    This method calls `obj2np`.

    :param str obj_name: object name in the Scene
    :param dtype: dtype
    :param bool apply_modifier: whether to apply modifiers
    :param int frame: frame when you want to get matrices
    :param str geo_type: "position" or "normal". This is used when `obj.data == bpy.types.Mesh`.
    :param bool is_local: whether to get positions as local coordinates. This is used when `obj.data == bpy.types.Mesh`.
    :param bool as_homogeneous: whether to get positions as homogeneous or not. This is used when `obj.data == bpy.types.Mesh`.
    :param str mode: "head", "tail", "length", "rest", "dynamic". This is used when `obj.data == bpy.types.Armature`.
    :return: `np.ndarray`
