import bpy
import bnp.mathfunc
import re

# -------------------------- Remove from scene -----------------------------


def remove_objects(prefix="debug"):
    if bpy.context.view_layer.objects.active is None:
        return
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    bpy.ops.object.select_all(action="DESELECT")
    cnt = 0
    for obj in bpy.context.scene.objects:
        if re.match(prefix, obj.name) is not None:
            obj.select_set(True)
            cnt += 1
    if cnt != 0:
        bpy.ops.object.delete()
    clear_garbages()


def clear_garbages():
    for block in bpy.data.objects:
        if block.users == 0:
            bpy.data.objects.remove(block)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)
    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)
    for block in bpy.data.collections:
        if block.users == 0:
            bpy.data.collections.remove(block)

# -------------------------- Remove keyframes ------------------------------


def remove_keyframe_from_object(obj, frame):
    if obj.rotation_mode == "QUATERNION":
        obj.keyframe_insert(data_path="rotation_quaternion", frame=frame)
        obj.keyframe_delete(data_path="rotation_quaternion", frame=frame)
    elif obj.rotation_mode == "AXIS_ANGLE":
        obj.keyframe_insert(data_path="rotation_axis_angle", frame=frame)
        obj.keyframe_delete(data_path="rotation_axis_angle", frame=frame)
    else:
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)
        obj.keyframe_delete(data_path="rotation_euler", frame=frame)
    obj.keyframe_insert(data_path="location", frame=frame)
    obj.keyframe_delete(data_path="location", frame=frame)
    obj.keyframe_insert(data_path="scale", frame=frame)
    obj.keyframe_delete(data_path="scale", frame=frame)


def remove_keyframe_from_armature(armature, frame, exception_bone_indices=None):
    exception_bone_indices = [] if exception_bone_indices is None else exception_bone_indices
    for idx, bone in enumerate(armature.pose.bones):
        if idx in exception_bone_indices:
            continue
        remove_keyframe_from_object(bone, frame)


# --------------------------- Normalization ------------------------------

def change_bone_rotation_mode(armature, mode, normalized=True):
    armature.rotation_mode = mode
    for bone in armature.pose.bones:
        q = bnp.mathfunc.normalize_axis_angle(bone.rotation_axis_angle)
        print(q)
        assert False
        bone.rotation_mode = mode


def normalize_armature(armature: bpy.types.Object):
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    for bone in armature.data.edit_bones:
        bone.roll = 0.0
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

# -------------------------- Create objects ------------------------------


def put_cubes(positions, prefix="debug", size=0.015, sampling_rate=1):
    # positions: (vtx_num, 3)
    for block in bpy.data.collections:
        if block.name == prefix:
            bpy.data.collections.remove(block)
    debug_collection = bpy.data.collections.new(prefix)
    bpy.data.collections["Collection"].children.link(debug_collection)
    for idx, v in enumerate(positions):
        if idx % sampling_rate != 0:
            continue
        bpy.ops.mesh.primitive_cube_add(size=size, location=(v[0], v[1], v[2]))
        bpy.context.object.name = f"debug_{str(idx)}"
        debug_collection.objects.link(bpy.context.object)
        bpy.data.collections["Collection"].objects.unlink(bpy.context.object)
