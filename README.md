# 🐣 bnp: Blender numpy utilities

![](https://github.com/j20232/bnp/blob/master/assets/logo.png)

## ✌ About

bnp contains simple numpy utilities for Blender.

Latest version: 0.2.0

You can easily read Blender's objects with numpy!

## 🚶　Installation

### bnp installation

1. Copy `bnp/bnp` to `$YOUR_BLENDER_PATH/scripts/addons_contrib` manually

e.g. `$YOUR_BLENDER_PATH`: `C:/Program Files/Blender Foundation/Blender 2.83/2.83`

- OK: C:/Program Files/Blender Foundation/Blender 2.83/2.83/scripts/addons_contrib/bnp/__init__.py
- NG: C:/Program Files/Blender Foundation/Blender 2.83/2.83/scripts/addons_contrib/bnp/bnp/__init__.py

### (Appendix) how to install numpy

If you have some errors when you import numpy, please run following commands.

1. Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) in `$YOUR_FAVORITE_DIRECTORY`
2. `% cd $YOUR_FAVORITE_DIRECTORY`
3. `% $BLENDER_PYTHON_PATH/python get-pip.py` with administrator mode or `sudo`
4. `% $BLENDER_PIP_PATH/pip install numpy` with administrator mode or `sudo`

e.g.

- `$YOUR_FAVORITE_DIRECTORY`: `C:/Users/YOUR_ACCOUNT/Downloads`
- `$BLENDER_PYTHON_PATH`: `C:/Program Files/Blender Foundation/Blender 2.83/2.83/python/bin`

## 🎲 Tiny example

```py
import bnp
vertices = bnp.objname2np("Cube")
print(vertices)  # (vtx_num, 3)
bnp.scene.put_cubes(vertices)
```

You can find more examples at https://github.com/j20232/bnp/tree/master/examples

To check examples, please open `*.blend`([sample scenes](https://github.com/j20232/bnp/tree/master/samples)) files in **your file browser**.

Don't open `*.blend` files from `Blender.exe` because this library doesn't work due to the permission.

## 🗄 Features

- [x] Numpy converter
  - Translation matrices of `bpy.types.Object` and `bpy.types.Armature`
  - Vertex positions of `bpy.types.Mesh`
  - Skinning weights (vertex weights) of `bpy.types.Object`
  - Blend shapes (shape keys) of `bpy.types.Object`
- [x] Simple geometry importer/exporter
- [x] Clear unused objects in your Scene
- [x] [Linear Blend Skinning](https://github.com/j20232/bnp/blob/master/assets/screenshots/lbs.png)

## 📄 Documentation

https://bnp.readthedocs.io/en/latest/

## 👁 Versions

- Blender 2.83.0 (or later)
- numpy: 1.17.0 (or later)

## ⚠️ LICENSE

GPL-3.0 (based on Blender)

If bnp violates any licenses, I'll delete this repository immediately.  
Please let me know if there're problems.

## 🐈 Author

mocobt

mocobt@gmail.com
