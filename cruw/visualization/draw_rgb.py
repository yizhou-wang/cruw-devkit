import numpy as np
import pycocotools.mask as cocomask
from matplotlib.patches import Rectangle


def draw_dets(ax, img, bboxes, colors, texts=None, masks=None):
    """
    Draw bounding boxes on image.
    :param ax: plt ax
    :param img: image
    :param bboxes: xywh n_bbox x 4
    :param colors: n_bbox colors
    :param texts: n_bbox text strings
    :param masks: n_bbox rle masks
    :return:
    """
    n_bbox = len(bboxes)
    for bbox_id in range(n_bbox):
        bbox = bboxes[bbox_id]
        ax.add_patch(Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=1,
                               edgecolor=colors[bbox_id], facecolor='none'))
        if texts is not None:
            ax.text(bbox[0], bbox[1], texts[bbox_id], color=colors[bbox_id])
        if masks is not None:
            binary_mask = cocomask.decode(masks[bbox_id])
            apply_mask(img, binary_mask, colors[bbox_id])
    ax.imshow(img)


# from https://github.com/matterport/Mask_RCNN/blob/master/mrcnn/visualize.py
def apply_mask(image, mask, color, alpha=0.25):
    """Apply the given mask to the image.
    """
    for c in range(3):
        image[:, :, c] = np.where(mask == 1,
                                  image[:, :, c] * (1 - alpha) + alpha * color[c],
                                  image[:, :, c])
    return image
