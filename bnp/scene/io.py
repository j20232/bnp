import bpy
import os


def import_geom(filepath: str, keep_vertex_order=True, **kwargs):
    ext = filepath.split(".")[-1]
    if not os.path.exists(filepath):
        print(f"WARNING: {filepath} doesn't exist!")
        return
    if ext == "obj":
        split_mode = "OFF" if keep_vertex_order else "ON"
        bpy.ops.import_scene.obj(
            filepath=filepath, split_mode=split_mode, **kwargs)
    elif ext == "fbx":
        bpy.ops.import_scene.fbx(filepath=filepath, **kwargs)
    elif ext == "glb":
        bpy.ops.import_scene.gltf(filepath=filepath, **kwargs)
    elif ext == "x3d":
        bpy.ops.import_scene.x3d(filepath=filepath, **kwargs)
    elif ext == "ply":
        bpy.ops.import_mesh.ply(filepath=filepath, **kwargs)
    elif ext == "stl":
        bpy.ops.import_mesh.stl(filepath=filepath, **kwargs)
    else:
        raise Exception("Illegal extension")
    print(f"Imported {filepath}")


def export_geom(filepath: str, obj: bpy.types.Object,
                keep_vertex_order=True, use_selection=True, **kwargs):
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    ext = filepath.split('.')[-1]
    if ext == "obj":
        bpy.ops.export_scene.obj(filepath=filepath, keep_vertex_order=keep_vertex_order,
                                 use_selection=use_selection, **kwargs)
    elif ext == "fbx":
        bpy.ops.export_scene.fbx(
            filepath=filepath, use_selection=use_selection, **kwargs)
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


def render(filepath: str, camera: bpy.types.Object = bpy.context.scene.camera, animation: bool = False,
           frame_start: int = bpy.context.scene.frame_current, frame_end: int = bpy.context.scene.frame_current + 1,
           fps: float = 30.0, render: bpy.types.RenderSettings = bpy.context.scene.render, write_still: bool = True,
           engine: str = "BLENDER_EEVEE", device: str = "GPU"):
    bpy.context.scene.camera = camera
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end
    render.fps = fps

    ext = filepath.split(".")[-1].lower()
    if ext == "png":
        render.image_settings.file_format = "PNG"
    elif ext == "bmp":
        render.image_settings.file_format = "BMP"
    elif ext == "jpg" or ext == "jpeg":
        render.image_settings.file_format = "JPEG"
    elif ext == "exr":
        render.image_settings.file_format = "OPEN_EXR"
    elif ext == "hdr":
        render.image_settings.file_format = "HDR"
    elif ext == "mp4":
        render.image_settings.file_format = "FFMPEG"
        render.ffmpeg.format = "MPEG4"
        render.ffmpeg.codec = "H264"

    render.engine = engine
    if engine == "CYCLES":
        bpy.context.scene.cycles.device = device

    render.filepath = filepath
    bpy.ops.render.render(animation=animation, write_still=write_still)
