import bpy
import sys
from pathlib import Path
import importlib

# Please change LIBRARY_ROOT_PATH according to your environment
LIBRARY_ROOT_PATH = Path(".").resolve().parent
sys.path.append(str(LIBRARY_ROOT_PATH))


if __name__ == '__main__':
    import bnp
    importlib.reload(bnp)
    bnp.scene.remove_objects("debug")
    frame = 50

    amt = bpy.context.scene.objects["Armature"]
    head_positions = bnp.armature2np(amt, mode="head")
    print("Head positions: ", head_positions)  # (joint_num, 3) at rest pose

    tail_positions = bnp.armature2np(amt, mode="tail")
    print("Tail positions: ", tail_positions)  # (joint_num, 3) at rest pose

    bone_lengths = bnp.armature2np(amt, mode="length")
    print("Bone lengths: ", bone_lengths)  # (joint_num,) at rest pose

    obj = amt.children[0]
    rest_pose_vertices = bnp.any2np(obj, as_homogeneous=True)
    skinning_weights = bnp.skinning_weights2np(obj)
    print("Skinning weights: ", skinning_weights.shape)  # (vtx_num, joint_num)

    armature = bnp.normalize_roll(amt)
    # bnp.scene.remove_keyframe_from_armature(armature, frame)

    kinematic_tree = bnp.get_kinematic_tree(amt)
    print("kinematic_tree: ", kinematic_tree)

    rest_pose = bnp.armature2np(amt, mode="rest")
    print("Rest pose: ", rest_pose)  # (joint_num, 4, 4) not considering bones' rotation at rest pose

    dynamic_pose = bnp.armature2np(amt, mode="dynamic", frame=frame)
    print("Dynamic pose: ", dynamic_pose)  # (joint_num, 4, 4) not considering bones' rotation at the pose

    # Linear Blend Skinning from skinning weights and poses
    vertices = bnp.math.linear_blend_skinning(rest_pose_vertices, rest_pose,
                                              dynamic_pose, skinning_weights)
    # bnp.scene.put_cubes(vertices[:, 0:3], size=0.15)

    vertices = bnp.math.linear_blend_skinning(rest_pose_vertices, rest_pose,
                                              dynamic_pose, skinning_weights)
    bnp.scene.put_cubes(vertices[:, 0:3], size=0.15)

    # Deformation with depsgraph
    deformed_vertices = bnp.obj2np(obj, frame=50, apply_modifier=True)
    # bnp.scene.put_cubes(deformed_vertices, size=0.15)
