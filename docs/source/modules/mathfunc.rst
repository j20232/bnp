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
