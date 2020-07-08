# 🐣 bnp: Blender numpy utilities
## ✌ About

bnp contains simple numpy utilities for Blender.

You can easily read Blender's objects with numpy!

Currently, work in progress. 🥺

##  🎲 Tiny example

```py
import bnp
vertices = bnp.io.load_geom("Cube")
print(vertices)  # (vtx_num, 3)
bnp.scene.put_cubes(vertices)
```

## 📄 Documentation

https://bnp.readthedocs.io/en/latest/

## 👁 Blender version

Blender 2.83

## 🐈 Authoer

mocobt
