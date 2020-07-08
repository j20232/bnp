# 🐣 bnp: Blender numpy utilities
## ✌ About

bnp contains simple numpy utilities for Blender.

You can easily read Blender's objects with numpy!

Currently, work in progress. 🥺

##  🎲 Tiny example

```py
import bnp
vertices = bnp.conversion.objname2np("Cube")
print(vertices)  # (vtx_num, 3)
bnp.scene.put_cubes(vertices)
```

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
