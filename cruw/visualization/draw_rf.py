import numpy as np
import matplotlib.pyplot as plt


def magnitude(chirp, radar_data_type):
    """
    Calculate magnitude of a chirp
    :param chirp: radar data of one chirp (w x h x 2) or (2 x w x h)
    :param radar_data_type: current available types include 'RI', 'RISEP', 'AP', 'APSEP'
    :return: magnitude map for the input chirp (w x h)
    """
    c0, c1, c2 = chirp.shape
    if radar_data_type == 'RI' or radar_data_type == 'RISEP':
        if c0 == 2:
            chirp_abs = np.sqrt(chirp[0, :, :] ** 2 + chirp[1, :, :] ** 2)
        elif c2 == 2:
            chirp_abs = np.sqrt(chirp[:, :, 0] ** 2 + chirp[:, :, 1] ** 2)
        else:
            raise ValueError
    elif radar_data_type == 'AP' or radar_data_type == 'APSEP':
        if c0 == 2:
            chirp_abs = chirp[0, :, :]
        elif c2 == 2:
            chirp_abs = chirp[:, :, 0]
        else:
            raise ValueError
    else:
        raise ValueError
    return chirp_abs


def draw_centers(ax, chirp, dts, colors, texts=None, chirp_type='RISEP'):
    """
    Draw object centers on RF image.
    :param ax: plt ax
    :param chirp: radar chirp data
    :param dts: [n_dts x 2] object detections
    :param colors: [n_dts]
    :param texts: [n_dts] text to show beside the centers
    :param chirp_type: radar chirp type
    :return:
    """
    chirp_abs = magnitude(chirp, chirp_type)
    ax.imshow(chirp_abs, vmin=0, vmax=1, origin='lower')
    n_dts = len(dts)
    for dt_id in range(n_dts):
        color = np.array(colors[dt_id])
        color = color.reshape((1, -1))
        ax.scatter(dts[dt_id][1], dts[dt_id][0], s=100, c=color, edgecolors='white')
        if texts is not None:
            ax.text(dts[dt_id][1] + 2, dts[dt_id][0] + 2, '%s' % texts[dt_id], c='white')


def show_rf_cart(chirp_cart, xz_grid):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(chirp_cart, vmin=0, vmax=1, origin='lower')
    ax.set_xticks(np.arange(0, len(xz_grid[0]), 30), xz_grid[0][::30])
    ax.set_yticks(np.arange(0, len(xz_grid[1]), 20), xz_grid[1][::20])
    ax.set_xlabel('x(m)')
    ax.set_ylabel('z(m)')
