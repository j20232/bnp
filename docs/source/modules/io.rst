bnp.io
=====================


.. py:function:: export_geom(filepath, obj, keep_vertex_order=True, use_selection=True, **kwargs)

    Export obj to filepath (Note: this function exports all objects in `glb` mode)
    
    :param str filepath: absolute filepath
    :param bpy.types.Object obj: obj to export
    :param bool keep_vertex_order: whether to keep topology
    :param bool use_selection: whether to output only the selected object
    :param kwargs: read https://docs.blender.org/api/current/bpy.ops.export_scene.html
