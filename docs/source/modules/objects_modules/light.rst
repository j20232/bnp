bnp.objects.light
=====================


.. py:function:: create_light(name="debug_light", position=[0.0, 0.0, 3.0], rotation=[0.0, 0.0, 0.0], light_type="POINT", radius=1.0, align="WORLD") -> bpy.types.Object:

    Create a light in the current scene.
    Reference: https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.light_add

    :param name: The name of the light
    :param position: The position of the light
    :param rotation: The rotation of the light
    :param light_type: The type of the light
    :param radius: The radius of the light
    :param align: The align of the light
    :return: `light` which has `bpy.types.Light` at `light.data`
