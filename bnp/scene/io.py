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


def render(filepath: str, ext: str = "exr", camera: bpy.types.Object = bpy.context.scene.camera, animation: bool = False,
           frame_start: int = bpy.context.scene.frame_current, frame_end: int = bpy.context.scene.frame_current + 1,
           fps: float = 30.0, render: bpy.types.RenderSettings = bpy.context.scene.render,
           render_mode="all", engine: str = "BLENDER_EEVEE", device: str = "GPU"):
    # Prepare the renderer
    render_layer, out_layer = _prepare_composit_node(filepath, camera, frame_start, frame_end, render_mode)
    _set_engine(filepath, ext, render, engine, device, fps)
    all_modes = ["Image", "Depth", "Mist", "Normal", "Shadow", "AO", "DiffCol", "GlossCol", "Emit"]
    if render_mode in all_modes:
        _render_single_buffer(render_layer, out_layer, render_mode, animation)
    elif render_mode == "all":
        _render_all_buffers(render_layer, out_layer, animation)
    else:
        raise NotImplementedError("Illegal render_mode.")


def _render_all_buffers(render_layer, out_layer, animation: bool):
    socket_idx = _get_socket_index_from_render_layer(render_layer, "Image")
    bpy.context.scene.node_tree.links.new(render_layer.outputs[socket_idx], out_layer.inputs[0])
    # Depth, Stencil, Normal, Roughness, Ambient Occlusion, Albedo, Metalic, Emission
    all_modes = ["Depth", "Mist", "Normal", "Shadow", "AO", "DiffCol", "GlossCol", "Emit"]
    current_slots = [slot.path for slot in out_layer.file_slots]
    for idx, mode in enumerate(all_modes):
        if mode not in current_slots:
            out_layer.file_slots.new(mode)
        socket_idx = _get_socket_index_from_render_layer(render_layer, mode)
        bpy.context.scene.node_tree.links.new(render_layer.outputs[socket_idx], out_layer.inputs[idx + 1])
    bpy.ops.render.render(animation=animation)


def _render_single_buffer(render_layer, out_layer, render_mode: str, animation: bool):
    slot = out_layer.file_slots["Image"]
    slot.path = render_mode
    socket_idx = _get_socket_index_from_render_layer(render_layer, render_mode)
    bpy.context.scene.node_tree.links.new(render_layer.outputs[socket_idx], out_layer.inputs[0])
    bpy.ops.render.render(animation=animation)


def _get_socket_index_from_render_layer(render_layer, socket_name: str = "Image"):
    for idx, socket in enumerate(render_layer.outputs):
        if socket.name == socket_name:
            return idx
    return -1


def _set_engine(filepath: str, ext: str = "exr", render: bpy.types.RenderSettings = bpy.context.scene.render,
                engine: str = "BLENDER_EEVEE", device: str = "GPU", fps: float = 30.0):
    render.fps = fps
    render.filepath = filepath  # directory name

    # Set file type
    render.image_settings.file_format = _get_format_from_ext(ext)
    if ext == "mp4":
        render.ffmpeg.format = "MPEG4"
        render.ffmpeg.codec = "H264"

    render.image_settings.use_zbuffer = True
    render.engine = engine
    if engine == "CYCLES":
        bpy.context.scene.cycles.device = device
    elif engine == "BLENDER_EEVEE":
        bpy.context.scene.eevee.use_gtao = True  # Ambient Occlusion
    else:
        raise NotImplementedError("Illegal engine name!")
    bpy.context.scene.view_layers["View Layer"].use_pass_combined = True  # Output
    bpy.context.scene.view_layers["View Layer"].use_pass_diffuse_color = True   # Albedo
    bpy.context.scene.view_layers["View Layer"].use_pass_normal = True  # Normal
    bpy.context.scene.view_layers["View Layer"].use_pass_z = True  # Depth
    bpy.context.scene.view_layers["View Layer"].use_pass_mist = True  # Stencil
    bpy.context.scene.view_layers["View Layer"].use_pass_emit = True  # Emission
    bpy.context.scene.view_layers["View Layer"].use_pass_shadow = True  # Roughness
    bpy.context.scene.view_layers["View Layer"].use_pass_glossy_color = True  # Metalic
    bpy.context.scene.view_layers["View Layer"].use_pass_ambient_occlusion = True  # Ambient Occlusion


def _prepare_composit_node(filepath: str, camera: bpy.types.Object = bpy.context.scene.camera,
                           frame_start: int = bpy.context.scene.frame_current, frame_end: int = bpy.context.scene.frame_current + 1,
                           render_mode="Image"):
    bpy.context.scene.camera = camera
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end
    bpy.context.scene.use_nodes = True
    render_layer = None
    for node in bpy.context.scene.node_tree.nodes:
        if type(node) == bpy.types.CompositorNodeRLayers:
            render_layer = node
    if render_layer is None:
        render_layer = bpy.context.scene.node_tree.nodes.new("CompositorNodeRLayers")
    out_layer = _generate_output_node(bpy.context.scene.node_tree, render_mode)
    out_layer.base_path = filepath + "/" + render_mode
    return render_layer, out_layer


def _generate_output_node(node_tree, node_name: str = "Image"):
    layer = None
    node_list = [node.name for node in node_tree.nodes]
    if node_name in node_list:
        layer = node_tree.nodes[node_name]
    else:
        layer = node_tree.nodes.new("CompositorNodeOutputFile")
        layer.name = node_name
    return layer


def _get_format_from_ext(ext: str):
    if ext == "png":
        return "PNG"
    elif ext == "bmp":
        return "BMP"
    elif ext == "jpg" or ext == "jpeg":
        return "JPEG"
    elif ext == "exr":
        return "OPEN_EXR"
    elif ext == "hdr":
        return "HDR"
    elif ext == "mp4":
        return "FFMPEG"
    else:
        raise NotImplementedError("Illegal extension!")
