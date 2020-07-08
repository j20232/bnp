bnp.conversion
=====================

.. py:function:: any2np(obj, dtype=np.float32, is_local=False)

    Convert any objects in Blender to `np.ndarray`

    :param obj: any object such as `mathutils.Vector`, `mathutils.Matrix`, and so on
    :param dtype: dtype
    :param bool is_local: return local positions if is_local else global positions
    :return: np.ndarray


.. py:function:: vec2np(vec, dtype=np.float32)

    Convert a vector such as `mathutils.Vector` to `np.ndarray`

    :param vec: vector
    :param dtype: dtype
    :return: np.ndarray


.. py:function:: mat2np(mat, dtype=np.float32)

    Convert a matrix such as `mathutils.Matrix` to `np.ndarray`

    :param vec: matrix
    :param dtype: dtype
    :return: np.ndarray


.. py:function:: obj2np(obj, geo_type="position", dtype=np.float32, is_local=False)

    Convert a `bpy.types.Object` which have a mesh to `np.ndarray`

    :param bpy.types.Object obj: object which have a mesh
    :param str geo_type: "position" or "normal"
    :param dtype: dtype
    :param bool is_local: return local positions if is_local else global positions
    :return: np.ndarray (vertex_number, 3)


.. py:function:: objname2np(obj_name, geo_type="position", dtype=np.float32, is_local=False)

    Get `bpy.types.Object` in the Scene which have a mesh and convert it to `np.ndarray`

    :param str obj_name: object name
    :param str geo_type: "position" or "normal"
    :param dtype: dtype
    :param bool is_local: return local positions if is_local else global positions
    :return: np.ndarray (vertex_number, 3)


.. py:function:: mesh2np(mesh, geo_type="position", dtype=np.float32, is_local=False)

    Convert a `bpy.types.Mesh` to  `np.ndarray`

    :param bpy.types.Mesh mesh: input mesh
    :param str geo_type: "position" or "normal"
    :param dtype: dtype
    :param bool is_local: return local positions if is_local else global positions
    :return: np.ndarray (vertex_number, 3)

