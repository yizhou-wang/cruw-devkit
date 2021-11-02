import math

from cruw.mapping.coor_transform import pol2cart_ramap


def get_ols_btw_objects(obj1, obj2, dataset):
    """
    Calculate OLS between two objects.
    :param obj1: object 1 dict
    :param obj2: object 2 dict
    :param dataset: dataset object
    :return: OLS value
    """
    classes = dataset.object_cfg.classes
    object_sizes = dataset.object_cfg.sizes
    if obj1['class_id'] != obj2['class_id']:
        print('Error: Computing OLS between different classes!')
        raise TypeError("OLS can only be compute between objects with same class.  ")
    if obj1['score'] < obj2['score']:
        raise TypeError("Confidence score of obj1 should not be smaller than obj2. "
                        "obj1['score'] = %s, obj2['score'] = %s" % (obj1['score'], obj2['score']))
    classid = obj1['class_id']
    class_str = classes[classid]
    rng1 = obj1['range']
    agl1 = obj1['angle']
    rng2 = obj2['range']
    agl2 = obj2['angle']
    x1, y1 = pol2cart_ramap(rng1, agl1)
    x2, y2 = pol2cart_ramap(rng2, agl2)
    dx = x1 - x2
    dy = y1 - y2
    dist = (dx ** 2 + dy ** 2) ** 0.5
    s = (x1 ** 2 + y1 ** 2) ** 0.5
    kappa = object_sizes[class_str] / 100
    return ols(dist, s, kappa)


def get_ols_ra(obj1, obj2, dataset):
    """
    Calculate OLS between two objects.
    :param obj1: object 1 [range, angle, class_id]
    :param obj2: object 2 [range, angle, class_id]
    :param dataset: dataset object
    :return: OLS value
    """
    classes = dataset.object_cfg.classes
    object_sizes = dataset.object_cfg.sizes
    if obj1[2] != obj2[2]:
        # print('Error: Computing OLS between different classes!')
        # raise TypeError("OLS can only be compute between objects with same class.  ")
        classid = int(max(obj1[2], obj2[2]))
    else:
        classid = int(obj1[2])
    class_str = classes[classid]
    rng1 = obj1[0]
    agl1 = obj1[1]
    rng2 = obj2[0]
    agl2 = obj2[1]
    x1, y1 = pol2cart_ramap(rng1, agl1)
    x2, y2 = pol2cart_ramap(rng2, agl2)
    dx = x1 - x2
    dy = y1 - y2
    dist = (dx ** 2 + dy ** 2) ** 0.5
    s = (x1 ** 2 + y1 ** 2) ** 0.5
    kappa = object_sizes[class_str] / 100
    return ols(dist, s, kappa)


def get_ols_xy(obj1, obj2, dataset):
    """
    Calculate OLS between two objects.
    :param obj1: object 1 [x, y, class_id]
    :param obj2: object 2 [x, y, class_id]
    :param dataset: dataset object
    :return: OLS value
    """
    classes = dataset.object_cfg.classes
    object_sizes = dataset.object_cfg.sizes
    if obj1[2] != obj2[2]:
        # print('Error: Computing OLS between different classes!')
        # raise TypeError("OLS can only be compute between objects with same class.  ")
        classid = int(max(obj1[2], obj2[2]))
    else:
        classid = int(obj1[2])
    class_str = classes[classid]
    x1 = obj1[0]
    y1 = obj1[1]
    x2 = obj2[0]
    y2 = obj2[1]
    dx = x1 - x2
    dy = y1 - y2
    dist = (dx ** 2 + dy ** 2) ** 0.5
    s = (x1 ** 2 + y1 ** 2) ** 0.5
    kappa = object_sizes[class_str] / 100
    return ols(dist, s, kappa)


def ols(dist, scale, kappa):
    """Calculate OLS based on distance, scale and kappa."""
    e = dist ** 2 / 2 / (scale ** 2 * kappa)
    return math.exp(-e)
