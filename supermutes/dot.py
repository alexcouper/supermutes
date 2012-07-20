from supermutes.register import get_new_obj, register
from supermutes.base import SuperMutable


dotify = lambda obj: get_new_obj(obj)


def reset_mapping():
    register(__name__, dict, DotDict)
    register(__name__, list, DotList)


class DotList(SuperMutable, list):
    """
    A list that allows dot notation access to its items.

    For example:

    >> d = DotList(['a', 'b', 'c'])
    >> d._0
    'a'
    >> d._1
    'b'
    >> d._2
    'c'
    >> d._3
    IndexError

    """
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        for i, value in enumerate(self):
            self[i] = value

    def __getattr__(self, attr):
        try:
            index = int(attr.strip('_'))
            return self[index]
        except ValueError:
            pass
        return list.__getattr__(self, attr)

    def __setattr__(self, attr, value):
        try:
            index = int(attr.strip('_'))
            self[index] = value
        except ValueError:
            pass
        list.__setattr__(self, attr, dotify(value))

    def __setitem__(self, index, value):
        list.__setitem__(self, index, dotify(value))


class DotDict(SuperMutable, dict):
    """
    A dictionary that allows dot notation access to its values.

    For example:

    >>  d = DotDict({
            'a': 12,
            'b': {
                'something': 5
            }
        })
    >>  d.a
    12
    >>  d.b.something
    5
    >>  d.c = 99
    >>  del d['a']
    >>  del d['b']
    >>  d
    {'c': 99}
    """
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        for key, value in self.items():
            self[key] = value

    def __setitem__(self, key, value):
        super(DotDict, self).__setitem__(key, dotify(value))

    __getattr__ = dict.__getitem__
    __setattr__ = __setitem__
