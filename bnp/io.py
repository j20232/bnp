import bpy
import os
import numpy as np

def import_geom(filepath, keep_vertex_order=True, **kwargs):
    ext = filepath.split(".")[-1]
    if not os.path.exists(filepath):
        print(f"WARNING: {filepath} doesn't exist!")
        return
    if ext == "obj":
        split_mode = "OFF" if keep_vertex_order else "ON"
        bpy.ops.import_scene.obj(filepath=filepath, split_mode=split_mode, **kwargs)
    elif ext == "fbx":
        bpy.ops.import_scene.fbx(filepath=filepath, **kwargs)
    elif ext == "glb":
        bpy.ops.import_scene.glb(filepath=filepath, **kwargs)
    elif ext == "x3d":
        bpy.ops.import_scene.x3d(filepath=filepath, **kwargs)
    elif ext == "ply":
        bpy.ops.import_mesh.ply(filepath=filepath, **kwargs)
    elif ext == "stl":
        bpy.ops.import_mesh.stl(filepath=filepath, **kwargs)
    else:
        raise Exception("Illegal extension")


def export_geom(filepath, obj,
                keep_vertex_order=True, use_selection=True, **kwargs):
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    ext = filepath.split('.')[-1]
    if ext == "obj":
        bpy.ops.export_scene.obj(filepath=filepath, keep_vertex_order=keep_vertex_order,
                                 use_selection=use_selection, **kwargs)
    elif ext == "fbx":
        bpy.ops.export_scene.fbx(filepath=filepath, use_selection=use_selection, **kwargs)
    elif ext == "glb":
        bpy.ops.export_scene.gltf(filepath=filepath, **kwargs)
    elif ext == "x3d":
        bpy.ops.export_scene.x3d(filepath=filepath, **kwargs)
    elif ext == "ply":
        bpy.ops.export_mesh.ply(filepath=filepath, **kwargs)
    elif ext == "stl":
        bpy.ops.export_mesh.stl(filepath=filepath, **kwargs)
    else:
        raise Exception("Illegal extension")
    print(f"Exported {obj.name} to {filepath}")



