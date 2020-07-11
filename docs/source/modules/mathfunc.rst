bnp.mathfunc
=====================

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


.. py:function:: linear_blend_skinning(vertices, rest_pose, dynamic_pose, skinning_weights)

    Calculate new vertex positions with Linear Blend Skinning

    :param np.ndarray vertices: homogeneous vertex positions (vtx_num, 4)
    :param np.ndarray rest_pose: translation matices at rest pose (joint_num, 4, 4)
    :param np.ndarray dynamic_pose: translation matrices at a specified frame (joint_num, 4, 4)
    :param np.ndarray skinning_weights: skinning weights (equal to vertex weights) (vtx_num, joint_num)
    :return: `np.ndarray` new vertex positions at homogeneous coordinates (vtx_num, 4)
