import numpy as np

import cruw
from cruw.mapping.coor_transform import cart2pol_ramap
from cruw.mapping.ops import ra2idx, ra2idx_interpolate, bilinear_interpolate
from cruw.mapping.complex import ri2ap, ap2ri


def rf2rfcart(rfim, range_grid, angle_grid, xz_grid, magnitude_only=True):
    """
    Convert RF images to cart coordinates
    :param rfim: RF image data
    :param range_grid:
    :param angle_grid:
    :param dim: output cart RF image dimension
    :param zrange: largest range in z axis (in meter)
    :param magnitude_only: convert magnitude map only
    """
    xline, zline = xz_grid
    dim = (len(zline), len(xline))

    if magnitude_only:
        rf_cart = np.zeros([dim[0], dim[1], 1])
        rfim = np.sqrt(rfim[:, :, 0] ** 2 + rfim[:, :, 1] ** 2)
    else:
        rf_cart = np.zeros([dim[0], dim[1], 2])
        rfim = ri2ap(rfim)

    for zi in range(dim[0]):
        for xi in range(dim[1]):
            x, z = xline[xi], zline[zi]
            rng, agl = cart2pol_ramap(x, z)
            # rid, aid = ra2idx(rng, agl, range_grid, angle_grid)
            rid_inter, aid_inter = ra2idx_interpolate(rng, agl, range_grid, angle_grid)
            rf_cart[zi, xi] = bilinear_interpolate(rfim, aid_inter, rid_inter)

    if not magnitude_only:
        rf_cart = ap2ri(rf_cart)

    return np.squeeze(rf_cart), (xline, zline)


if __name__ == '__main__':
    cruw = cruw.CRUW(data_root='/home/yzwang/Remote/CR3DLoc/data/ROD2021')
    rfim = np.load(
        '/home/yzwang/Remote/CR3DLoc/data/ROD2021/sequences/train/2019_09_29_ONRD001/RADAR_RA_H/000000_0000.npy')
    rfim_cart, _ = rf2rfcart(rfim, cruw.range_grid, cruw.angle_grid, cruw.xz_grid)
    rfim_cart_mag = np.sqrt(rfim_cart[:, :, 0] ** 2 + rfim_cart[:, :, 1] ** 2)
