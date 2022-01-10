import numpy as np

import cruw
from cruw.mapping.generate_grids import get_xzgrid
from cruw.mapping.ops import ra2idx, ra2idx_interpolate, bilinear_interpolate


def pol2cart(rho, phi):
    """
    Transform from polar to cart coordinates
    :param rho: distance to origin
    :param phi: angle (rad)
    :return: x, y
    """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


def cart2pol(x, y):
    """
    Transform from cart to polar coordinates
    :param x: x
    :param y: y
    :return: rho, phi (rad)
    """
    rho = (x * x + y * y) ** 0.5
    phi = np.arctan2(y, x)
    return rho, phi


def pol2cart_ramap(rho, phi):
    """
    Transform from polar to cart under RAMap coordinates
    :param rho: distance to origin
    :param phi: angle (rad) under RAMap coordinates
    :return: x, y
    """
    x = rho * np.sin(phi)
    y = rho * np.cos(phi)
    return x, y


def cart2pol_ramap(x, y):
    """
    Transform from cart to polar under RAMap coordinates
    :param x: x
    :param y: y
    :return: rho, phi (rad) under RAMap coordinates
    """
    rho = (x * x + y * y) ** 0.5
    phi = np.arctan2(x, y)
    return rho, phi


def rf2rfcart(rfim, range_grid, angle_grid, dim=(128, 101), zrange=30.0, magnitude_only=True):
    """
    Convert RF images to cart coordinates
    :param rfim: RF image data
    :param range_grid:
    :param angle_grid:
    :param dim: output cart RF image dimension
    :param zrange: largest range in z axis (in meter)
    :param magnitude_only: convert magnitude map only
    """
    xline, zline = get_xzgrid(dim, zrange)
    rf_cart = np.zeros([dim[0], dim[1], 2])

    if magnitude_only:
        rfim = np.sqrt(rfim[:, :, 0] ** 2 + rfim[:, :, 1] ** 2)

    for zi in range(dim[0]):
        for xi in range(dim[1]):
            x, z = xline[xi], zline[zi]
            rng, agl = cart2pol_ramap(x, z)
            # rid, aid = ra2idx(rng, agl, range_grid, angle_grid)
            rid_inter, aid_inter = ra2idx_interpolate(rng, agl, range_grid, angle_grid)
            rf_cart[zi, xi] = bilinear_interpolate(rfim, aid_inter, rid_inter)

    return rf_cart, (xline, zline)


if __name__ == '__main__':
    cruw = cruw.CRUW(data_root='/home/yzwang/Remote/CR3DLoc/data/ROD2021')
    rfim = np.load(
        '/home/yzwang/Remote/CR3DLoc/data/ROD2021/sequences/train/2019_09_29_ONRD001/RADAR_RA_H/000000_0000.npy')
    rfim_cart, _ = rf2rfcart(rfim, cruw.range_grid, cruw.angle_grid)
    rfim_cart_mag = np.sqrt(rfim_cart[:, :, 0] ** 2 + rfim_cart[:, :, 1] ** 2)
