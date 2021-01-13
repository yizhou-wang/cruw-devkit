import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib import gridspec

from cruw.mapping import ra2idx

from .draw_rgb import draw_dets
from .draw_rf import draw_centers
from .utils import generate_colors_rgb


def show_dataset(image_path, chirp_path, anno_path):
    frame_id = int(image_path.split('/')[-1][:-4])
    img = plt.imread(image_path)
    chirp = np.load(chirp_path)
    anno = json.load(open(anno_path, 'rb'))
    metadata = anno['metadata'][frame_id]

    fig = plt.figure()
    fig.set_size_inches(16, 5)
    gs = gridspec.GridSpec(1, 2)

    ax1 = plt.subplot(gs[0])
    ax1.axis('off')
    draw_dets(ax1, img, [], [])
    ax1.set_title('RGB Image')

    ax2 = plt.subplot(gs[1])
    ax2.axis('off')
    n_obj = metadata['rad_h']['n_objects']
    categories = metadata['rad_h']['obj_info']['categories']
    center_ids = metadata['rad_h']['obj_info']['center_ids']
    colors = generate_colors_rgb(n_obj)
    draw_centers(ax2, chirp, center_ids, colors, texts=categories)
    ax2.set_title('RF Image (BEV)')

    fig.subplots_adjust(hspace=0, wspace=0)


def show_dataset_rod2021(image_path, chirp_path, anno_path, dataset):
    frame_id = int(image_path.split('/')[-1][:-4])
    img = plt.imread(image_path)
    chirp = np.load(chirp_path)
    with open(anno_path, 'r') as f:
        lines = f.readlines()
    center_ids = []
    categories = []
    for line in lines:
        fid, rng, azm, class_name = line.rstrip().split()
        fid = int(fid)
        if fid == frame_id:
            rng = float(rng)
            azm = float(azm)
            rid, aid = ra2idx(rng, azm, dataset.range_grid, dataset.angle_grid)
            center_ids.append([rid, aid])
            categories.append(class_name)
    center_ids = np.array(center_ids)
    n_obj = len(categories)

    fig = plt.figure()
    fig.set_size_inches(16, 5)
    gs = gridspec.GridSpec(1, 2)

    ax1 = plt.subplot(gs[0])
    ax1.axis('off')
    draw_dets(ax1, img, [], [])
    ax1.set_title('RGB Image')

    ax2 = plt.subplot(gs[1])
    ax2.axis('off')
    colors = generate_colors_rgb(n_obj)
    draw_centers(ax2, chirp, center_ids, colors, texts=categories)
    ax2.set_title('RF Image (BEV)')

    fig.subplots_adjust(hspace=0, wspace=0)
