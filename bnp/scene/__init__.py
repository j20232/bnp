from bnp.scene import clean
from bnp.scene import io
from bnp.scene import visualize


if True:
    import importlib
    importlib.reload(clean)
    importlib.reload(io)
    importlib.reload(visualize)
    from bnp.scene.clean import remove_objects, clear_garbages
    from bnp.scene.io import import_geom, export_geom, render
    from bnp.scene.visualize import put_cubes
