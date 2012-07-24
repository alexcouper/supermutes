from supermutes.register import get_new_obj, register
from supermutes.base import SuperMutable


dotify = lambda obj: get_new_obj(obj)
"Helper function for converting a mutable"


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

    def mutate(self, value):
        return get_new_obj(value)

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
        super(DotList, self).__setattr__(attr, value)


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

    def mutate(self, value):
        print("mutating", value)
        obj = get_new_obj(value)
        print("got", obj, type(obj))
        return obj

    __getattr__ = dict.__getitem__
    __setattr__ = SuperMutable.__setitem__


d = DotDict({})
d.li = [1, 2, 3]
d.li._0
