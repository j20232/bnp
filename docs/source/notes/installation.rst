Installation
=====================

(work in the progress)

1. Copy `bnp/bnp` to `$YOUR_BLENDER_PATH/scripts/addons_contrib` manually

e.g. `$YOUR_BLENDER_PATH`: `C:/Program Files/Blender Foundation/Blender 2.83/2.83`

- OK: C:/Program Files/Blender Foundation/Blender 2.83/2.83/scripts/addons_contrib/bnp/__init__.py
- NG: C:/Program Files/Blender Foundation/Blender 2.83/2.83/scripts/addons_contrib/bnp/bnp/__init__.py

If you have some errors when you import numpy, please run following commands.

1. Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) in `$YOUR_FAVORITE_DIRECTORY`
2. `% cd $YOUR_FAVORITE_DIRECTORY`
3. `% $BLENDER_PYTHON_PATH/python get-pip.py` with administrator mode or `sudo`
4. `% $BLENDER_PIP_PATH/pip install numpy` with administrator mode or `sudo`

e.g.

- `$YOUR_FAVORITE_DIRECTORY`: `C:/Users/YOUR_ACCOUNT/Downloads`
- `$BLENDER_PYTHON_PATH`: `C:/Program Files/Blender Foundation/Blender 2.83/2.83/python/bin`
