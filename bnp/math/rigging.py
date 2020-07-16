import numpy as np


def linear_blend_skinning(vertices, rest_pose, dynamic_pose, skinning_weights):
    """Calculate new vertex positions

    Args:
        vertices (np.ndarray): homogeneous vertex positions (vtx_num, 4)
        rest_pose (np.ndarray): translation matices at rest pose (joint_num, 4, 4)
        dynamic_pose (np.ndarray): translation matrices at a specified frame (joint_num, 4, 4)
        skinning_weights (np.ndarray): skinning weights (equal to vertex weights) (vtx_num, joint_num)

    Returns:
        np.ndarray: new vertex positions at homogeneous coordinates (vtx_num, 4)
    """
    vertices = vertices.reshape(-1, 1, 4)
    inv_rest_pose = np.linalg.inv(rest_pose).transpose(0, 2, 1)
    dynamic_pose = dynamic_pose.transpose(0, 2, 1)
    skinning_weights = skinning_weights.reshape(len(vertices), -1, 1, 1)
    lbs_matrices = np.sum(skinning_weights * inv_rest_pose @ dynamic_pose, axis=1)
    return (vertices @ lbs_matrices)[:, 0]  # (vtx_num, 4)
