bnp.math.rigging
=====================



.. py:function:: linear_blend_skinning(vertices, rest_pose, dynamic_pose, skinning_weights) -> np.ndarray

    Calculate new vertex positions with Linear Blend Skinning. Green box is deformed with Blender's LBS, white boxes are vertex positions calculated with this LBS.

    .. image:: ../../../../assets/screenshots/lbs.png
        :scale: 100%
        :height: 600px
        :width: 800px
        :align: center

    :param np.ndarray vertices: homogeneous vertex positions (vtx_num, 4)
    :param np.ndarray rest_pose: translation matices at rest pose (joint_num, 4, 4)
    :param np.ndarray dynamic_pose: translation matrices at a specified frame (joint_num, 4, 4)
    :param np.ndarray skinning_weights: skinning weights (equal to vertex weights) (vtx_num, joint_num)
    :return: `np.ndarray` new vertex positions at homogeneous coordinates (vtx_num, 4)
