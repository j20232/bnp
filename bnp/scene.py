import bpy
import re


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
