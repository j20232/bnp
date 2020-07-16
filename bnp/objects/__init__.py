from bnp.objects import base
from bnp.objects import armature
from bnp.objects import mesh
from bnp.objects import obj


if True:
    import importlib
    importlib.reload(base)
    importlib.reload(armature)
    importlib.reload(mesh)
    importlib.reload(obj)

    # base
    from bnp.objects.base import batch_identity, vec2np, mat2np, vertices2np, collection2np, world_matrix2np, location2np, rotation2np, scale2np
    from bnp.objects.base import normalize_quaternion, normalize_axis_angle, quaternion2R, axis_angle2R, euler2R
    from bnp.objects.base import remove_keyframe

    # armature
    from bnp.objects.armature import armature2np, posebone2np, bone2np
    from bnp.objects.armature import get_kinematic_tree
    from bnp.objects.armature import remove_keyframe_from_armature
    from bnp.objects.armature import change_bone_rotation_mode, normalize_roll

    # mesh
    from bnp.objects.mesh import mesh2np, skinning_weights2np, get_active_indices

    # obj
    from bnp.objects.obj import any2np, obj2np, objname2np
