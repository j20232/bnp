import bpy
import numpy as np

def import_geom():
    pass

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
    else:
        raise Exception("Illegal extension")
    print(f"Exported {obj.name} to {filepath}")



