import bpy
from pathlib import Path

# ----------------------------------- Object --------------------------------------------


def create_material(material_name: str = "debug_material"):
    scene_material_names = [material.name for material in bpy.data.materials]
    if material_name not in scene_material_names:
        return bpy.data.materials.new(material_name)
    else:
        print(f"Material '{material_name}' already exists.")
        return bpy.data.materials[material_name]


def assign_material(obj: bpy.types.Object, material: bpy.types.Material):
    bpy.context.view_layer.objects.active = obj
    object_slot_names = [slot.name for slot in obj.material_slots]
    if material.name not in object_slot_names:
        bpy.ops.object.material_slot_add()
        bpy.context.object.active_material = material


def create_shader(material: bpy.types.Material):
    bpy.context.object.active_material = material
    material.use_nodes = True
    node_tree = material.node_tree

    # bsdf
    bsdf_node = pickup_node(node_tree, bpy.types.ShaderNodeBsdfPrincipled)
    if bsdf_node is None or bsdf_node.name != "bsdf":
        bsdf_node = node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        bsdf_node.name = "bsdf"
    bsdf_node.location = (0.0, 0.0)

    # output
    output_node = pickup_node(node_tree, bpy.types.ShaderNodeOutputMaterial)
    if output_node is None or output_node.name != "output":
        output_node = node_tree.nodes.new("ShaderNodeOutputMaterial")
        output_node.name = "output"

    node_tree.links.new(bsdf_node.outputs[0], output_node.inputs[0])
    output_node.location = (300.0, 0.0)


def add_pbr_textures(material: bpy.types.Material, texture_paths: dict,
                     use_combined_metallic_roughness: bool = True,
                     metallic_channel: int = 2, roughness_channel: int = 1):
    add_albedo(material, texture_paths["albedo"])
    add_normal(material, texture_paths["normal"])
    if use_combined_metallic_roughness:
        add_metallic_roughness(material, texture_paths["metallic_roughness"],
                               metallic_channel=metallic_channel,
                               roughness_channel=roughness_channel)
    else:
        add_metallic(material, texture_paths["metallic"])
        add_roughness(material, texture_paths["roughness"])
    add_emissive(material, texture_paths["emissive"])
    add_ao(material, texture_paths["ao"])


def add_albedo(material: bpy.types.Material, albedo_path: str):
    texture_node = create_image_texture(material, albedo_path, "albedo")
    connect_texture_to_bsdf(material, texture_node, "Base Color")
    texture_node.location = (-600.0, 300.0)


def add_normal(material: bpy.types.Material, normal_path: str):
    node_tree = material.node_tree
    texture_node = create_image_texture(material, normal_path, "normal", "Non-Color")
    texture_node.location = (-600.0, -900.0)
    normal_map_node = pickup_node(node_tree, bpy.types.ShaderNodeNormalMap, "normal_map")
    if normal_map_node is None or normal_map_node.name != "normal_map":
        normal_map_node = node_tree.nodes.new("ShaderNodeNormalMap")
        normal_map_node.name = "normal_map"
    normal_map_node.location = (-250.0, -600.0)
    node_tree.links.new(texture_node.outputs[0], normal_map_node.inputs[1])
    connect_texture_to_bsdf(material, normal_map_node, "Normal")


def add_metallic(material: bpy.types.Material, metallic_path: str):
    texture_node = create_image_texture(material, metallic_path, "metallic", "Non-Color")
    connect_texture_to_bsdf(material, texture_node, "Metallic")
    texture_node.location = (-600.0, -300.0)


def add_roughness(material: bpy.types.Material, roughness_path: str):
    texture_node = create_image_texture(material, roughness_path, "roughness", "Non-Color")
    connect_texture_to_bsdf(material, texture_node, "Roughness")
    texture_node.location = (-600.0, -300.0)


