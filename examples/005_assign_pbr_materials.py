import bpy
import sys
from pathlib import Path
import importlib

# Please change LIBRARY_ROOT_PATH according to your environment
LIBRARY_ROOT_PATH = Path(".").resolve().parent
sys.path.append(str(LIBRARY_ROOT_PATH))


if __name__ == '__main__':
    import bnp
    importlib.reload(bnp)

    bnp.scene.remove_objects("debug")
    helmet = bpy.context.scene.objects["auto_shader"]

    # Create a material and assign it to the scene object
    material = bnp.create_material()
    bnp.assign_material(helmet, material)
    bnp.create_shader(material)

    # Define texture paths
    texture_dir = LIBRARY_ROOT_PATH / "assets" / "DamagedHelmet"
    albedo_path = str(texture_dir / "Default_albedo.jpg")
    normal_path = str(texture_dir / "Default_normal.jpg")
    metalRoughness_path = str(texture_dir / "Default_metalRoughness.jpg")
    emissive_path = str(texture_dir / "Default_emissive.jpg")
    ao_path = str(texture_dir / "Default_ao.jpg")

    # Add each texture
    """
    bnp.add_albedo(material, albedo_path)
    bnp.add_normal(material, normal_path)

    # metallic: blue channel, roughness: green channel
    bnp.add_metallic_roughness(material, metalRoughness_path)

    # You can set metallic and roughness separately
    # bnp.add_metallic(material, metal_path)
    # bnp.add_roughness(material, roughness_path)

    bnp.add_emissive(material, emissive_path)
    bnp.add_ao(material, ao_path)
    """

    # Add PBR textures
    texture_paths = {
        "albedo": albedo_path,
        "normal": normal_path,
        "metallic_roughness": metalRoughness_path,
        "emissive": emissive_path,
        "ao": ao_path
    }
    bnp.add_pbr_textures(material, texture_paths)
