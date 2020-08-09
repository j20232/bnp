import bpy
import re


def remove_objects(prefix: str = "debug"):
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
