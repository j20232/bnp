bnp.objects.base
=====================


.. py:function:: batch_identity(batch_num, size, dtype=np.float32) -> np.ndarray

    Return batched identity matrices

    :param batch_num: number of the batch
    :param size: size of each matrix
    :param dtype: dtype
    :return: `np.ndarray` (batch_num, size, size)


.. py:function:: vec2np(vec, dtype=np.float32) -> np.ndarray

    Convert a vector such as `mathutils.Vector` to `np.ndarray`.

    :param vec: vector
    :param dtype: dtype
    :return: `np.ndarray` (vector_size)


.. py:function:: mat2np(mat, dtype=np.float32) ->np.ndarray

    Convert a matrix such as `mathutils.Matrix` to `np.ndarray`.

    :param vec: matrix
    :param dtype: dtype
    :return: Row-major `np.ndarray` (matrix_size)


.. py:function:: vertices2np(vertices, dtype=np.float32) -> np.ndarray

    Convert vertices (`bpy.types.bpy_prop_collection` or `bmesh.types.BMVertSeq`) to `np.ndarray`

    :param vertices: `bpy.types.bpy_prop_collection` or `bmesh.types.BMVertSeq`
    :param dtype: dtype
    :return: `np.ndarray` (vtx_num, 3)


.. py:function:: collection2np(obj, dtype=np.float32) -> np.ndarray

    Convert vertices (`bpy.types.bpy_prop_collection`) to `np.ndarray`

    :param obj: `bpy.types.bpy_prop_collection`
    :param dtype: dtype
    :return: `np.ndarray` (vtx_num, 3)
   

.. py:function:: world_matrix2np(obj, dtype=np.float32, frame=bpy.context.scene.frame_current) -> np.ndarray

    Get world matrix of `bpy.types.Object` as `np.ndarray` (row major). This function is equal to `mat2np(obj.matrix_world)`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray` (worldmatrix; row major)


.. py:function:: location2np(obj, dtype=np.float32, to_matrix=False, frame=bpy.context.scene.frame_current) -> np.ndarray

    Get location of `bpy.types.Object` as `np.ndarray`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param bool to_matrix: whether to convert a location vector to a translation matrix
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray`  (4, 4) if to_matrix else (3)


.. py:function:: rotation2np(obj, dtype=np.float32, to_matrix=False, frame=bpy.context.scene.frame_current, convert_axis_4to3=False) -> np.ndarray

    Get rotation of `bpy.types.Object` as `np.ndarray`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param bool to_matrix: whether to convert a rotation vector to a translation matrix
    :param int frame: frame when you want to read (default: current frame)
    :param bool convert_axis_4to3: whether to convert the dimension of axis angles from 4 to 3 (same as SMPL context)
    :return: `np.ndarray` (4, 4) if to_matrix else {(3) (euler angle) or (4) (quaternion or axis angle)}


.. py:function:: scale2np(obj, dtype=np.float32, to_matrix=False, frame=bpy.context.scene.frame_current) -> np.ndarray

    Get scale of `bpy.types.Object` as `np.ndarray`.

    :param bpy.types.Object obj: object
    :param dtype: dtype
    :param bool to_matrix: whether to convert a scale vector to a translation matrix
    :param int frame: frame when you want to read (default: current frame)
    :return: `np.ndarray` (4, 4) if to_matrix else (3)


.. py:function:: normalize_quaternion(q, eps=1e-10) -> np.ndarray

    Normalize input quaternions

    :param np.ndarray: quaternion: (4) or (num_of_quaternion, 4)
    :param float eps: epsilon to avoid zero-division
    :return: `np.ndarray` normalized quaternions (1, 4) or (num_of_quaternion, 4)


.. py:function:: normalize_axis_angle(a, eps=1e-10) -> np.ndarray

    Normalize input axis angles

    :param np.ndarray: axis angles: (4) or (num_of_quaternion, 4)
    :param float eps: epsilon to avoid zero-division
    :return: `np.ndarray` normalized axis angles (1, 4) or (num_of_axis_angles, 4)


.. py:function:: axis_angle_4to3(a, eps=1e-10) -> np.ndarray

    Convert the dimension of axis angles from 4 to 3 (same as SMPL context)

    :param np.ndarray: axis angles: (4) or (num_of_quaternion, 4)
    :param float eps: epsilon to avoid zero-division
    :return: `np.ndarray` normalized axis angles (1, 3) or (num_of_axis_angles, 3)


.. py:function:: axis_angle_3to4(a, eps=1e-10) -> np.ndarray

    Convert the dimension of axis angles from 3 to 4 (same as SMPL context)

    :param np.ndarray: axis angles: (3) or (num_of_quaternion, 3)
    :param float eps: epsilon to avoid zero-division
    :return: `np.ndarray` normalized axis angles (1, 4) or (num_of_axis_angles, 4)


.. py:function:: quaternion2R(q, dtype=np.float32, eps=1e-10) -> np.ndarray

    Convert quaternions to rotation matrices
    
    :param np.ndarray q: quaternion (num_of_quaternion, 4)
    :param dtype: dtype
    :param float eps: epsilon to avoid zero-division
    :return: `np.ndarray` rotation matrices (num_of_quaternion, 4, 4)


.. py:function:: axis_angle2R(a, dtype=np.float32, eps=1e-10) -> np.ndarray

    Convert axis angles to rotation matrices
    
    :param np.ndarray a: axis angles (num_of_axis_angles, 4)
    :param dtype: dtype
    :param float eps: epsilon to avoid zero-division
    :return: `np.ndarray` rotation matrices (num_of_axis_angles, 4, 4)


.. py:function:: euler2R(e, dtype=np.float32, eps=1e-10) -> np.ndarray

    Convert euler angles to rotation matrices
    
    :param np.ndarray e: euler angles (num_of_euler_angles, 3)
    :param dtype: dtype
    :param float eps: epsilon to avoid zero-division
    :return: `np.ndarray` rotation matrices (num_of_euler_angles, 4, 4)


.. py:function:: change_rotation_mode(obj, rotation_mode, normalized=True)

    Change current rotation mode of obj

    :param bpy.types.Object obj: object
    :param str rotation_mode: "rotation_axis_angle" (equal to "AXIS_ANGLE"), "rotation_quaternion" (equal to "QUATERNION") or "rotation_euler" (equal to "XYZ")
    :param bool normalized: whether to normalize axis_angle or quaternion


.. py:function:: get_keyframe_list(obj)

    Get a sorted list which contains keyframes of obj. If there is no keyframes, return an empty list.

    :param bpy.types.Object obj: obj
    :return: `list` sorted with keyframes (no duplication)


.. py:function:: insert_keyframe(obj, vec: np.ndarray, datapath: str, frame=bpy.context.scene.frame_current) -> np.ndarray

    Insert keyframe to datapath in the frame

    :param bpy.types.Object obj: obj
    :param np.ndarray vec: location: (3), "rotation": (4) or (3) (radian), "scale": (3)
    :param str datapath: "location", "rotation", "scale", "rotation_euler", "rotation_quaternion" or "rotation_axis_angle". In "rotation", this method inserts the vec to current rotation mode.
    :param int frame: frame


.. py:function:: remove_keyframe(obj, frame)

    Remove the specified keyframe from obj
    
    :param obj: `bpy.types.Object` or `bpy.types.PoseBone`
    :param int frame: the frame


.. py:function:: remove_keyframes(obj, frames)

    Remove the specified keyframes from obj
    
    :param obj: `bpy.types.Object` or `bpy.types.PoseBone`
    :param list frames: frame list
