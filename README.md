# 🐣 bnp: Blender numpy utilities

## ✌ About

bnp contains simple numpy utilities for Blender.

You can easily read Blender's objects with numpy!

Currently, work in progress. 🥺

## 🚶　Installation

(work in the progress)

1. Add pip to your Bender
2. Install `numpy` with the Blender's pip
3. Copy `bnp/bnp` to `$YOUR_BLENDER_PATH/scripts/addons_contrib` manually

e.g. `$YOUR_BLENDER_PATH`: `C:/Program Files/Blender Foundation/Blender 2.83/2.83/scripts/addons_contrib`

- OK: C:/Program Files/Blender Foundation/Blender 2.83/2.83/scripts/addons_contrib/bnp/__init__.py
- NG: C:/Program Files/Blender Foundation/Blender 2.83/2.83/scripts/addons_contrib/bnp/bnp/__init__.py

## 🎲 Tiny example

```py
import bnp
vertices = bnp.conversion.objname2np("Cube")
print(vertices)  # (vtx_num, 3)
bnp.scene.put_cubes(vertices)
```

You can find more examples at https://github.com/j20232/bnp/tree/master/examples

To check examples, please open `*.blend`([sample scenes](https://github.com/j20232/bnp/tree/master/samples)) files in **your file browser**.  
Don't open `*.blend` files from `Blender.exe` because this library doesn't work due to the permission.

## 📄 Documentation

https://bnp.readthedocs.io/en/latest/

## 👁 Blender version

Blender 2.83

## ⚠️ LICENSE

GPL-3.0 (based on Blender)

If bnp violates any licenses, I'll delete this repository immediately.  
Please let me know if there're problems.

## 🐈 Author

mocobt

mocobt@gmail.com
