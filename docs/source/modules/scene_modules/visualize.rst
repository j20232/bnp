bnp.scene.visualize
=====================


.. py:function:: put_cubes(positions, prefix="debug", size=0.015, sampling_rate=1)

    Put cubes from np.ndarray whose shape should be (vtx_num, 3)

    :param np.ndarray positions: vertices (vtx_num, 3)
    :param str prefix: prefix of cube names
    :param float size: global scales of cubes
    :param int sampling_rate: the number which determines the ratio of vertices for visualization
