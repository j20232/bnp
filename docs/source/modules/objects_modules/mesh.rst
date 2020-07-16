bnp.objects.mesh
=====================

.. py:function:: mesh2np(mesh: bpy.types.Mesh, world_matrix=None, geo_type="position", dtype=np.float32, is_local=False, frame=bpy.context.scene.frame_current, as_homogeneous=False) -> np.ndarray

    Convert a `bpy.types.Mesh` to  `np.ndarray` at current frame.

    :param bpy.types.Mesh mesh: input mesh
    :param np.ndarray world_matrix: world matrix (equal to model matrix)
    :param str geo_type: "position" or "normal"
    :param dtype: dtype
    :param bool is_local: return local positions if is_local else global positions
    :param int frame: frame when you want to read (default: current frame)
    :param bool as_homogeneous: whether to return vertices as homogeneous coordinates or not
    :return: `np.ndarray` (vertex_number, 3) or (vertex_number, 4)


.. py:function:: skinning_weights2np(obj: bpy.types.Object, dtype=np.float32) -> np.ndarray

    Get skinning weights (vertex weights in Blender) as `np.ndarray`

    :param bpy.types.Object obj: object which has `bpy.types.Mesh`
    :param dtype: dtype
    :return: `np.ndarray` skinning weights (vtx_num, joint_num)


.. py:function:: get_active_indices(obj: bpy.types.Object)

    Get active indices from the mesh of the input obj

    :param bpy.types.Object obj: object which has `bpy.types.Mesh`
