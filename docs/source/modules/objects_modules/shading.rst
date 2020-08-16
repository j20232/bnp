bnp.objects.shading
=====================


.. py:function:: create_material(material_name="debug_material")

    Create material in `bpy.data.materials`

    :param str material_name: name of the material


.. py:function:: assign_material(obj, material)

    Assign the input material to the object

    :param bpy.types.Object obj: object in the scene
    :param bpy.types.Material material: material in `bpy.data.materials`


.. py:function:: create_shader(material)

    Add a BSDF shader to the material

    :param  bpy.types.Material material: material


.. py:function:: add_pbr_textures(material, texture_paths, use_combined_metallic_roughness=True, metallic_channel=2, roughness_channel=1)

    Add pbr textures to the material

    :param bpy.types.Material material: material
    :param dict texture_paths: absolute paths of textures. key: "albedo", "normal", "metallic", "roughness", "metallic_roughness", "emissive" or "ao".
    :param bool use_combined_metallic_roughness: whether to use a texture combined with metallic and roughness
    :param int metallic_channel: metallic channel of the combined texture only used when use_combined_metallic_roughness == True
    :param int roughness_channel: roughness channel of the combined texture only used when use_combined_metallic_roughness == True


.. py:function:: add_albedo(material, albedo_path)

    Add albedo texture to the material

    :param bpy.types.Material material: material
    :param str albedo_path: abosolute albedo texture path


.. py:function:: add_normal(material, normal_path)

    Add normal texture to the material

    :param bpy.types.Material material: material
    :param str normal_path: abosolute normal texture path


.. py:function:: add_metallic(material, metallic_path)

    Add metallic texture to the material

    :param bpy.types.Material material: material
    :param str metallic_path: abosolute metallic texture path


.. py:function:: add_roughness(material, roughness_path)

    Add roughness texture to the material

    :param bpy.types.Material material: material
    :param str roughness_path: absolute roughness texture path


.. py:function:: add_metallic_roughness(material, metallic_roughness_path, metallic_channel=2, roughness_channel=1)

    Add metalic and roughness textures to the material

    :param bpy.types.Material material: material
    :param str metallic_roughness_path: abosolute metalic and roughness texture path
    :param int metallic_channel: metallic channel of the combined texture
    :param int roughness_channel: roughness channel of the combined texture

.. py:function:: add_emissive(material, emissive_path)

    Add emissive texture to the material

    :param bpy.types.Material material: material
    :param str emissive_path: abosolute emissive texture path


.. py:function:: add_ao(material, ao_path, fac=0.25)

    Add AO (Ambient Occlusion) texture to the material

    :param bpy.types.Material material: material
    :param str ao_path: abosolute AO texture path
    :param float fac:  mixing ratio of ao (ambient occlusion) to albedo

.. py:function:: set_envmap(filepath)

    Set an environment map to the current world

    :param str filepath: environment map filepath
