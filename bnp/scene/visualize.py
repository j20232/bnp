import bpy

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
        if bpy.context.object in list(bpy.data.collections["Collection"].objects):
            bpy.data.collections["Collection"].objects.unlink(bpy.context.object)
        if bpy.context.object in list(bpy.context.scene.collection.objects):
            bpy.context.scene.collection.objects.unlink(bpy.context.object)
