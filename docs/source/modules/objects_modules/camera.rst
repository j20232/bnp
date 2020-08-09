bnp.objects.camera
=====================


.. py:function:: camera2np(camera, render=bpy.context.scene.render, dtype=np.float32, frame=bpy.context.scene.frame_current, use_cv_coord=False) -> Tuple[np.ndarray]

    Return a tuple of intrinsic parameters and extrinsic parameters
    Ref: https://blender.stackexchange.com/questions/38009/3x4-camera-matrix-from-blender-camera

    :param bpy.types.Object camera: camera which has `bpy.types.Camera` at `camera.data`
    :param bpy.types.RenderSettings render: render setting in the scene
    :param dtype: dtype
    :param int frame: frame
    :param bool use_cv_coord: whether to convert the camera pose to opencv's coordinate
    :return: `Tuple[np.ndarray]` (K, Rt) where K: [3, 3], Rt: [3, 4]


.. py:function:: get_intrinsic_parameters(camera, render=bpy.context.scene.render, dtype=np.float32) -> np.ndarray

    Return intrinsic parameters

    :param bpy.types.Object camera: camera which has `bpy.types.Camera` at `camera.data`
    :param bpy.types.RenderSettings render: render setting in the scene
    :param dtype: dtype
    :return: `np.ndarray` K: [3, 3]


.. py:function:: get_extrinsic_parameters(camera, dtype=np.float32, frame=bpy.context.scene.frame_current, use_cv_coord=False) -> np.ndarray

    Return extrinsic parameters

    :param bpy.types.Object camera: camera which has `bpy.types.Camera` at `camera.data`
    :param dtype: dtype
    :param int frame: frame
    :param bool use_cv_coord: whether to convert the camera pose to opencv's coordinate
    :return: `np.ndarray` Rt: [3, 4]
                   

.. py:function:: KRt_from_P(P) -> Tuple[np.ndarray]

    Decompose camera matrix to intrinsic parameters and extrinsic parameters

    :param np.ndarray P: camera matrix
    :return: `Tuple[np.ndarray]` K, R, T


.. py:function:: create_camera(name="debug_camera", position=[0.0, 0.0, 3.0], rotation=[0.0, 0.0, 0.0], align="WORLD", enter_editmode=False, render=bpy.context.scene.render, P=None, K=None, Rt=None, scale=1.0, use_cv_coord=False) -> bpy.types.Object

    Create a camera from camera parameters. You can get the camera by setting either P or (K and Rt).
    Referenece: https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.camera_add

    :param str name: camera name
    :param list position: camera position
    :param list rotation: camera rotation
    :param str align: The alignment of the new object. See Blender's API
    :param bool enter_editmode: Enter Editmode, Enter editmode when adding this object
    :param bpy.types.RenderSettings render: render setting in the scene
    :param np.ndarray P: camera matrix. [3, 4]
    :param np.ndarray K: intrinsic parameters. [3, 3]
    :param np.ndarray Rt: extrinsic parameters. [3, 4]
    :param float scale: scale
    :param bool use_cv_coord: whether to convert the camera pose to opencv's coordinate
    :return: `bpy.types.Object` camera which has `bpy.types.Camera` at `camera.data`
