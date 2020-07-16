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


.. py:function:: normalize_skinning_weights(obj: bpy.types.Object) -> bpy.types.Mesh

    Get a mesh after normalization of skinning weights (vertex weights in Blender)

    :param bpy.types.Object obj: object which has `bpy.types.Mesh`
    :return: `bpy.types.Mesh` mesh after normalization of skinning weights


.. py:function:: get_active_vertex_indices(obj: bpy.types.Object) -> list

    Get active vertex indices from the mesh of the input obj

    :param bpy.types.Object obj: object which has `bpy.types.Mesh`


.. py:function:: remove_shape_keys(obj, all=True)

    Remove the selected shape key (blend weight). If all == true, remove all shape keys from obj

    :param bpy.types.Object obj: object which has `bpy.types.Mesh`


.. py:function:: add_shape_keys(obj, name, blend_weight=1.0, vertices=None, slider_min=0.0, slider_max=1.0, from_mix=False)

    Add a shape key (blend weight) to obj

    :param bpy.types.Object obj: object which has `bpy.types.Mesh`
    :param str name: name of the shape key. Any name is ok.
    :param float blend_weight: blend weight
    :param np.ndarray vertices: vertex positions (vtx_num, 3). None: vertex positions won't be changed.
    :param float slider_min: minimum value of the blend weight
    :param float slider_max: maximum value of the blend weight
    :param bool from_mix: create new shape from existing mix of shapes (see: https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.shape_key_add)


.. py:function:: adjust_shape_key(obj, name, blend_weight, vertices=None)

    Adjust the value and vertices of the shape key

    :param bpy.types.Object obj: object which has `bpy.types.Mesh`
    :param str name: name of the shape key
    :param float blend_weight: blend weight
    :param np.ndarray vertices: vertex positions (vtx_num, 3). None: vertex positions won't be changed.


.. py:function:: insert_keyframes_to_shape_keys(obj, blend_weights)

    Insert keyframes to shape keys (blend weights)

    :param bpy.types.Object obj: object which has `bpy.types.Mesh` and shapekeys
    :param dict blend_weights: dictionary like {FRAME: {SHAPE_KEY_NAME1: 1.0, SHAPE_KEY_NAME2: 0.0}} where `FRAME` should be `str(int(target_frame))`, `SHAPE_KEY_NAME1` and `SHAPE_KEY_NAME2` should be names of shape keys. Please check example 003.

.. py:function:: get_keyframe_of_shapekeys(obj)

    Get a sorted list which contains keyframes of obj's shape keys(blend weights). If there is no keyframes, return an empty list.

    :param bpy.types.Object obj: obj
    :return: `list` sorted with keyframes (no duplication)