def add_metallic_roughness(material: bpy.types.Material, metallic_roughness_path: str,
                           metallic_channel: int = 2, roughness_channel: int = 1):
    node_tree = material.node_tree
    texture_node = create_image_texture(material, metallic_roughness_path, "metallic_roughness", "Non-Color")
    texture_node.location = (-600.0, -300.0)

    separate_node = pickup_node(node_tree, bpy.types.ShaderNodeSeparateRGB, "separate_roughness_metallic")
    if separate_node is None or separate_node.name != "separate_roughness_metallic":
        separate_node = node_tree.nodes.new("ShaderNodeSeparateRGB")
        separate_node.name = "separate_roughness_metallic"
    separate_node.location = (-250.0, -300.0)

    node_tree.links.new(texture_node.outputs[0], separate_node.inputs[0])
    bsdf_node = pickup_node(node_tree, bpy.types.ShaderNodeBsdfPrincipled)
    roughness_socket_idx = -1
    metallic_socket_idx = -1
    for idx, socket in enumerate(bsdf_node.inputs):
        if socket.name == "Roughness":
            roughness_socket_idx = idx
        if socket.name == "Metallic":
            metallic_socket_idx = idx
    node_tree.links.new(separate_node.outputs[roughness_channel], bsdf_node.inputs[roughness_socket_idx])
    node_tree.links.new(separate_node.outputs[metallic_channel], bsdf_node.inputs[metallic_socket_idx])


def add_emissive(material: bpy.types.Material, emissive_path: str):
    texture_node = create_image_texture(material, emissive_path, "emissive")
    connect_texture_to_bsdf(material, texture_node, "Emission")
    texture_node.location = (-600.0, -600.0)


def add_ao(material: bpy.types.Material, ao_path: str, fac: float = 0.25):
    node_tree = material.node_tree
    ao_node = create_image_texture(material, ao_path, "ao", "Non-Color")
    ao_node.location = (-600.0, 0.0)

    mix_rgb_node = pickup_node(node_tree, bpy.types.ShaderNodeMixRGB, "mix_albedo_and_ao")
    if mix_rgb_node is None or mix_rgb_node.name != "mix_albedo_and_ao":
        mix_rgb_node = node_tree.nodes.new("ShaderNodeMixRGB")
        mix_rgb_node.name = "mix_albedo_and_ao"
    albedo_node = pickup_node(node_tree, bpy.types.ShaderNodeTexImage, "albedo")

    # mix_rgb_node
    mix_rgb_node.inputs[0].default_value = fac
    mix_rgb_node.blend_type = "MULTIPLY"
    mix_rgb_node.location = (-250.0, 0.0)

    node_tree.links.new(albedo_node.outputs[0], mix_rgb_node.inputs[1])
    node_tree.links.new(ao_node.outputs[0], mix_rgb_node.inputs[2])
    connect_texture_to_bsdf(material, mix_rgb_node, "Base Color")


def create_image_texture(material: bpy.types.Material, texture_path: str, node_name, color_settings: str = "sRGB"):
    node_tree = material.node_tree
    texture_node = pickup_node(node_tree, bpy.types.ShaderNodeTexImage, node_name)
    if texture_node is None or texture_node.name != node_name:
        texture_node = node_tree.nodes.new("ShaderNodeTexImage")
        texture_node.name = node_name
    bpy.data.images.load(texture_path, check_existing=True)
    image = bpy.data.images[Path(texture_path).name]
    image.colorspace_settings.name = color_settings
    texture_node.image = image
    return texture_node


def connect_texture_to_bsdf(material: bpy.types.Material, texture_node: bpy.types.TextureNode, socket_name: str):
    node_tree = material.node_tree
    bsdf_node = pickup_node(node_tree, bpy.types.ShaderNodeBsdfPrincipled)
    socket_idx = -1
    for idx, socket in enumerate(bsdf_node.inputs):
        if socket.name == socket_name:
            socket_idx = idx
    node_tree.links.new(texture_node.outputs[0], bsdf_node.inputs[socket_idx])

# ----------------------------------- Env map -------------------------------------------


def set_envmap(filepath: str):
    if bpy.context.scene.world is None:
        new_world = bpy.data.worlds.new("World")
        bpy.context.scene.world = new_world
        bpy.context.scene.world.use_nodes = True
    node_tree = bpy.context.scene.world.node_tree
    env_node = pickup_node(node_tree, bpy.types.ShaderNodeTexEnvironment)
    if env_node is None:
        env_node = node_tree.nodes.new("ShaderNodeTexEnvironment")
    bpy.data.images.load(filepath, check_existing=True)
    image = bpy.data.images[Path(filepath).name]
    env_node.image = image
    background_node = node_tree.nodes["Background"]
    node_tree.links.new(env_node.outputs[0], background_node.inputs[0])


# ----------------------------------- Util ----------------------------------------------

def pickup_node(node_tree, node_type, node_name: str = None):
    for node in node_tree.nodes:
        if type(node) is node_type:
            if node_name is None or node.name == node_name:
                return node
    return None
