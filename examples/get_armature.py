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

    amt = bpy.context.scene.objects["Armature"]
    head_positions = bnp.conversion.armature2np(amt, mode="head")
    print("Head positions: ", head_positions)  # (joint_num, 3)

    tail_positions = bnp.conversion.armature2np(amt, mode="tail")
    print("Tail positions: ", tail_positions)  # (joint_num, 3)

    bone_lengths = bnp.conversion.armature2np(amt, mode="length")
    print("Bone lengths: ", bone_lengths)  # (joint_num,)

    rest_pose = bnp.conversion.armature2np(amt, mode="rest_from_origin")
    print("Rest pose: ", rest_pose)  # (joint_num, 4, 4) considering bones' rotation at rest pose

    dynamic_pose = bnp.conversion.armature2np(amt, mode="dynamic_from_origin")
    print("Dynamic pose: ", dynamic_pose)  # (joint_num, 4, 4) considering bones' rotation at rest pose
