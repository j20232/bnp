bnp.scene.io
=====================


.. py:function:: import_geom(filepath, obj, keep_vertex_order=True, **kwargs)

    Import obj from filepath
    
    :param str filepath: absolute filepath (extension should be `.obj`, `.fbx`, `.glb`, `x3d`, `ply` or `stl`)
    :param bool keep_vertex_order: whether to keep topology
    :param kwargs: read https://docs.blender.org/api/current/bpy.ops.import_scene.html and https://docs.blender.org/api/current/bpy.ops.import_mesh.html


.. py:function:: export_geom(filepath, obj, keep_vertex_order=True, use_selection=True, **kwargs)

    Export obj to filepath (Note: this function exports all objects in `glb` mode)
    
    :param str filepath: absolute filepath (extension should be `.obj`, `.fbx`, `.glb`, `x3d`, `ply` or `stl`)
    :param bpy.types.Object obj: obj to export
    :param bool keep_vertex_order: whether to keep topology
    :param bool use_selection: whether to output only the selected object
    :param kwargs: read https://docs.blender.org/api/current/bpy.ops.export_scene.html and https://docs.blender.org/api/current/bpy.ops.export_mesh.html


.. py:function:: render(dirpath, ext="exr", camera=bpy.context.scene.camera, animation=False, frame_start=bpy.context.scene.frame_current, frame_end=bpy.context.scene.frame_current + 1, fps=30.0, render=bpy.context.scene.render,  render_mode="all", engine="BLENDER_EEVEE", device="GPU")

    Render an image or movie from camera

    :param str dirpath: absolute dirpath to save the image or movie
    :param str ext: file's extension. "png", "bmp", "jpg", "jpeg", "exr", "hdr" or "mp4".
    :param bpy.types.Object camera: camera which has `bpy.types.Camera` at `camera.data`
    :param bool animation: image (False) or movie (True)
    :param int frame_start: initial frame. this parameter is only used when `animation==True`
    :param int frame_end: final frame. this parameter is only used when `animation==True`
    :param float fps: frame rate. this parameter is only used when `animation==True`
    :param bpy.types.RenderSettings render: render setting in the scene
    :param str render_mode: type of gbuffers. "all": output all gbuffers. "Image" (rendered image), "Depth", "Mist" (Stencil), "Normal", "Shadow" (Roughness), "AO" (Ambient Occlusion), "DiffCol" (Albedo), "GlossCol" (Metalic) or "Emit" (Emission).
    :param str engine: "BLENDER_EEVEE" (GL-based) or "CYCLES" (Path Tracing)
    :param str device: "CPU" or "GPU"

