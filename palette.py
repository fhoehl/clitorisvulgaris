#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A tool to find an interesting background color that constrasts well with a
foreground object. The chosen color is the complement of a highlight on the
foreground object.
"""

from argparse import ArgumentParser
from collections import namedtuple
from colorsys import rgb_to_hsv, hsv_to_rgb

import scipy
from scipy.cluster.vq import kmeans, vq
from scipy.misc import fromimage
from PIL import Image, ImageEnhance
from skimage import img_as_float

THUMBNAIL_SIZE = (400, 400)
CONTRAST = 1.5
CLUSTER_NUMBER = 8


def rgb_to_hex(rgb):
    """Returns the hex color code for the rgb tuple."""

    hexcodes = ("%02x" % int(v * 255) for v in rgb)

    return "#%s" % "".join(hexcodes)


def parse_args():
    """Parse and return cli arguments"""

    description = "A tool to find an interesting background color that" \
                  "constrasts well with a object."

    parser = ArgumentParser(description=description)

    parser.add_argument("image",
                        help="an image",
                        type=str)

    return parser.parse_args()


def prepare_image(image_fd):
    """Returns a PIL image from the given file descriptor. The image is
    resized in order to filtrate dominant colors and ease k-means computation.
    The contrast of the image is also enhanced to help find more saturated
    colors.
    """

    image = Image.open(image_fd)
    image.thumbnail(THUMBNAIL_SIZE)
    contrast = ImageEnhance.Contrast(image)
    image_high_contrast = contrast.enhance(CONTRAST)

    return image_high_contrast


def find_dominant_colors(image):
    """Cluster the colors of the image in CLUSTER_NUMBER of clusters. Returns
    an array of dominant colors reverse sorted by cluster size.
    """

    array = img_as_float(fromimage(image))

    # Reshape from MxNx4 to Mx4 array
    array = array.reshape(scipy.product(array.shape[:2]), array.shape[2])

    # Remove transparent pixels if any (channel 4 is alpha)
    if array.shape[-1] > 3:
        array = array[array[:, 3] == 1]

    # Finding centroids (centroids are colors)
    centroids, _ = kmeans(array, CLUSTER_NUMBER)

    # Allocate pixel to a centroid cluster
    observations, _ = vq(array, centroids)

    # Calculate the number of pixels in a cluster
    histogram, _ = scipy.histogram(observations, len(centroids))

    # Sort centroids by number of pixels in their cluster
    sorted_centroids = sorted(zip(centroids, histogram),
                              key=lambda x: x[1],
                              reverse=True)

    sorted_colors = tuple((couple[0] for couple in sorted_centroids))

    return sorted_colors


def find_background_color(image_path):
    """Find an interesting background color for the given image. Returns
    color rgb and hex value tuple.
    """

    color = __find_background_color(image_path)

    simple_color = namedtuple("SimpleColor", ["rgb", "RGB", "hex"])

    return simple_color(rgb=color,
                        RGB=tuple(int(v * 255) for v in color),
                        hex=rgb_to_hex(color))


def __find_background_color(image_path):
    """Find an interesting background color for the given image."""

    with open(image_path, "rb") as image_file:
        image = prepare_image(image_file)

        dominant_color = find_dominant_colors(image)[-1]
        dominant_color_hsl = rgb_to_hsv(*dominant_color[:3])

        dominant_color_complement_hsl = (dominant_color_hsl[0] + .5,
                                         dominant_color_hsl[1],
                                         dominant_color_hsl[2])

        return hsv_to_rgb(*dominant_color_complement_hsl)


def main():
    """Main"""

    args = parse_args()
    color = find_background_color(args.image)
    print(color.hex, color.RGB, color.rgb)


if __name__ == "__main__":
    main()
