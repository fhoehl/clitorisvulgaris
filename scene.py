import os
import sys
from collections import defaultdict
from random import choice, uniform
from math import radians
from tempfile import gettempdir
from operator import itemgetter
from datetime import datetime

import bpy
import mathutils

# Update Blender's Python import path
sys.path.append(os.path.dirname(__file__))
sys.path.append("/usr/lib/python3.5")
sys.path.append("/usr/local/lib/python3.5/dist-packages")

import palette


TEXTURE_DIRECTORY_PATH = "./textures"

TRACKBALL_OBJ = bpy.data.objects["Trackball"]

CLIT_OBJ = bpy.data.objects["Clitoris"]

CLIT_MATERIAL = bpy.data.materials["ClitorisMaterial"]

TEXTURE_NODE_NAME = "Wallpaper"

ACTIVITY_SHAPE_KEY = CLIT_OBJ.data.shape_keys.key_blocks["Activity"]
ACTIVITY_SHAPE_KEY_RANGE = (0, 1)

BACKDROP_MATERIAL = bpy.data.materials["BackdropMaterial"]

RENDER_RESOLUTION_X = 1200
RENDER_RESOLUTION_Y = 1500

RENDER_LOW_RESOLUTION_X = 400
RENDER_LOW_RESOLUTION_Y = 500

DEBUG_INFO = defaultdict(str)


def set_random_clitoris_texture():
    """Picks a random texture from the TEXTURE_DIRECTORY_PATH and assigns it to
    the clitoris material.
    """

    try:
        texture_names = list(entry.name for entry in os.scandir(TEXTURE_DIRECTORY_PATH)
                             if not entry.name.startswith('.') and entry.is_file())

        random_texture_name = choice(texture_names)

        texture_image = bpy.data.images.load(os.path.join(TEXTURE_DIRECTORY_PATH,
                                                          random_texture_name))

        CLIT_MATERIAL.node_tree.nodes[TEXTURE_NODE_NAME].image = texture_image

        DEBUG_INFO["random_texture_name"] = random_texture_name

    except FileNotFoundError:
        print("Cloud not find the texture directory", file=sys.stderr)
    except IndexError:
        print("Texture directory is empty", file=sys.stderr)


def set_random_clitoris_shape():
    """Assigns a random value between 0 and 1 to the clitoris shape key. 0 being
    a rest pose and 1 being an active pose.
    """

    activity_factor = uniform(ACTIVITY_SHAPE_KEY_RANGE[0],
                              ACTIVITY_SHAPE_KEY_RANGE[1])

    ACTIVITY_SHAPE_KEY.value = activity_factor

    DEBUG_INFO["activity_factor"] = activity_factor


def set_random_clitoris_rotation():
    """Sets a random rotation on every axis."""

    rotation_vector = (uniform(-45, 45),
                       uniform(0, 360),
                       uniform(-45, 45))

    rotation_vector_radians = (radians(scalar) for scalar in rotation_vector)

    rotation_euler_angles = mathutils.Euler(rotation_vector_radians, 'XYZ')

    TRACKBALL_OBJ.rotation_euler.rotate(rotation_euler_angles)

    DEBUG_INFO["rotation_vector"] = rotation_vector


def set_backdrop_visibility(visible):
    """Sets the backdrop visibility (does it appear in the rendering) according
    to the boolean value of visible.
    """

    cycles_settings = ("camera", "diffuse", "glossy", "transmission",
                       "scatter", "shadow")

    for setting in cycles_settings:
        bpy.data.objects["Backdrop"].cycles_visibility[setting] = visible


def set_backdrop_color():
    """Sets the backdrop color by making a low fidelity render and extracting
    an interesting color from it. The low fidelity render will show the clitoris
    on a transparent background with its applied texture.
    """

    # Changing settings

    bpy.data.scenes["Scene"].render.use_antialiasing = False
    bpy.data.scenes["Scene"].render.use_compositing = False
    bpy.data.scenes["Scene"].render.image_settings.file_format = "PNG"
    bpy.data.scenes["Scene"].render.resolution_x = RENDER_LOW_RESOLUTION_X
    bpy.data.scenes["Scene"].render.resolution_y = RENDER_LOW_RESOLUTION_Y

    set_backdrop_visibility(False)

    # Saving the low fidelity render to a temporary file

    bpy.ops.render.render()

    image = bpy.data.images["Render Result"]

    image_tmp_path = os.path.join(gettempdir(), 'clitoris_tmp_render')

    image.save_render(image_tmp_path)

    # Find the backdrop color!

    backdrop_color = palette.find_background_color(image_tmp_path)

    # Setting the backdrop color

    for index, value in enumerate(backdrop_color.rgb):
        BACKDROP_MATERIAL.node_tree.nodes["Diffuse BSDF"].inputs[0] \
        .default_value[index] = value

    # Reverting settings

    bpy.data.scenes["Scene"].render.use_antialiasing = True
    bpy.data.scenes["Scene"].render.use_compositing = True
    bpy.data.scenes["Scene"].render.image_settings.file_format = "JPEG"
    bpy.data.scenes["Scene"].render.resolution_x = RENDER_RESOLUTION_X
    bpy.data.scenes["Scene"].render.resolution_y = RENDER_RESOLUTION_Y

    set_backdrop_visibility(True)

    DEBUG_INFO["backdrop_color"] = backdrop_color.hex


def get_render_stamp():
    """Returns a string with debug information."""

    stamp_tpl = "{chosen_texture_name} - rotation: {vector}," \
                "shape_factor: {shape_factor}, color: {color}"

    stamp = stamp_tpl.format(chosen_texture_name=DEBUG_INFO["chosen_texture_name"],
                             vector=DEBUG_INFO["rotation_vector"],
                             shape_factor=DEBUG_INFO["activity_factor"],
                             color=DEBUG_INFO["backdrop_color"])

    return stamp


def set_debug_stamp():
    """Debug mode will show information on the rendering."""

    bpy.data.scenes["Scene"].render.use_stamp = True
    bpy.data.scenes["Scene"].render.use_stamp_date = True
    bpy.data.scenes["Scene"].render.use_stamp_note = True
    bpy.data.scenes["Scene"].render.use_stamp_time = False
    bpy.data.scenes["Scene"].render.use_stamp_render_time = False
    bpy.data.scenes["Scene"].render.use_stamp_frame = False
    bpy.data.scenes["Scene"].render.use_stamp_scene = False
    bpy.data.scenes["Scene"].render.use_stamp_camera = False
    bpy.data.scenes["Scene"].render.use_stamp_filename = False

    stamp = get_render_stamp()

    bpy.data.scenes["Scene"].render.stamp_note_text = stamp


def set_debug_render_log():
    """Write render information to a log file."""

    stamp = get_render_stamp()

    with open("render_log.txt", "a") as log:
        log.write("\n".join([datetime.now().strftime("%Y%m%d-%H:%M"), stamp, ""]))


def update_scene():
    """Update the scene before rendering."""

    set_random_clitoris_texture()
    set_random_clitoris_shape()
    set_random_clitoris_rotation()
    set_backdrop_color()
    #set_debug_stamp()
    #set_debug_render_log()


if __name__ == "__main__":
    print("Hello!")
    update_scene()
    print("Done!")
