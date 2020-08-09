import bpy
import bmesh
import numpy as np
from bnp.objects.base import vec2np


# ----------------------------------- Conversion -----------------------------------------

def mesh2np(mesh: bpy.types.Mesh, world_matrix: np.ndarray = None,
            geo_type: str = "position", dtype: type = np.float32, is_local: bool = False,
            frame: int = bpy.context.scene.frame_current, as_homogeneous: bool = False) -> np.ndarray:
    # Input: mesh(bpy.types.Mesh), Output: positions or normals
    bpy.context.scene.frame_set(frame)
    if geo_type not in ["position", "normal"]:
        raise Exception("The type should  be position or normal.")

    # select position or normal
    local_verts = np.array([
        vec2np(v.co if geo_type == "position" else v.normal)
        for v in mesh.vertices], dtype=dtype)

    # whether convert to homogeneous coordinates or not
    local_verts = np.hstack((local_verts, np.ones(
        (len(local_verts), 1)))) if as_homogeneous or world_matrix is not None else local_verts
    if is_local or geo_type == "normal" or world_matrix is None:
        return local_verts if as_homogeneous else local_verts[:, 0:3]

    # Calculate global positions
    global_verts = np.array(
        [world_matrix @ v for v in local_verts], dtype=dtype)
    return global_verts if as_homogeneous else global_verts[:, 0:3]


def skinning_weights2np(obj: bpy.types.Object, dtype: type = np.float32) -> np.ndarray:
    # skining weights are equal to vertex weights in Blender
    mesh = obj.data
    vertices = mesh.vertices
    skinning_weights = np.zeros((len(vertices), len(obj.vertex_groups)), dtype=dtype)
    for vid, v in enumerate(mesh.vertices):
        for vg in v.groups:
            skinning_weights[vid, vg.group] = vg.weight
        skinning_weights[vid] /= sum(skinning_weights[vid])
    return skinning_weights  # (vtx_num, joint_num)

# -------------------------------- Normalization ----------------------------------------


def normalize_skinning_weights(obj: bpy.types.Object) -> bpy.types.Mesh:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action="DESELECT")

    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    for idx in range(len(bm.verts)):
        bm.select_history.add(bm.verts[idx])
        bpy.ops.object.vertex_weight_normalize_active_vertex()
        bpy.ops.mesh.select_all(action="DESELECT")

    mesh = obj.to_mesh()
    bm.to_mesh(mesh)
    bm.free()
    bpy.ops.object.mode_set(mode="OBJECT")
    return mesh

# ----------------------------------- Selection -----------------------------------------


def get_active_vertex_indices(obj: bpy.types.Object) -> list:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    indices = [v.index for v in reversed(bm.verts) if v.select]
    bm.free()
    bpy.ops.object.mode_set(mode="OBJECT")
    return indices  # vertex indices


# ----------------------------------- Shape keys ----------------------------------------


def remove_shape_keys(obj: bpy.types.Object, all: bool = True):
    # Shape key is equal to blend shape
    bpy.context.view_layer.objects.active = obj
    if bpy.context.object.data.shape_keys is not None:
        bpy.ops.object.shape_key_remove(all=all)


def add_shape_key(obj: bpy.types.Object, name: str, blend_weight: float = 1.0, vertices: np.ndarray = None,
                  slider_min: float = 0.0, slider_max: float = 1.0, from_mix: bool = False):
    # Shape key is equal to blend shape
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shape_key_add(from_mix=from_mix)
    key_block = bpy.data.shape_keys["Key"].key_blocks[bpy.context.object.active_shape_key_index]
    key_block.name = name
    key_block.slider_min = slider_min
    key_block.slider_max = slider_max
    adjust_shape_key(obj, name, blend_weight, vertices)


def adjust_shape_key(obj: bpy.types.Object, name: str, blend_weight: float, vertices: np.ndarray = None):
    bpy.context.view_layer.objects.active = obj
    key_block = bpy.data.shape_keys["Key"].key_blocks[name]
    key_block.value = blend_weight
    if vertices is not None:
        bpy.ops.object.mode_set(mode="EDIT")
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        for idx in range(len(bm.verts)):
            bm.verts[idx].co = (vertices[idx][0], vertices[idx][1], vertices[idx][2])
        mesh = obj.to_mesh()
        bm.to_mesh(mesh)
        bm.free()
        bpy.ops.object.mode_set(mode="OBJECT")


def insert_keyframes_to_shape_keys(obj: bpy.types.Object, blend_weights: dict):
    bpy.context.view_layer.objects.active = obj
    for str_frame in blend_weights.keys():
        frame = int(str_frame)
        for block_name in blend_weights[str_frame]:
            key_block = bpy.data.shape_keys["Key"].key_blocks[block_name]
            key_block.value = blend_weights[str_frame][block_name]
            key_block.keyframe_insert("value", frame=frame)


def get_keyframe_of_shapekeys(obj: bpy.types.Object) -> list:
    bpy.context.view_layer.objects.active = obj
    if obj.data.shape_keys is None or obj.data.shape_keys.animation_data.action is None:
        return []
    keyframes = []
    for fcurve in obj.data.shape_keys.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            # keyframe: Vector(keyframe, value)
            keyframes.append(int(keyframe.co[0]))
    return list(sorted(set(keyframes))) # list of keyframes (int)
