bnp.conversion
=====================

.. py:function:: any2np(obj, dtype=np.float32, **kwargs)

    Convert any objects in Blender to `np.ndarray` at current frame.

    :param obj: any object such as `mathutils.Vector`, `mathutils.Matrix`, and so on
    :param dtype: dtype
    :param kwargs: other attrs
    :return: `np.ndarray`


.. py:function:: vec2np(vec, dtype=np.float32)

    Convert a vector such as `mathutils.Vector` to `np.ndarray`.

    :param vec: vector
    :param dtype: dtype
    :return: `np.ndarray`


.. py:function:: mat2np(mat, dtype=np.float32)

    Convert a matrix such as `mathutils.Matrix` to `np.ndarray`.

    :param vec: matrix
    :param dtype: dtype
    :return: `np.ndarray` (row major)


.. py:function:: obj2np(obj, dtype=np.float32, **kwargs)

    Convert a `bpy.types.Object` which have a mesh to `np.ndarray` at current frame.
    If obj.data == bpy.types.Mesh, this method calls `mesh2np`.

    :param bpy.types.Object obj: object which have a mesh
    :param dtype: dtype
    :param kwargs: other attrs
    :return: `np.ndarray` (vertex_number, 3) or (vertex_number, 4)


.. py:function:: objname2np(obj_name, dtype=np.float32, **kwargs)

    Get `bpy.types.Object` in the Scene which have a mesh and convert it to `np.ndarray` at current frame.
    This method calls `obj2np`

    :param str obj_name: object name
    :param dtype: dtype
    :param kwargs: other attrs
    :return: `np.ndarray` (vertex_number, 3) or (vertex_number, 4)


.. py:function:: mesh2np(mesh, geo_type="position", dtype=np.float32, is_local=False, frame=bpy.context.scene.frame_current, change_frame=True, as_homogeneous=False)

    Convert a `bpy.types.Mesh` to  `np.ndarray` at current frame.

    :param bpy.types.Mesh mesh: input mesh
    :param str geo_type: "position" or "normal"
    :param dtype: dtype
    :param bool is_local: return local positions if is_local else global positions
    :param int frame: frame when you want to read (default: current frame)
    :param bool change_frame: whether to keep the frame after getting the array
    :param bool as_homogeneous: whether to return vertices as homogeneous coordinates or not
    :return: `np.ndarray` (vertex_number, 3)


.. py:function:: get_world_matrix_as_np(obj, dtype=np.float32, frame=bpy.context.scene.frame_current, change_frame=True)

    Get world matrix of `bpy.types.Object` as `np.ndarray` (row major).

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param int frame: frame when you want to read (default: current frame)
    :param bool change_frame: whether to keep the frame after getting the array
    :return: `np.ndarray` (worldmatrix; row major)


.. py:function:: get_location_as_np(obj, dtype=np.float32, frame=bpy.context.scene.frame_current, change_frame=True)

    Get location of `bpy.types.Object` as `np.ndarray`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param int frame: frame when you want to read (default: current frame)
    :param bool change_frame: whether to keep the frame after getting the array
    :return: `np.ndarray` (location)


.. py:function:: get_rotation_as_np(obj, dtype=np.float32, mode="DEFAULT", frame=bpy.context.scene.frame_current, change_frame=True)

    Get rotation of `bpy.types.Object` as `np.ndarray`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param str mode: "DEFAULT" (current rotation mode), "QUATERNION", "AXIS_ANGLE", others(rotation_euler)
    :param int frame: frame when you want to read (default: current frame)
    :param bool change_frame: whether to keep the frame after getting the array
    :return: `np.ndarray` (rotation)


.. py:function:: get_scale_as_np(obj, dtype=np.float32, frame=bpy.context.scene.frame_current, change_frame=True)

    Get scale of `bpy.types.Object` as `np.ndarray`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param int frame: frame when you want to read (default: current frame)
    :param bool change_frame: whether to keep the frame after getting the array
    :return: `np.ndarray` (scale)
