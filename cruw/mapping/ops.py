import numpy as np


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


def ra2idx(rng, agl, range_grid, angle_grid):
    """Mapping from absolute range (m) and azimuth (rad) to ra indices."""
    rng_id, _ = find_nearest(range_grid, rng)
    agl_id, _ = find_nearest(angle_grid, agl)
    return rng_id, agl_id
