# 🐣 bnp: Blender numpy utilities

![](https://github.com/j20232/bnp/blob/master/assets/logo.png)

## ✌ About

bnp contains simple numpy utilities for Blender.

Latest version: 0.4.1

You can easily read Blender's objects with numpy!

## 🚶 Installation

### bnp installation

1. Copy `bnp/bnp` to `$YOUR_BLENDER_PATH/scripts/addons_contrib` manually

e.g. `$YOUR_BLENDER_PATH`: `C:/Program Files/Blender Foundation/Blender 2.83/2.83`

- OK: C:/Program Files/Blender Foundation/Blender 2.83/2.83/scripts/addons_contrib/bnp/**init**.py
- NG: C:/Program Files/Blender Foundation/Blender 2.83/2.83/scripts/addons_contrib/bnp/bnp/**init**.py

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
  - Camera parameters from `bpy.types.Camera`
- [x] Clear unused objects in your Scene
- [x] [Simple geometry importer/exporter](https://github.com/j20232/bnp/blob/master/examples/001_load_mesh.py)
- [x] [Linear Blend Skinning](https://github.com/j20232/bnp/blob/master/examples/002_lbs.py)  
![](https://github.com/j20232/bnp/blob/master/assets/screenshots/lbs.png)
 - Green box: box deformed with Blender's LBS
 - White boxes: vertices calculated with bnp's LBS

- [x] [Blend shape setting API](https://github.com/j20232/bnp/blob/master/examples/003_blendshape.py)  
![](https://github.com/j20232/bnp/blob/master/assets/screenshots/blend_shapes.gif)
 - You can easily add blend shapes (shape keys) and insert the keyframes to the scene

- [x] [Simple rendering API](https://github.com/j20232/bnp/blob/master/examples/004_set_camera_and_render_image.py)  
![](https://github.com/j20232/bnp/blob/master/assets/screenshots/gbuffer.png)
 - You can easily write rendered images and gbuffers as `.png`, `.bmp`, `.jpg`, `.exr`, `.hdr` and `.mp4`

- [x] [PBR material setting API](https://github.com/j20232/bnp/blob/master/examples/005_assign_pbr_materials.py)  
![](https://github.com/j20232/bnp/blob/master/assets/screenshots/pbr_material.png)
 - Left: GLTF default shading
 - Right: PBR shading based on [cgbookcase.com](https://www.cgbookcase.com/textures/how-to-use-pbr-textures-in-blender)
 - You can easily load PBR textures!
    - Please get them from [FREE PBR](https://freepbr.com/), [textures.com](https://www.textures.com/) and so on

You can render images with offscreen mode as follows:

```sh
$ blender.exe -b .\004_set_camera_and_render_image.blend -P ..\examples\004_set_camera_and_render_image.py
```

## 📄 Documentation

https://bnp.readthedocs.io/en/latest/

## 👁 Versions

- Blender 2.83.0 (or later)
- numpy: 1.19.0 (or later)

## ⚠️ LICENSE

GPL-3.0 (based on Blender)

If bnp violates any licenses, I'll delete this repository immediately.  
Please let me know if there're problems.

## 🐈 Author

mocobt

mocobt@gmail.com
