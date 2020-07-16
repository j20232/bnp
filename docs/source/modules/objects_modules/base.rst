bnp.objects.base
=====================

.. py:function:: vec2np(vec, dtype=np.float32)

    Convert a vector such as `mathutils.Vector` to `np.ndarray`.

    :param vec: vector
    :param dtype: dtype
    :return: `np.ndarray` (vector_size)


.. py:function:: mat2np(mat, dtype=np.float32)

    Convert a matrix such as `mathutils.Matrix` to `np.ndarray`.

    :param vec: matrix
    :param dtype: dtype
    :return: Row-major `np.ndarray` (matrix_size)


.. py:function:: quaternion2R(q, dtype=np.float32, eps=1e-10)

    Convert quaternions to rotation matrices
    
    :param np.ndarray q: quaternion (num_of_quaternion, 4)
    :param dtype: dtype
    :param float eps: epsilon to avoid zero-division
    :return: `np.ndarray` rotation matrices (num_of_quaternion, 4, 4)


.. py:function:: axis_angle2R(a, dtype=np.float32, eps=1e-10)

    Convert axis angles to rotation matrices
    
    :param np.ndarray a: axis angles (num_of_axis_angles, 4)
    :param dtype: dtype
    :param float eps: epsilon to avoid zero-division
    :return: `np.ndarray` rotation matrices (num_of_axis_angles, 4, 4)


.. py:function:: euler2R(e, dtype=np.float32, eps=1e-10)

    Convert euler angles to rotation matrices
    
    :param np.ndarray e: euler angles (num_of_euler_angles, 3)
    :param dtype: dtype
    :param float eps: epsilon to avoid zero-division
    :return: `np.ndarray` rotation matrices (num_of_euler_angles, 4, 4)


.. py:function:: get_world_matrix_as_np(obj, dtype=np.float32, frame=bpy.context.scene.frame_current, change_frame=True)

    Get world matrix of `bpy.types.Object` as `np.ndarray` (row major). This function is equal to `mat2np(obj.matrix_world)`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray` (worldmatrix; row major)


.. py:function:: get_location_as_np(obj, dtype=np.float32, to_matrix=False, frame=bpy.context.scene.frame_current)

    Get location of `bpy.types.Object` as `np.ndarray`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param bool to_matrix: whether to convert a location vector to a translation matrix
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray`  (4, 4) if to_matrix else (3)


.. py:function:: get_rotation_as_np(obj, dtype=np.float32, to_matrix=False, frame=bpy.context.scene.frame_current)

    Get rotation of `bpy.types.Object` as `np.ndarray`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param bool to_matrix: whether to convert a rotation vector to a translation matrix
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray` (4, 4) if to_matrix else {(3) (euler angle) or (4) (quaternion or axis angle)}


.. py:function:: get_scale_as_np(obj, dtype=np.float32, to_matrix=False, frame=bpy.context.scene.frame_current)

    Get scale of `bpy.types.Object` as `np.ndarray`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param bool to_matrix: whether to convert a scale vector to a translation matrix
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray` (4, 4) if to_matrix else (3)
