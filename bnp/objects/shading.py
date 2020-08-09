import bpy
from pathlib import Path


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


def pickup_node(node_tree, node_type):
    for node in node_tree.nodes:
        if type(node) is node_type:
            return node
    return None
