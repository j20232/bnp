import bpy
import bmesh
import numpy as np
from bnp.objects.base import vec2np


# ----------------------------------- Conversion -----------------------------------------

def mesh2np(mesh: bpy.types.Mesh, world_matrix=None,
            geo_type="position", dtype=np.float32, is_local=False,
            frame=bpy.context.scene.frame_current, as_homogeneous=False) -> np.ndarray:
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


def skinning_weights2np(obj: bpy.types.Object, dtype=np.float32) -> np.ndarray:
    # skining weights are equal to vertex weights in Blender
    mesh = obj.data
    vertices = mesh.vertices
    skinning_weights = np.zeros((len(vertices), len(obj.vertex_groups)))
    for vid, v in enumerate(mesh.vertices):
        for vg in v.groups:
            skinning_weights[vid, vg.group] = vg.weight
        skinning_weights[vid] /= sum(skinning_weights[vid])
    return skinning_weights  # (vtx_num, joint_num)

# -------------------------------- Normalization ----------------------------------------


def normalize_skinning_weights(obj):
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


def get_active_indices(obj: bpy.types.Object):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    indices = [v.index for v in reversed(bm.verts) if v.select]
    bm.free()
    bpy.ops.object.mode_set(mode="OBJECT")
    return indices
