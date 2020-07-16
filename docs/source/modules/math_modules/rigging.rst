bnp.math.rigging
=====================


.. py:function:: linear_blend_skinning(vertices, rest_pose, dynamic_pose, skinning_weights)

    Calculate new vertex positions with Linear Blend Skinning

    :param np.ndarray vertices: homogeneous vertex positions (vtx_num, 4)
    :param np.ndarray rest_pose: translation matices at rest pose (joint_num, 4, 4)
    :param np.ndarray dynamic_pose: translation matrices at a specified frame (joint_num, 4, 4)
    :param np.ndarray skinning_weights: skinning weights (equal to vertex weights) (vtx_num, joint_num)
    :return: `np.ndarray` new vertex positions at homogeneous coordinates (vtx_num, 4)
