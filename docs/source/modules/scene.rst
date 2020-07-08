bnp.scene
=====================

.. py:function:: remove_objects(prefix="debug")

    Remove objects whose name starts with `prefix` from Blender

    :param str prefix: prefix


.. py:function:: clear_garbages()

    Remove objects which are not referenced from any data


.. py:function:: put_cubes(positions, prefix="debug", size=0.015, sampling_rate=1)

    Put cubes from np.ndarray whose shape should be (vtx_num, 3)

    :param np.ndarray positions: vertices (vtx_num, 3)
    :param str prefix: prefix of cube names
    :param float size: global scales of cubes
    :param int sampling_rate: the number which determines the ratio of vertices for visualization

