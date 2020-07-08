bnp.io
=====================

.. py:function:: load_geom(obj_name, geo_type="position", dtype=np.float32, is_local=False)

    Load a geometry from object name as `np.ndarray`

    :param str obj_name: object name
    :param str geo_type: "position" or "normal"
    :param dtype: dtype
    :param bool is_local: return local positions if is_local else global positions
    :return: np.ndarray (vertex_number, 3)
