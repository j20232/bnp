from bnp.scene import cleaner
from bnp.scene import io
from bnp.scene import visualize


if True:
    import importlib
    importlib.reload(cleaner)
    importlib.reload(io)
    importlib.reload(visualize)
    from bnp.scene.cleaner import remove_objects, clear_garbages
    from bnp.scene.io import import_geom, export_geom
    from bnp.scene.visualize import put_cubes
