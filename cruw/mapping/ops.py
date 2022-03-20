import numpy as np

from cruw.mapping.coor_transform import pol2cart_ramap, cart2pol_ramap


def find_nearest(array, value):
    """Find nearest value to 'value' in 'array'."""
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]


def idx2ra(rng_id, agl_id, range_grid, angle_grid):
    """Mapping from ra indices to absolute range (m) and azimuth (rad)."""
    rng = range_grid[rng_id]
    agl = angle_grid[agl_id]
    return rng, agl


def idx2ra_interpolate(rng_id, agl_id, range_grid, angle_grid):
    """Mapping from ra indices to absolute range (m) and azimuth (rad)."""
    rids = np.arange(range_grid.shape[0])
    aids = np.arange(angle_grid.shape[0])
    rng = np.interp(rng_id, rids, range_grid)
    agl = np.interp(agl_id, aids, angle_grid)
    return rng, agl


def ra2idx(rng, agl, range_grid, angle_grid):
    """Mapping from absolute range (m) and azimuth (rad) to ra indices."""
    rng_id, _ = find_nearest(range_grid, rng)
    agl_id, _ = find_nearest(angle_grid, agl)
    return rng_id, agl_id


def ra2idx_interpolate(rng, agl, range_grid, angle_grid):
    """get interpolated RA indices in float"""
    rids = np.arange(range_grid.shape[0])
    aids = np.arange(angle_grid.shape[0])
    rng_id = np.interp(rng, range_grid, rids)
    agl_id = np.interp(np.sin(agl), np.sin(angle_grid), aids)
    return rng_id, agl_id


def xz2idx_interpolate(x, z, x_grid, z_grid):
    """get interpolated XZ indices in float"""
    xids = np.arange(x_grid.shape[0])
    zids = np.arange(z_grid.shape[0])
    x_id = np.interp(x, x_grid, xids)
    z_id = np.interp(z, z_grid, zids)
    return x_id, z_id


def xz2raidx(x, z, range_grid, angle_grid):
    rng, agl = cart2pol_ramap(x, z)
    rng_id, agl_id = ra2idx(rng, agl, range_grid, angle_grid)
    return rng_id, agl_id


def xz2raidx_interpolate(x, z, range_grid, angle_grid):
    rng, agl = cart2pol_ramap(x, z)
    rng_id, agl_id = ra2idx_interpolate(rng, agl, range_grid, angle_grid)
    return rng_id, agl_id


def ra2xzidx_interpolate(rng, agl, xz_grid):
    x, z = pol2cart_ramap(rng, agl)
    x_id, z_id = xz2idx_interpolate(x, z, *xz_grid)
    return x_id, z_id


def bilinear_interpolate(im, x, y):
    x = np.asarray(x)
    y = np.asarray(y)

    x0 = np.floor(x).astype(int)
    x1 = x0 + 1
    y0 = np.floor(y).astype(int)
    y1 = y0 + 1

    x0 = np.clip(x0, 0, im.shape[1] - 1)
    x1 = np.clip(x1, 0, im.shape[1] - 1)
    y0 = np.clip(y0, 0, im.shape[0] - 1)
    y1 = np.clip(y1, 0, im.shape[0] - 1)

    Ia = im[y0, x0]
    Ib = im[y1, x0]
    Ic = im[y0, x1]
    Id = im[y1, x1]

    wa = (x1 - x) * (y1 - y)
    wb = (x1 - x) * (y - y0)
    wc = (x - x0) * (y1 - y)
    wd = (x - x0) * (y - y0)

    return wa * Ia + wb * Ib + wc * Ic + wd * Id
