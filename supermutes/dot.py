

def dotify(obj):
    if isinstance(obj, list) and not isinstance(obj, DotList):
        return DotList(obj)
    elif isinstance(obj, dict) and not isinstance(obj, DotDict):
        return DotDict(obj)
    return obj


class DotList(list):
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


class DotDict(dict):
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
    def __init__(self, value=None):
        if value is None:
            pass
        elif isinstance(value, dict):
            for key in value:
                self[key] = value[key]
        else:
            raise TypeError('Expected dict')

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, dotify(value))

    __getattr__ = dict.__getitem__
    __setattr__ = __setitem__
