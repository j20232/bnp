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
    head_positions = bnp.conversion.armature2np(amt, mode="head")
    print("Head positions: ", head_positions)  # (joint_num, 3) at rest pose

    tail_positions = bnp.conversion.armature2np(amt, mode="tail")
    print("Tail positions: ", tail_positions)  # (joint_num, 3) at rest pose

    bone_lengths = bnp.conversion.armature2np(amt, mode="length")
    print("Bone lengths: ", bone_lengths)  # (joint_num,) at rest pose

    rest_pose_from_origin = bnp.conversion.armature2np(amt, mode="rest_from_origin")
    print("Rest pose from origin: ", rest_pose_from_origin)  # (joint_num, 4, 4) considering bones' rotation at rest pose

    dynamic_pose_from_origin = bnp.conversion.armature2np(amt, mode="dynamic_from_origin", frame=frame)
    print("Dynamic pose from origin: ", dynamic_pose_from_origin)  # (joint_num, 4, 4) considering bones' rotation at the pose

    obj = amt.children[0]
    rest_pose_vertices = bnp.conversion.any2np(obj, as_homogeneous=True)
    skinning_weights = bnp.conversion.get_skinning_weights_as_np(obj)
    print("Skinning weights: ", skinning_weights.shape)  # (vtx_num, joint_num)

    # Linear Blend Skinning from skinning weights and poses
    vertices = bnp.mathfunc.linear_blend_skinning(rest_pose_vertices, rest_pose_from_origin,
                                                  dynamic_pose_from_origin, skinning_weights)
    # bnp.scene.put_cubes(vertices[:, 0:3], size=0.15)

    armature = bnp.conversion.normalize_armature(amt)
    kinematic_tree = bnp.conversion.get_kinematic_tree(amt)
    print("kinematic_tree: ", kinematic_tree)

    rest_pose_relative = bnp.conversion.armature2np(amt, mode="rest_relative")
    print("Rest pose relative to parent: ", rest_pose_relative)  # (joint_num, 4, 4) not considering bones' rotation at rest pose
    rest_pose = bnp.conversion.armature2np(amt, mode="rest")
    print("Rest pose: ", rest_pose)  # (joint_num, 4, 4) not considering bones' rotation at rest pose

    dynamic_pose_relative = bnp.conversion.armature2np(amt, mode="dynamic_relative", frame=frame)
    print("Dynamic pose relative to parent: ", dynamic_pose_relative)  # (joint_num, 4, 4) not considering bones' rotation at the pose
    dynamic_pose = bnp.conversion.armature2np(amt, mode="dynamic", frame=frame)
    print("Dynamic pose: ", dynamic_pose)  # (joint_num, 4, 4) not considering bones' rotation at the pose

    vertices = bnp.mathfunc.linear_blend_skinning(rest_pose_vertices, rest_pose,
                                                  dynamic_pose, skinning_weights)
    # bnp.scene.put_cubes(vertices[:, 0:3], size=0.15)

    # Deformation with depsgraph
    deformed_vertices = bnp.conversion.obj2np(obj, frame=50, apply_modifier=True)
    bnp.scene.put_cubes(deformed_vertices, size=0.15)
