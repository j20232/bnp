from bnp.objects import base
from bnp.objects import armature
from bnp.objects import camera
from bnp.objects import light
from bnp.objects import mesh
from bnp.objects import obj
from bnp.objects import shading


if True:
    import importlib
    importlib.reload(base)
    importlib.reload(armature)
    importlib.reload(camera)
    importlib.reload(light)
    importlib.reload(mesh)
    importlib.reload(obj)
    importlib.reload(shading)

    # base
    from bnp.objects.base import batch_identity, vec2np, mat2np, vertices2np, collection2np, world_matrix2np, location2np, rotation2np, scale2np
    from bnp.objects.base import normalize_quaternion, normalize_axis_angle, axis_angle_4to3, axis_angle_3to4, quaternion2R, axis_angle2R, euler2R, change_rotation_mode
    from bnp.objects.base import get_keyframe_list, insert_keyframe, remove_keyframe, remove_keyframes

    # armature
    from bnp.objects.armature import posebone_basis, armature2np, posebone2np, bone2np
    from bnp.objects.armature import get_kinematic_tree
    from bnp.objects.armature import insert_keyframe_to_posebone, insert_keyframe_to_armature
    from bnp.objects.armature import remove_keyframe_from_posebone, remove_keyframe_from_armature, remove_keyframes_from_armature
    from bnp.objects.armature import change_rotation_modes_of_armature, normalize_roll

    # camera
    from bnp.objects.camera import camera2np, create_camera, get_intrinsic_parameters, get_extrinsic_parameters, KRt_from_P

    # light
    from bnp.objects.light import create_light

    # mesh
    from bnp.objects.mesh import mesh2np, skinning_weights2np
    from bnp.objects.mesh import normalize_skinning_weights
    from bnp.objects.mesh import get_active_vertex_indices
    from bnp.objects.mesh import remove_shape_keys, add_shape_key, adjust_shape_key, insert_keyframes_to_shape_keys, get_keyframe_of_shapekeys

    # obj
    from bnp.objects.obj import any2np, obj2np, objname2np

    # shading
    from bnp.objects.shading import create_material, assign_material, create_shader
    from bnp.objects.shading import add_pbr_textures, add_albedo, add_normal, add_metallic, add_roughness, add_metallic_roughness, add_emissive, add_ao
    from bnp.objects.shading import set_envmap
