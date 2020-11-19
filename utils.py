def concatenate_dicts(d0, d1):

    """Concatenates two dicts of lists.
    E.G. d0 = {1:[1,2,3], 2:[0,0]} d1 = {1:[4,5], 0:[1,2]}
    result = {0:[1,2], 1:[1,2,3,4,5], 2:[0,0,1,2]}

    Args:
        d0 (dict): dict of list
        d1 (dict): dict of list

    Returns:
        dict: merged dict
    """

    keys = set(d0).union(d1)
    default = []
    return dict((k, d0.get(k, default) + d1.get(k, default)) for k in keys)