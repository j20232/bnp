bnp.objects.base
=====================

..py:function:: batch_identity(batch_num, size, dtype=np.float32)

    Return batched identity matrices

    :param batch_num: number of the batch
    :param size: size of each matrix
    :param dtype: dtype
    :return: `np.ndarray` (batch_num, size, size)


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


.. py:function:: world_matrix2np(obj, dtype=np.float32, frame=bpy.context.scene.frame_current)

    Get world matrix of `bpy.types.Object` as `np.ndarray` (row major). This function is equal to `mat2np(obj.matrix_world)`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray` (worldmatrix; row major)


.. py:function:: location2np(obj, dtype=np.float32, to_matrix=False, frame=bpy.context.scene.frame_current)

    Get location of `bpy.types.Object` as `np.ndarray`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param bool to_matrix: whether to convert a location vector to a translation matrix
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray`  (4, 4) if to_matrix else (3)


.. py:function:: rotation2np(obj, dtype=np.float32, to_matrix=False, frame=bpy.context.scene.frame_current)

    Get rotation of `bpy.types.Object` as `np.ndarray`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param bool to_matrix: whether to convert a rotation vector to a translation matrix
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray` (4, 4) if to_matrix else {(3) (euler angle) or (4) (quaternion or axis angle)}


.. py:function:: scale2np(obj, dtype=np.float32, to_matrix=False, frame=bpy.context.scene.frame_current)

    Get scale of `bpy.types.Object` as `np.ndarray`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param bool to_matrix: whether to convert a scale vector to a translation matrix
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray` (4, 4) if to_matrix else (3)


.. py:function:: normalize_quaternion(q, eps=1e-10):

    Normalize input quaternions

    :param np.ndarray: quaternion: (4) or (num_of_quaternion, 4)
    :param float eps: epsilon to avoid zero-division
    :return: `np.ndarray` normalized quaternions (1, 4) or (num_of_quaternion, 4)


.. py:function:: normalize_axis_angle(a, eps=1e-10):

    Normalize input axis angles

    :param np.ndarray: axis angles: (4) or (num_of_quaternion, 4)
    :param float eps: epsilon to avoid zero-division
    :return: `np.ndarray` normalized axis angles (1, 4) or (num_of_axis_angles, 4)


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


.. py:function:: remove_keyframe(obj, frame)

    Remove the specified keyframe from obj
    
    :param obj: `bpy.types.Object` or `bpy.types.PoseBone`
    :param int frame: the frame
