"""
copyright tretyak@gmail.com
MIT Licence
"""

import collections


def multi_dict_as_dict(md):
    """
    See http://aiohttp.readthedocs.io/en/v0.21.5/multidict.html#aiohttp.MultiDictProxy
    """
    return {k: md[k] for k in iter(md)}


def safeget(dct, *keys, **kwargs):
    """
    function get for included dict
    :param dct:
    :param keys:
    :return: None if no key
    """
    default = kwargs.get('default', None)
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return default
    return dct or default


def dict_merge(merge_to, merge_from):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurse down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_from`` is merged into
    ``merge_to``.
    :param merge_to: dict onto which the merge is executed
    :param merge_from: merge_to merged into merge_to
    :return: merge_to
    """
    for k, v in merge_from.items():
        if (k in merge_to and isinstance(merge_to[k], dict)
                and isinstance(merge_from[k], collections.Mapping)):
            dict_merge(merge_to[k], merge_from[k])
        else:
            merge_to[k] = merge_from[k]
    return merge_to


def walk(node, leaf_perform):
    """ Walk through a dictionary(list) and perform action to each 'leaf' value
    :param node: <dict|list>
    :param leaf_perform: <function>
    :return: updated node
    """
    if isinstance(node, list):
        for item in node:
            walk(item, leaf_perform)
    elif isinstance(node, dict):
        for key, item in list(node.items()):
            node[key] = walk(item, leaf_perform)
    else:
        node = leaf_perform(node)
    return node
