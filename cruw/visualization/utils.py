import random
import colorsys


def generate_colors_code(number_of_colors):
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
              for i in range(number_of_colors)]
    return colors


# adapted from https://github.com/matterport/Mask_RCNN/blob/master/mrcnn/visualize.py
def generate_colors_rgb(n_colors):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 0.7
    hsv = [(i / n_colors, 1, brightness) for i in range(n_colors)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    colors = [list(color) for color in colors]
    return colors
